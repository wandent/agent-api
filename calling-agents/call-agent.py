import os
from azure.ai.projects import AIProjectClient
from azure.ai.projects.models import CodeInterpreterTool
from azure.identity import DefaultAzureCredential
from typing import Any
from pathlib import Path
from dotenv import load_dotenv
from dotenv import find_dotenv
# Load environment variables from .env file
load_dotenv(find_dotenv())  



# Create an Azure AI Client from a connection string, copied from your Azure AI Foundry project.
# At the moment, it should be in the format "<HostName>;<AzureSubscriptionId>;<ResourceGroup>;<ProjectName>"
# HostName can be found by navigating to your discovery_url and removing the leading "https://" and trailing "/discovery"
# To find your discovery_url, run the CLI command: az ml workspace show -n {project_name} --resource-group {resource_group_name} --query discovery_url
# Project Connection example: eastus.api.azureml.ms;12345678-abcd-1234-9fc6-62780b3d3e05;my-resource-group;my-project-name
# Customer needs to login to Azure subscription via Azure CLI and set the environment variables

def create_client():
    project_client = AIProjectClient.from_connection_string(
        credential=DefaultAzureCredential(), conn_str=os.getenv("AZURE_PROJECT_CONNECTION_STRING")
    )
    return project_client

def call_agent(project_client, assistant_id: str):
    agent = project_client.agents.get_agent(assistant_id=assistant_id, )
    print(f"Agent ID: {agent.id}")
    print(f"Agent Name: {agent.name}")
    print(f"Agent Instructions: {agent.instructions}")
    print(f"Agent Model: {agent.model}")
    print(f"Agent Tools: {agent.tools}")
    print(f"Agent Tool Resources: {agent.tool_resources}")
    return agent

def create_thread(project_client):
    # Create a thread
    thread = project_client.agents.create_thread()
    print(f"Created thread, thread ID: {thread.id}")
    return thread

def create_message(project_client, prompt: str):
    message = project_client.agents.create_message(
        thread_id=thread.id,
        role="user",
        content=prompt,
    )
    return message

# create the main function, where we have a loop receiving the user input and calling create_message
if __name__ == "__main__":
        thread = None   
        while True:
            if thread is None:
                project_client = create_client()
                agent = call_agent(project_client, assistant_id="asst_imwZWQebLCDze69a7s8A1G65")
                thread = create_thread(project_client)
            user_input = input("Enter your message: ")
            if user_input == "exit":
                break
            if user_input == "new chat":
                print ("Creating new chat")
                thread = create_thread(project_client)
                continue
            message = create_message(project_client, prompt=user_input)
            print(f"Created message, message ID: {message.id}")
            run = project_client.agents.create_and_process_run(thread_id=thread.id, assistant_id=agent.id)
            print(f"Run finished with status: {run.status}")

            if run.status == "failed":
                # Check if you got "Rate limit is exceeded.", then you want to get more quota
                print(f"Run failed: {run.last_error}")

            # Get messages from the thread
            messages = project_client.agents.list_messages(thread_id=thread.id)
            output =  messages.get_last_text_message_by_role("assistant")
            
            print(f"Messages: {output.text.value}")




  
    