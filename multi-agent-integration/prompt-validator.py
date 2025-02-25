import os
from azure.ai.projects import AIProjectClient
from azure.ai.projects.models import CodeInterpreterTool
from azure.identity import DefaultAzureCredential
from typing import Any
from pathlib import Path
from dotenv import load_dotenv
from dotenv import find_dotenv

# autogen imports
from autogen.agentchat import assistant_agent
from autogen.agentchat.groupchat import GroupChat
from autogen.io import console
from autogen.messages import agent_messages, client_messages, print_message, base_message


# Load environment variables from .env file
load_dotenv(find_dotenv())  