import json
import asyncio
import os
from semantic_kernel import Kernel
from semantic_kernel.agents import AzureAIAgent, AzureAIAgentThread

from azure.identity import DefaultAzureCredential
from orchestrator import Orchestrator

from ui import ChatAppUI
from agent_classifier import AgentClassifier
from dotenv import load_dotenv, find_dotenv
load_dotenv(find_dotenv())  # Load environment variables from .env file

async def main():
    creds = DefaultAzureCredential()
    client = AzureAIAgent.create_client(credential=creds, conn_str=os.getenv("AZURE_AI_AGENT_PROJECT_CONNECTION_STRING"))

    chat = ChatAppUI()

    agent_id = ""
    await chat.run_chat()



if __name__ == "__main__":
    asyncio.run(main())