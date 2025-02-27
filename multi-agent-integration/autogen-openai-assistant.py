import os

from autogen import config_list_from_json
from autogen.agentchat.contrib.gpt_assistant_agent import GPTAssistantAgent
from dotenv import load_dotenv
from dotenv import find_dotenv

load_dotenv(find_dotenv())

assistant_id = os.environ.get("ASSISTANT_ID", None)
config_list = config_list_from_json("azure_oaai.json")
llm_config = {
    "config_list": config_list,
}
assistant_config = {
    # define the openai assistant behavior as you need
}
oai_agent = GPTAssistantAgent(
    name="oai_agent",
    instructions="I'm an openai assistant running in autogen",
    llm_config=llm_config,
    assistant_config=assistant_config,
)