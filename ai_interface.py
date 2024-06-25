import os
from abc import ABC, abstractmethod
from anthropic import Anthropic, AnthropicError
from openai import OpenAI
from tavily import TavilyClient
from utils import print_colored, CLAUDE_COLOR, GPT_COLOR
from file_operations import create_folder, create_file, write_to_file, list_files

class AIModel(ABC):
    @abstractmethod
    def chat(self, messages, system_prompt, tools):
        pass

class ClaudeModel(AIModel):
    def __init__(self):
        api_key = os.getenv("ANTHROPIC_API_KEY")
        if not api_key:
            raise ValueError("ANTHROPIC_API_KEY not found in environment variables")
        print(f"Initializing Anthropic client with API Key: {api_key[:10]}...{api_key[-5:]}")
        self.client = Anthropic(api_key=api_key)
        print("Anthropic client initialized successfully")
        self.tavily_client = TavilyClient(api_key=os.getenv("TAVILY_API_KEY"))

    def chat(self, messages, system_prompt, tools):
        try:
            params = {
                "model": "claude-3-opus-20240229",
                "max_tokens": 4000,
                "messages": messages,
            }
            if system_prompt:
                params["system"] = system_prompt
            if tools:
                params["tools"] = tools
                params["tool_choice"] = {"type": "auto"}

            response = self.client.messages.create(**params)
            return response
        except AnthropicError as e:
            print(f"AnthropicError: {str(e)}")
            return None

class GPT4Model(AIModel):
    def __init__(self):
        self.client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))
        self.tavily_client = TavilyClient(api_key=os.getenv("TAVILY_API_KEY"))

    def chat(self, messages, system_prompt, tools):
        # Implement GPT-4 chat method
        # Note: This is a placeholder and needs to be implemented based on OpenAI's API
        pass

class AIInterface:
    def __init__(self, model_name):
        self.model = self._get_model(model_name)

    def _get_model(self, model_name):
        if model_name == "claude":
            return ClaudeModel()
        elif model_name == "gpt4":
            return GPT4Model()
        else:
            raise ValueError(f"Unsupported model: {model_name}")

    def chat(self, user_input, conversation_history, system_prompt, tools):
        # Filter out any empty messages from the conversation history
        filtered_history = [msg for msg in conversation_history if msg.get('content')]

        # Add the new user input
        messages = filtered_history + [{"role": "user", "content": user_input}]

        response = self.model.chat(messages, system_prompt, tools)

        if response is None:
            return "Sorry, there was an error processing your request."

        # Process and return the response
        if isinstance(self.model, ClaudeModel):
            return self.process_claude_response(response)
        elif isinstance(self.model, GPT4Model):
            # Handle GPT-4's response format (placeholder)
            return response
        else:
            return str(response)  # Fallback for unknown model types

    def process_claude_response(self, response):
        result = ""
        for content_block in response.content:
            if content_block.type == "text":
                result += content_block.text
                print_colored(f"\nClaude: {content_block.text}", CLAUDE_COLOR)
            elif content_block.type == "tool_calls":
                for tool_call in content_block.tool_calls:
                    tool_result = self.execute_tool(tool_call.function.name, tool_call.function.arguments)
                    result += f"\nTool result: {tool_result}"
                    print_colored(f"\nTool result: {tool_result}", CLAUDE_COLOR)
        return result

    def execute_tool(self, tool_name, tool_arguments):
        if tool_name == "create_folder":
            return create_folder(tool_arguments["path"])
        elif tool_name == "create_file":
            return create_file(tool_arguments["path"], tool_arguments.get("content", ""))
        elif tool_name == "write_to_file":
            return write_to_file(tool_arguments["path"], tool_arguments["content"])
        elif tool_name == "list_files":
            return list_files(tool_arguments.get("path", "."))
        else:
            return f"Unknown tool: {tool_name}"