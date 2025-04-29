from rich.console import Console
from rich.markdown import Markdown
import asyncio
import sys
from orchestrator import orchestrator
from agent_classifier import AgentClassifier

class ChatAppUI:
    def __init__(self):
        self.console = Console()
        self.agent_id = ""

    def display_welcome_message(self):
        self.console.print("Hello, I am your AI assistant. Type 'exit' to end the conversation.", style="bold green")

    def get_user_input(self):
        return input("You: ")

    def display_response(self, response):
        markdown_response = response.items[0].text
        #markdown_response = Markdown(response, code_theme="monokai")
        self.console.print(markdown_response)

    async def run_chat(self):
        self.display_welcome_message()
        while True:
            user_input = self.get_user_input()
            if user_input.lower() == "exit":
                self.console.print("Goodbye!", style="bold red")
                break

            if self.agent_id == "":
                self.agent_id = await orchestrator("./agents-manifest.json", user_input)
                self.console.print(f"Selected agent: {self.agent_id}")

            agent = await AgentClassifier.load_agent(self.agent_id)
            response = await agent.invoke(messages=[user_input])
            #self.display_response(response)
            if response.status == "failed":
                self.console.print(f"Error: {response.last_error}", style="bold red")
                self.console.print("Error in the request, my responses are limited. Please try again.", style="bold yellow")
            else:
                self.display_response(response)


            

if __name__ == "__main__":
    chat_app = ChatAppUI()
    asyncio.run(chat_app.run_chat())