import json
import os
from azure.identity import DefaultAzureCredential
from semantic_kernel.agents import AzureAIAgent, AzureAIAgentThread

creds = DefaultAzureCredential()
client = AzureAIAgent.create_client(credential=creds, conn_str=os.getenv("AZURE_AI_AGENT_PROJECT_CONNECTION_STRING"))

async def orchestrator(manifest_path, input_text):
    with open(manifest_path, 'r') as file:
        manifest = json.load(file)
        
        if "@" in input_text:
            agent_name = input_text.split("@")[1].split(" ")[0]
            agents = manifest.get('agents', [])
            for agent in agents:
                if agent['agent-name'] == agent_name:
                    return agent['agent_id']

        prompt = f"Please choose an agent from the following manifest:\n{json.dumps(manifest, indent=4)}\n\nWhich agent would you like to use in order that meet the following input text: {input_text}. You should choose the agent based on the input text closeness with the utterances depicted on the manifest.\n\n Return just the information on the agent_id field."
        generic_agent = await client.agents.get_agent(os.getenv("AI_ASSISTANT_GENERIC"))
        agent = AzureAIAgent(client=client, definition=generic_agent)
        async for content in agent.invoke(messages=prompt):
            response = content.content

    return response