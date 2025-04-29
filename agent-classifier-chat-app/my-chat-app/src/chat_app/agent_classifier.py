import json
import os
import asyncio
from azure.identity import DefaultAzureCredential
from semantic_kernel.agents import AzureAIAgent, AzureAIAgentThread
from azure.ai.projects import AIProjectClient


class AgentClassifier:
    def __init__(self):
        self.creds = DefaultAzureCredential()
        self.client = AzureAIAgent.create_client(credential=self.creds, conn_str=os.getenv("AZURE_AI_AGENT_PROJECT_CONNECTION_STRING"))
        self.agent_thread = None

    async def load_agent(self, agent_id):
        self.agent_thread = AzureAIAgentThread(client=self.client)
        agent_definition = await self.client.agents.get_agent(agent_id)
        return AzureAIAgent(client=self.client, definition=agent_definition)

    async def orchestrator(self, manifest_path, input_text):
        with open(manifest_path, 'r') as file:
            manifest = json.load(file)
            agents = manifest.get('agents', [])
            agent_id = self.get_agent_id_from_input(agents, input_text)

            if agent_id:
                return agent_id

            prompt = self.create_prompt(manifest, input_text)
            generic_agent = await self.client.agents.get_agent(os.getenv("AI_ASSISTANT_GENERIC"))
            agent = AzureAIAgent(client=self.client, definition=generic_agent)

            async for content in agent.invoke(messages=prompt, thread=self.agent_thread):
                return content.content

    def get_agent_id_from_input(self, agents, input_text):
        if "@" in input_text:
            agent_name = input_text.split("@")[1].split(" ")[0]
            for agent in agents:
                if agent['agent-name'] == agent_name:
                    return agent['agent_id']
        return None

    def create_prompt(self, manifest, input_text):
        return f"Please choose an agent from the following manifest:\n{json.dumps(manifest, indent=4)}\n\nWhich agent would you like to use in order that meet the following input text: {input_text}. You should choose the agent based on the input text closeness with the utterances depicted on the manifest.\n\n Return just the information on the agent_id field."

    async def close(self):
        await self.client.close()
        if self.agent_thread:
            await self.agent_thread.delete()