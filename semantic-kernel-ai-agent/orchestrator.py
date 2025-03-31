
import json
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


async def load_agent(agent_id):
    agent_definition = await client.agents.get_agent(agent_id)
    agent = AzureAIAgent(client=client,
                        definition=agent_definition)
    return agent


async def load_thread():
    thread: AzureAIAgentThread = AzureAIAgentThread(client=client)
    thread = AzureAIAgentThread(client=client)
    return thread 

# Create a function to load the agent-manifest.json and ask chatgpt which agent to use
async def orchestrator(thread,  manifest_path, input_text):
    with open(manifest_path, 'r') as file:
        manifest = file.read()
        # convert manifest from json document into a string
        manifest = json.dumps(json.loads(manifest), indent=4)


        prompt = f"Please choose an agent from the following manifest:\n{manifest}\n\nWhich agent would you like to use in order that meet the following input text: {input_text}. You should choose the agent based on the input text closeness with the utterances depicted on the manifest.\n\n Return just the information on the agent_id field." 
        # Here you would call your AI model to get the response
        # For example, using OpenAI's API or any other AI service
        generic_agent = await client.agents.get_agent("asst_rYEZZ8EHgoNtsjdZWXS9sBKb")
        agent = AzureAIAgent(client=client,
                        definition=generic_agent)
        async for content in agent.invoke(messages=prompt, thread=thread):
                print(f"AI: {content.content}")
                thread = content.thread
   
    
    response =content.content
    return response

async def main():
    try:
       # request the user input in loop until the user types "exit"
        
        print("Hello, I am your AI assistant. Type 'exit' to end the conversation.")
        agent_id =  ""
        while True:
            user_input = input("You: ")
            # if it's the first iteration, load the agent and thread
            if agent_id == "":
                thread = await load_thread()
                agent_id = await orchestrator(thread, "./agents/agents-manifest.json", user_input)
                print(f"New thread: {thread.id}")
                print(f"Selected agent: {agent_id}")
            if user_input.lower() == "exit":
                    #await thread.delete() if thread else None
                    await client.close()
                    print("Goodbye!")
                    break
           
            # close the thread if the user types "new chat"
            elif user_input.lower() == "new chat":
                thread = await exit
                load_thread()
                agent_id = ""
                print("New chat started.")
                continue
            else:
                # load the agent based on the agent_id
                agent = await load_agent(agent_id)
                async for content in agent.invoke(messages=user_input, thread=thread):
                    print(f"AI: {content.content}")
                    thread = content.thread
            
           
    finally:
        await client.close()
        #await thread.delete() if thread else None


# call the main function
if __name__ == "__main__":
    asyncio.run(main())

