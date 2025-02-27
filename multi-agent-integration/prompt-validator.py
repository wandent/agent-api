import os
import io
from azure.ai.projects import AIProjectClient
from azure.ai.projects.models import CodeInterpreterTool
from azure.identity import DefaultAzureCredential
from typing import Any
from pathlib import Path
from dotenv import load_dotenv
from dotenv import find_dotenv

# autogen imports
from autogen import ConversableAgent
from autogen import AssistantAgent
from autogen.agentchat.groupchat import GroupChat
from autogen.io import console
from autogen.messages import agent_messages, client_messages, print_message, base_message


# Load environment variables from .env file
load_dotenv(find_dotenv())  

def create_client():
    project_client = AIProjectClient.from_connection_string(
        credential=DefaultAzureCredential(), conn_str=os.getenv("AZURE_PROJECT_CONNECTION_STRING")
    )
    return project_client

def call_agent(project_client, assistant_id: str):
    agent = project_client.agents.get_agent(assistant_id=assistant_id, )
   
    return agent

def create_thread(project_client):
    # Create a thread
    thread = project_client.agents.create_thread()
    #print(f"Created thread, thread ID: {thread.id}")
    return thread

def create_message(project_client, thread,  prompt: str):
    message = project_client.agents.create_message(
        thread_id=thread.id,
        role="user",
        content=prompt,
    )
    return message

def main():
    project_client = create_client()
    agent_prompt = call_agent(project_client, assistant_id="asst_imwZWQebLCDze69a7s8A1G65")
    agent_validator = call_agent(project_client, assistant_id="asst_PbCZepsK9W1SE3uyRecqTJKr")
    thread = None
    thread_valid = None   
    while True:
        if thread is None:
            thread = create_thread(project_client)
        user_input = input("Enter your message: ")
        if user_input == "exit":
            exit(0)
        if user_input =="new chat":
            thread = create_thread(project_client)
            continue

        message = create_message(project_client, thread, user_input)
        run = project_client.agents.create_and_process_run(thread_id=thread.id, assistant_id=agent_prompt.id)
        print(f"Run finished with status: {run.status}")
        if run.status == "failed":
            break
        # print the response if successful
        messages = project_client.agents.list_messages(thread_id=thread.id)
        output =  messages.get_last_text_message_by_role("assistant")
        print(f"Messages: {output.text.value}")
        run_validation = project_client.agents.create_and_process_run(thread_id=thread.id, assistant_id=agent_validator.id)
        messages = project_client.agents.list_messages(thread_id=thread.id) 
        status =  messages.get_last_text_message_by_role("assistant")
        print(f'validation: {status.text.value}')
       
            
# Call the main function
if __name__ == "__main__":
    main()





            




# call the main function async
if __name__ == "__main__":
    import asyncio
    asyncio.run(main())

