
import json
import asyncio
import os
from azure.identity import DefaultAzureCredential
from semantic_kernel import Kernel
from semantic_kernel.agents import AzureAIAgent, AzureAIAgentThread
from dotenv import load_dotenv, find_dotenv

load_dotenv(find_dotenv())  # Load environment variables from .env file
kernel = Kernel()
creds = DefaultAzureCredential()
client = AzureAIAgent.create_client(credential=creds, conn_str=os.getenv("AZURE_AI_AGENT_PROJECT_CONNECTION_STRING"))
thread = None
agent_thread = None

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
        thread: AzureAIAgentThread = AzureAIAgentThread(client=client)
        manifest = file.read()
        # convert manifest from json document into a string
        manifest = json.dumps(json.loads(manifest), indent=4)


        # if the request directs to a specific agent, then return the agent_id of the agent
        # check if the name of the agent is mentioned in the prompt preceded by "@", like @waether or @researcher or @prompt-engineer
        # if the name is mentioned, then return the agent_id of the agent
        if "@" in input_text:
            agent_name = input_text.split("@")[1].split(" ")[0]
            # iterate over the manifest records and check if the agent_name is in the manifest, return the agent_id of the agent
            manifest_data = json.loads(manifest)
            agents = manifest_data.get('agents', [])

        # Search for the agent in the manifest
            for agent in agents:
                if agent['agent-name'] == agent_name:
                    return agent['agent_id']
                    


        prompt = f"Please choose an agent from the following manifest:\n{manifest}\n\nWhich agent would you like to use in order that meet the following input text: {input_text}. You should choose the agent based on the input text closeness with the utterances depicted on the manifest.\n\n Return just the information on the agent_id field." 
        generic_agent = await client.agents.get_agent(os.getenv("AI_ASSISTANT_GENERIC"))
        agent = AzureAIAgent(client=client,
                        definition=generic_agent)
        async for content in agent.invoke(messages=prompt, thread=thread):
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
                # set agent_thread to None
                thread = None
                agent_thread = None
                agent_id = await orchestrator(thread, "./agents/agents-manifest.json", user_input)
                print(f"Selected agent: {agent_id}")
            if user_input.lower() == "exit":
                    await thread.delete() if thread else None
                    await agent_thread.delete() if agent_thread else None
                    await client.close()
                    print("Goodbye!")
                    break
           
            # close the thread if the user types "new chat"
            if user_input.lower() == "new chat":
                await thread.delete() if thread else None
                await agent_thread.delete() if agent_thread else None
                agent_id = ""
                print("New chat started.")
                continue
            else:
                try:
                    # load the agent based on the agent_id
                    agent = await load_agent(agent_id)
                    if agent_thread is None:
                        agent_thread: AzureAIAgentThread = AzureAIAgentThread(client=client)
                    async for content in agent.invoke(messages=[user_input], thread=agent_thread, max_completion_tokens=4096):
                            print(f"AI: {content.content}")
                            print(f"Thread ID: {agent_thread.id}")
                        
                
                # report the error
                except Exception as e:
                    print(f"Error: {e}")
                    print("Error in the request, my responses are limited. Please try again.")
                    # diplay the thread content for debugging purposes
                    #async for content in thread.get_messages(sort_order="desc"):
                    #    print(f"Thread message: {content.content}")
                    continue
                finally:
                    pass
      
    finally:
        await client.close()
        await thread.delete() if thread else None
        await agent_thread.delete() if agent_thread else None



# call the main function
if __name__ == "__main__":
    asyncio.run(main())

