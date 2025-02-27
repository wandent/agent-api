import os

from autogen import ConversableAgent
from autogen import AssistantAgent
from dotenv import load_dotenv
from dotenv import find_dotenv

#    "model": "<your Azure OpenAI deployment name>",
#    "api_key": "<your Azure OpenAI API key here>",
#    "base_url": "<your Azure OpenAI API base here>",
#    "api_type": "azure",
#    "api_version": "<your Azure OpenAI API version here>"

load_dotenv(find_dotenv())  

prompt = AssistantAgent("prompt", 
                llm_config={"config_list": [{"model": "gpt-4o", "api_key": os.environ.get("AZURE_OPENAI_API_KEY"), "base_url": os.environ.get("AZURE_OPENAI_ENDPOINT"), "api_type": "azure",  "api_version": os.environ.get("AZURE_OPENAI_API_VERSION")}]},
)


agent = ConversableAgent(
    "chatbot",
    llm_config={"config_list": [{"model": "gpt-4o", "api_key": os.environ.get("AZURE_OPENAI_API_KEY"), "base_url": os.environ.get("AZURE_OPENAI_ENDPOINT"), "api_type": "azure",  "api_version": os.environ.get("AZURE_OPENAI_API_VERSION")}]},
    code_execution_config=False,  # Turn off code execution, by default it is off.
    function_map=None,  # No registered functions, by default it is None.
    human_input_mode="NEVER",  # Never ask for human input.
)


reply = agent.generate_reply(messages=[{"content": "Tell me a joke.", "role": "user"}])
print(reply)

cathy = ConversableAgent(
    "cathy",
    system_message="Your name is Cathy and you are a part of a duo of comedians.",
    llm_config={"config_list": [{"model": "gpt-4o", "api_key": os.environ.get("AZURE_OPENAI_API_KEY"), "base_url": os.environ.get("AZURE_OPENAI_ENDPOINT"), "api_type": "azure",  "api_version": os.environ.get("AZURE_OPENAI_API_VERSION")}]},
    human_input_mode="NEVER",  # Never ask for human input.
)

joe = ConversableAgent(
    "joe",
    system_message="Your name is Joe and you are a part of a duo of comedians.",
    llm_config={"config_list": [{"model": "gpt-4o", "api_key": os.environ.get("AZURE_OPENAI_API_KEY"), "base_url": os.environ.get("AZURE_OPENAI_ENDPOINT"), "api_type": "azure",  "api_version": os.environ.get("AZURE_OPENAI_API_VERSION")}]},
    human_input_mode="NEVER",  # Never ask for human input.
)

result = joe.initiate_chat(cathy, message="Cathy, tell me a joke.", max_turns=2)