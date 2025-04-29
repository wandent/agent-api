import unittest
from src.chat_app.main import main
from unittest.mock import patch, MagicMock

class TestMain(unittest.TestCase):

    @patch('builtins.input', side_effect=['Hello', 'exit'])
    @patch('src.chat_app.main.print')
    def test_main_flow(self, mock_print, mock_input):
        main()
        mock_print.assert_any_call("Hello, I am your AI assistant. Type 'exit' to end the conversation.")
        mock_print.assert_any_call("Goodbye!")

    @patch('builtins.input', side_effect=['new chat', 'exit'])
    @patch('src.chat_app.main.print')
    def test_new_chat_flow(self, mock_print, mock_input):
        main()
        mock_print.assert_any_call("New chat started.")
        mock_print.assert_any_call("Goodbye!")

if __name__ == '__main__':
    unittest.main()