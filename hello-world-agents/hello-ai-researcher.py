
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

load_dotenv(find_dotenv())  # Load environment variables from .env file
kernel = Kernel()
creds = DefaultAzureCredential()
client = AzureAIAgent.create_client(credential=creds, conn_str=os.getenv("AZURE_AI_AGENT_PROJECT_CONNECTION_STRING"))


async def load_agent():
    # 1. Define an agent on the Azure AI agent service
    agent_definition = await client.agents.get_agent(os.getenv("AI_ASSISTANT_RESEARCHER"))
    # 2. Create a Semantic Kernel agent based on the agent definition
   
    agent = AzureAIAgent(client=client,
                        definition=agent_definition)
    
    # user_inputs = ["Hello", "Look for AI papers related to watermarking techniques in text generation?"]

    return agent

# async def load_thread():
#     thread: AzureAIAgentThread = AzureAIAgentThread(client=client)
#     thread = AzureAIAgentThread(client=client)
#     return thread 

async def main():
    try:
       # request the user input in loop until the user types "exit"
        agent = await load_agent()
        #thread = await load_thread()
        thread = None
        print("Hello, I am your AI assistant. Type 'exit' to end the conversation.")
        while True:
            user_input = input("You: ")
            if user_input.lower() == "exit":
                    await thread.delete() if thread else None
                    await client.close()
                    print("Goodbye!")
                    break
            # Invoke the agent with the user input
            async for content in agent.invoke(messages=user_input, thread=thread):
                print(f"AI: {content.content}")
                thread = content.thread
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



