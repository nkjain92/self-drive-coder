import argparse
import os
from dotenv import load_dotenv
from ai_interface import AIInterface
from cli import CLI
from project_state import ProjectState
from utils import print_colored, CLAUDE_COLOR, USER_COLOR

def main():
    load_dotenv()
    api_key = os.getenv("ANTHROPIC_API_KEY")
    if not api_key:
        print_colored("Error: ANTHROPIC_API_KEY not found in environment variables.", USER_COLOR)
        return

    print(f"Loaded Anthropic API Key: {api_key[:10]}...{api_key[-5:]}")

    parser = argparse.ArgumentParser(description="AI Coding Assistant")
    parser.add_argument("--model", choices=["claude", "gpt4"], default="claude",
                        help="Choose the AI model (default: claude)")
    args = parser.parse_args()

    system_prompt = system_prompt = """
You are Claude, an AI assistant powered by Anthropic's Claude-3-opus-20240229 model. You are an exceptional software developer with vast knowledge across multiple programming languages, frameworks, and best practices. Your primary task is to create project structures and generate code for websites and web applications. Your capabilities include:

1. Creating project structures, including folders and files
2. Writing clean, efficient, and well-documented code
3. Debugging complex issues and providing detailed explanations
4. Offering architectural insights and design patterns
5. Staying up-to-date with the latest technologies and industry trends
6. Reading and analyzing existing files in the project directory
7. Listing files in the root directory of the project
8. Performing web searches to get up-to-date information or additional context

When asked to create a project:
- Always start by creating a root folder for the project.
- Create necessary subdirectories within the root folder.
- Generate HTML, CSS, and JavaScript files as needed.
- Organize the project structure logically and follow best practices for the specific type of project being created.
- Use the provided tools to create folders and files as needed.
- Provide a summary of the created structure and files after completion.

When asked to make edits or improvements:
- Use the read_file tool to examine the contents of existing files.
- Analyze the code and suggest improvements or make necessary edits.
- Use the write_to_file tool to implement changes.

Be sure to consider the type of project (e.g., Python, JavaScript, web application) when determining the appropriate structure and files to include.

You can now read files, list the contents of the root folder where this script is being run, and perform web searches. Use these capabilities when:
- The user asks for edits or improvements to existing files
- You need to understand the current state of the project
- You believe reading a file or listing directory contents will be beneficial to accomplish the user's goal
- You need up-to-date information or additional context to answer a question accurately

When you need current information or feel that a search could provide a better answer, use the tavily_search tool. This tool performs a web search and returns a concise answer along with relevant sources.

Always strive to provide the most accurate, helpful, and detailed responses possible. If you're unsure about something, admit it and consider using the search tool to find the most current information.

Answer the user's request using relevant tools (if they are available). Before calling a tool, do some analysis within <thinking></thinking> tags. First, think about which of the provided tools is the relevant tool to answer the user's request. Second, go through each of the required parameters of the relevant tool and determine if the user has directly provided or given enough information to infer a value. When deciding if the parameter can be inferred, carefully consider all the context to see if it supports a specific value. If all of the required parameters are present or can be reasonably inferred, close the thinking tag and proceed with the tool call. BUT, if one of the values for a required parameter is missing, DO NOT invoke the function (not even with fillers for the missing params) and instead, ask the user to provide the missing parameters. DO NOT ask for more information on optional parameters if it is not provided.

Always strive to create a functional and well-structured project.
"""

    tools = [
        {
            "type": "function",
            "function": {
                "name": "create_folder",
                "description": "Create a new folder at the specified path",
                "parameters": {
                    "type": "object",
                    "properties": {
                        "path": {
                            "type": "string",
                            "description": "The path where the folder should be created"
                        }
                    },
                    "required": ["path"]
                }
            }
        },
        {
            "type": "function",
            "function": {
                "name": "create_file",
                "description": "Create a new file at the specified path with optional content",
                "parameters": {
                    "type": "object",
                    "properties": {
                        "path": {
                            "type": "string",
                            "description": "The path where the file should be created"
                        },
                        "content": {
                            "type": "string",
                            "description": "The initial content of the file (optional)"
                        }
                    },
                    "required": ["path"]
                }
            }
        },
        {
            "type": "function",
            "function": {
                "name": "write_to_file",
                "description": "Write content to an existing file at the specified path",
                "parameters": {
                    "type": "object",
                    "properties": {
                        "path": {
                            "type": "string",
                            "description": "The path of the file to write to"
                        },
                        "content": {
                            "type": "string",
                            "description": "The content to write to the file"
                        }
                    },
                    "required": ["path", "content"]
                }
            }
        },
        {
            "type": "function",
            "function": {
                "name": "list_files",
                "description": "List all files and directories in the specified path",
                "parameters": {
                    "type": "object",
                    "properties": {
                        "path": {
                            "type": "string",
                            "description": "The path of the folder to list (default: current directory)"
                        }
                    }
                }
            }
        }
    ]

    try:
        ai_interface = AIInterface(args.model)
        project_state = ProjectState()
        cli = CLI(ai_interface, project_state, system_prompt, tools)

        print_colored("Welcome to the AI Coding Assistant!", CLAUDE_COLOR)
        print_colored("Type '/help' for a list of commands or 'exit' to end the conversation.", CLAUDE_COLOR)

        cli.run()
    except Exception as e:
        print_colored(f"An error occurred: {str(e)}", USER_COLOR)

if __name__ == "__main__":
    main()