import json
import asyncio
import os
from semantic_kernel import Kernel
from semantic_kernel.agents import AzureAIAgent, AzureAIAgentThread

from azure.identity import DefaultAzureCredential
from orchestrator import orchestrator

from ui import ChatAppUI
from agent_classifier import AgentClassifier
from dotenv import load_dotenv, find_dotenv
load_dotenv(find_dotenv())  # Load environment variables from .env file

async def main():
    creds = DefaultAzureCredential()
    client = AzureAIAgent.create_client(credential=creds, conn_str=os.getenv("AZURE_AI_AGENT_PROJECT_CONNECTION_STRING"))

    chat = ChatAppUI()
    chat.display_welcome_message()

    agent_id = ""
    
    while True:
        user_input = chat.get_user_input()
        
        if user_input.lower() == "exit":
            print("Goodbye!")
            break
        
        if user_input.lower() == "new chat":
            agent_id = ""
            print("New chat started.")
            continue
        
        if agent_id == "":
            agent_id = await orchestrator( "./agents-manifest.json", user_input)
            print(f"Selected agent: {agent_id}")
        
        #try:
            agent_classifier = AgentClassifier()
            agent = await agent_classifier.load_agent(agent_id)
            async for content in agent.invoke(messages=[user_input], thread=agent_classifier.agent_thread, max_completion_tokens=4096):
                chat.display_response(content.content)
        
        #except Exception as e:
        #    print(f"Error: {e}")
        #    print("Error in the request, my responses are limited. Please try again.")

if __name__ == "__main__":
    asyncio.run(main())