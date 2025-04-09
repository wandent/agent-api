
import asyncio
import os
from azure.ai.projects import AIProjectClient
from azure.ai.projects.models import CodeInterpreterTool, Agent, AgentThread
from azure.identity import DefaultAzureCredential
from semantic_kernel import Kernel
from semantic_kernel.agents import AzureAIAgent, AzureAIAgentThread
from semantic_kernel.agents import AgentGroupChat
from dotenv import load_dotenv, find_dotenv

load_dotenv(find_dotenv())  # Load environment variables from .env file
kernel = Kernel()
creds = DefaultAzureCredential()
client = AzureAIAgent.create_client(credential=creds, conn_str=os.getenv("AZURE_AI_AGENT_PROJECT_CONNECTION_STRING"))

async def main():
    prompt_validator_def = await client.agents.get_agent(os.getenv("AI_ASSISTANT_PROMPT_VALIDATOR"))
    promtp_engineer_def = await client.agents.get_agent(os.getenv("AI_ASSISTANT_PROMPT_ENGINEER"))
    
    # create the agents
    agent_prompt_validator = AzureAIAgent(client=client,
                         definition=prompt_validator_def)
    
    agent_prompt_engineer = AzureAIAgent(client=client,
                         definition=promtp_engineer_def)
    # create the threads
    thread = AzureAIAgentThread(client=client)


    while True:
        if thread is None:
            thread = AzureAIAgentThread(client=client)
        user_input = input("Enter your message: ")
        if user_input == "exit":
            exit(0)
        if user_input =="new chat":
            thread = AzureAIAgentThread(client=client)
            continue

        # send the message to the prompt engineer agent
        run = await agent_prompt_engineer.invoke(user_input)
        print(f"Prompt Engineer: {run.content}")

        print("Is your request complete? (yes/no)")
        user_input = input()
        if user_input.lower() == "yes":
            run = await agent_prompt_validator.invoke(run.content)
            print(f"Prompt Validator: {run.content}")
            continue
        else:
            print("Please provide more details.")
            user_input = input()

        
    
# call the main function
if __name__ == "__main__":
    asyncio.run(main())



     