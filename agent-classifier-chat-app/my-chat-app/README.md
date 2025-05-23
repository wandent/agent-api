# My Chat Application

This project is a text-based chat application that interacts with users and supports markdown responses. It utilizes an agent-based architecture to provide intelligent responses based on user input.

## Project Structure

```
my-chat-app
├── src
│   └── chat_app
│       ├── __init__.py
│       ├── main.py
│       ├── orchestrator.py
│       ├── agent_classifier.py
│       └── ui.py
├── tests
│   ├── test_main.py
│   └── test_agent_classifier.py
├── .env
├── requirements.txt
└── README.md
```

## Features

- **User Interface**: A simple text-only interface that allows users to interact with the application.
- **Markdown Support**: Responses from the agents are formatted in markdown, allowing for rich text display.
- **Agent Selection**: The application intelligently selects the appropriate agent based on user input.
- **Asynchronous Processing**: The application handles user input and agent responses asynchronously for a smooth experience.

## Setup Instructions

1. Clone the repository:
   ```
   git clone <repository-url>
   cd my-chat-app
   ```

2. Create a virtual environment:
   ```
   python -m venv venv
   source venv/bin/activate  # On Windows use `venv\Scripts\activate`
   ```

3. Install the required dependencies:
   ```
   pip install -r requirements.txt
   ```

4. Set up environment variables in the `.env` file as needed.

## Usage

To start the chat application, run the following command:
```
python src/chat_app/main.py
```

Follow the prompts in the terminal to interact with the chat application. Type 'exit' to end the conversation.

## Features
- Leverages agents created on Azure AI Foundy
   - Researcher
   - Prompt Engineer
   - Weather
   - Generic
- Dynamically classifies the agent using the prompt comparing with the agent defintions and utterances on the agents-manifest.json
> Future improvement would be to query the agents based on the keywords to shorten the list, and the resulting json be used as context for the LLM to classify
- Classifies quickly the agent when the agent name is mentioned directly on the prompt preceded of @, like @weather, @researcher or @prompt-engineer
- Chat interface can engage with a given agent, if the user wants to change the subject of the conversation they can type "new chat" to start over
- To exit the application, type exit

## Testing

To run the tests, use the following command:
```
pytest tests/
```

This will execute all unit tests defined in the `tests` directory.

## Contributing

Contributions are welcome! Please open an issue or submit a pull request for any enhancements or bug fixes.

## License

This project is licensed under the MIT License. See the LICENSE file for details.