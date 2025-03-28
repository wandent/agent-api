
""""
# Original Environment Variables
# These are the environment variables that need to be set for the Azure AI Agent to work properly.
# replace with the ones on .env file

AZURE_AI_AGENT_PROJECT_CONNECTION_STRING = "<example-connection-string>"
AZURE_AI_AGENT_MODEL_DEPLOYMENT_NAME = "<example-model-deployment-name>"
AZURE_AI_AGENT_ENDPOINT = "<example-endpoint>"
AZURE_AI_AGENT_SUBSCRIPTION_ID = "<example-subscription-id>"
AZURE_AI_AGENT_RESOURCE_GROUP_NAME = "<example-resource-group-name>"
AZURE_AI_AGENT_PROJECT_NAME = "<example-project-name>"
AZURE_AI_AGENT_MODEL_DEPLOYMENT_NAME = "<example-model-deployment-name>"
"""

import asyncio
import os
from azure.ai.projects import AIProjectClient
from azure.ai.projects.models import CodeInterpreterTool, Agent, AgentThread
from azure.identity import DefaultAzureCredential
from semantic_kernel import Kernel
from semantic_kernel.agents import AzureAIAgent, AzureAIAgentThread
from dotenv import load_dotenv, find_dotenv

async def main():
    load_dotenv(find_dotenv())  # Load environment variables from .env file
    creds = DefaultAzureCredential()
    #client = AIProjectClient(credential=creds, endpoint=os.getenv("AZURE_AI_AGENT_PROJECT_CONNECTION_STRING"),  project_name=os.getenv("AZURE_AI_AGENT_PROJECT_NAME"), subscription_id=os.getenv("AZURE_AI_AGENT_SUBSCRIPTION_ID"), resource_group_name=os.getenv("AZURE_AI_AGENT_RESOURCE_GROUP_NAME"),)
    client = AIProjectClient.from_connection_string(os.getenv("AZURE_AI_AGENT_PROJECT_CONNECTION_STRING"), credential=creds)
    # 1. Define an agent on the Azure AI agent service
    agent_definition =  client.agents.get_agent("asst_imwZWQebLCDze69a7s8A1G65")
    print(agent_definition.id)
    # 2. Create a Semantic Kernel agent based on the agent definition
   
    agent = await AzureAIAgent(client=client, definition=agent_definition)
       
    

    user_inputs = ["Hello", "Look for AI papers related to watermarking techniques in text generation?"]

    thread: AzureAIAgentThread = AzureAIAgentThread(client=client)
    thread = AzureAIAgentThread(client=client)
    try:
        for user_input in user_inputs:
            response =  agent.get_response(messages=user_input, thread=thread)
            print(f"User: {user_input}")
            print(f"AI: {response.content}")
            # print(response)
            thread = response.thread
    finally:
        await thread.delete() if thread else None


    """
    for user_input in USER_INPUTS:
        async for content in agent.invoke(message=user_input, thread=thread):
            print(content.content)
            thread = response.thread
    """

# call the main function
if __name__ == "__main__":
    asyncio.run(main())



