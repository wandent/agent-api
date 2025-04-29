import uuid
from rich.console import Console
from rich.markdown import Markdown
import asyncio
import sys
from orchestrator import Orchestrator
from agent_classifier import AgentClassifier

class ChatAppUI:
    def __init__(self):
        self.console = Console()
        self.agent_id = ""
        self.output_log = []
        self.console.print("Output log initialized.", style="bold yellow")

    def display_welcome_message(self):
        self.console.print("Hello, I am your AI assistant. Type 'exit' to end the conversation.", style="bold green")

    def get_user_input(self):
        self.console.print("Type your message:", style="bold magenta")
        message = input("You: ")
        # add to output_log
        self.output_log.append(f"User:{message}")
        return message

    def display_response(self, response):
        markdown_response = response.items[0].text
        # add to output_log
        self.output_log.append(f"Agent:{markdown_response}")
        #markdown_response = Markdown(response, code_theme="monokai")
        self.console.print(markdown_response, style="bold blue")

    async def run_chat(self):
        self.display_welcome_message()
        while True:
            user_input = self.get_user_input()
            if user_input.lower() == "exit":
                print("Goodbye!")
                # dump the output_log to a file with a name that includes the thread id
                with open(f"output_log_{agent_classifier.agent_thread.id}.txt", "w", encoding="utf-8", errors="ignore") as log_file:
                    for entry in self.output_log:
                        entry = entry.encode("utf-8")
                        log_file.write(entry + "\n")
                print("Output log saved successfully.")
                await agent_classifier.agent_thread.delete()
                await orch.orch_thread.delete()
                await orch.client.close()
                await agent_classifier.client.close()
      
                
                
                break
            elif user_input.lower() == "new chat":
                self.agent_id = ""
                await orch.orch_thread.delete()
                await agent_classifier.agent_thread.delete()
                print("New chat started.")
                continue
            elif self.agent_id == "":
                orch = Orchestrator()
                self.agent_id = await orch.orchestrate("./agents-manifest.json", user_input)
                print(f"Selected agent: {self.agent_id}")
                if self.agent_id != "":
                    agent_classifier = AgentClassifier()
                    agent = await agent_classifier.load_agent(self.agent_id)
                    async for content in agent.invoke(messages=[user_input], thread=agent_classifier.agent_thread, max_completion_tokens=4096):
                        self.display_response(content.content)
                    continue
                else:
                    self.display_response("No agent selected. Please try again.")
                    continue
            else:
                # after the agent is selected, we can use the same agent for the rest of the conversation
                async for content in agent.invoke(messages=[user_input], thread=agent_classifier.agent_thread, max_completion_tokens=4096):
                    self.display_response(content.content)
                continue

           

if __name__ == "__main__":
    chat_app = ChatAppUI()
    asyncio.run(chat_app.run_chat())