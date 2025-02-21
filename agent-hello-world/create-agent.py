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

project_client = AIProjectClient.from_connection_string(
    credential=DefaultAzureCredential(), conn_str=os.getenv("AZURE_PROJECT_CONNECTION_STRING")
)

with project_client:
    # Create an instance of the CodeInterpreterTool
    code_interpreter = CodeInterpreterTool()

    # The CodeInterpreterTool needs to be included in creation of the agent
    agent = project_client.agents.create_agent(
        model="gpt-4o-mini",
        name="promptengineer",
        instructions="""
            I want you to become my Prompt engineer.
            Your goal is to help me craft the best possible prompt for my needs. The prompts should (if necessary) leverage reasoning techniques. Start creating a prompt with zero-shot, if the problem is too complex, reflect and ask for more details. Also, depending on the description and complexity of the problem to be resolved, you might need to resort to creating a prompt with Chain of Thought
            The prompt will be used by you, ChatGPT. You will follow the following process:
            1. Your first response will be to ask me what the prompt should be about. I will provide my answer, but we will 
            need to improve it through continual iterations by going through the next steps.
            2. Based on my input, you will generate 2 sections, a) Revised prompt (provide your rewritten prompt, it should 
            be clear, concise, and easily understood by you), b) Questions (ask any relevant questions pertaining to what 
            additional information is needed from me to improve the prompt).
            3.You should reflect if the created prompt will lead to accurate answers for the request, you should review it and rewrite if necessary. Ask for more details if you feel like you need more information. 
            3. We will continue this iterative process with me providing additional information to you and you updating 
            the prompt in the Revised prompt section until I say we are done.
        """,
        tools=code_interpreter.definitions,
        tool_resources=code_interpreter.resources,
    )
    print(f"Created agent, agent ID: {agent.id}")

    # Create a thread
    thread = project_client.agents.create_thread()
    print(f"Created thread, thread ID: {thread.id}")

    # Create a message
    message = project_client.agents.create_message(
        thread_id=thread.id,
        role="user",
        content="Help me to craft a prompt for a study plan related to AI Development.",
    )
    print(f"Created message, message ID: {message.id}")

    # Run the agent
    run = project_client.agents.create_and_process_run(thread_id=thread.id, assistant_id=agent.id)
    print(f"Run finished with status: {run.status}")

    if run.status == "failed":
        # Check if you got "Rate limit is exceeded.", then you want to get more quota
        print(f"Run failed: {run.last_error}")

    # Get messages from the thread
    messages = project_client.agents.list_messages(thread_id=thread.id)
    print(f"Messages: {messages}")

    # Get the last message from the sender
    last_msg = messages.get_last_text_message_by_role("assistant")
    if last_msg:
        print(f"Last Message: {last_msg.text.value}")

    # Generate an image file for the bar chart
    for image_content in messages.image_contents:
        print(f"Image File ID: {image_content.image_file.file_id}")
        file_name = f"{image_content.image_file.file_id}_image_file.png"
        project_client.agents.save_file(file_id=image_content.image_file.file_id, file_name=file_name)
        print(f"Saved image file to: {Path.cwd() / file_name}")

    # Print the file path(s) from the messages
    for file_path_annotation in messages.file_path_annotations:
        print(f"File Paths:")
        print(f"Type: {file_path_annotation.type}")
        print(f"Text: {file_path_annotation.text}")
        print(f"File ID: {file_path_annotation.file_path.file_id}")
        print(f"Start Index: {file_path_annotation.start_index}")
        print(f"End Index: {file_path_annotation.end_index}")
        project_client.agents.save_file(file_id=file_path_annotation.file_path.file_id, file_name=Path(file_path_annotation.text).name)

    # Delete the agent once done
    project_client.agents.delete_agent(agent.id)
    print("Deleted agent")