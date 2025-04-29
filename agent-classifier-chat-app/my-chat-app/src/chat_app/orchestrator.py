import json
import os
from azure.identity import DefaultAzureCredential
from semantic_kernel.agents import AzureAIAgent, AzureAIAgentThread

class Orchestrator:
    def __init__(self):
        self.creds = DefaultAzureCredential()
        self.client = AzureAIAgent.create_client(
            credential=self.creds,
            conn_str=os.getenv("AZURE_AI_AGENT_PROJECT_CONNECTION_STRING")
        )
        self.orch_thread = None

    async def orchestrate(self, manifest_path: str, input_text: str) -> str:
        """
        Reads the manifest, picks an agent by name if mentioned,
        otherwise asks the generic agent to choose one.
        Returns the selected agent_id.
        """
        self.orch_thread = AzureAIAgentThread(client=self.client)

        with open(manifest_path, 'r', encoding='utf-8') as f:
            manifest = json.load(f)

        # direct lookup if user mentions "@agent-name"
        if "@" in input_text:
            agent_name = input_text.split("@", 1)[1].split()[0]
            for agent in manifest.get("agents", []):
                if agent.get("agent-name") == agent_name:
                    return agent["agent_id"]

        # ask generic to choose for us
        prompt = (
            f"Please choose an agent from the following manifest:\n"
            f"{json.dumps(manifest, indent=4)}\n\n"
            f"Which agent would you like to use to handle this input: {input_text}\n"
            "Return just the agent_id."
        )
        generic = await self.client.agents.get_agent(os.getenv("AI_ASSISTANT_GENERIC"))
        agent = AzureAIAgent(client=self.client, definition=generic)
        async for response in agent.invoke(messages=prompt):
            return response.content

        