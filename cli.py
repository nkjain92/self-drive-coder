import readline
import os
from utils import print_colored, USER_COLOR, CLAUDE_COLOR, TOOL_COLOR, RESULT_COLOR, Style
from code_execution import safe_execute_code
from package_management import update_requirements, install_packages
from context_analysis import get_context_suggestions
from doc_generation import generate_project_docs

class CLI:
    def __init__(self, ai_interface, project_state, system_prompt, tools):
        self.ai_interface = ai_interface
        self.project_state = project_state
        self.system_prompt = system_prompt
        self.tools = tools
        self.commands = {
            "/save": self.save_state,
            "/load": self.load_state,
            "/switch_model": self.switch_model,
            "/help": self.show_help,
            "/execute": self.execute_code,
            "/update_requirements": self.update_requirements,
            "/install_packages": self.install_packages,
            "/analyze": self.analyze_context,
            "/generate_docs": self.generate_docs
        }
        self.setup_autocomplete()

    def setup_autocomplete(self):
        readline.set_completer(self.autocomplete)
        readline.parse_and_bind("tab: complete")

    def autocomplete(self, text, state):
        options = [cmd for cmd in self.commands.keys() if cmd.startswith(text)]
        if state < len(options):
            return options[state]
        else:
            return None

    def save_state(self):
        self.project_state.save()
        print_colored("Project state saved.", RESULT_COLOR)

    def load_state(self):
        self.project_state.load()
        print_colored("Project state loaded.", RESULT_COLOR)

    def switch_model(self):
        # Implement model switching logic
        pass

    def show_help(self):
        help_text = "\n".join([f"{cmd}: {func.__doc__}" for cmd, func in self.commands.items()])
        print_colored(help_text, RESULT_COLOR)

    def execute_code(self):
        code = input("Enter Python code to execute: ")
        output, error = safe_execute_code(code)
        if output:
            print_colored(f"Output:\n{output}", RESULT_COLOR)
        if error:
            print_colored(f"Error:\n{error}", TOOL_COLOR)

    def update_requirements(self):
        file_path = input("Enter the path of the Python file to analyze: ")
        with open(file_path, 'r') as file:
            content = file.read()
        result = update_requirements(content)
        print_colored(result, RESULT_COLOR)

    def install_packages(self):
        result = install_packages()
        print_colored(result, RESULT_COLOR)

    def analyze_context(self):
        current_file = input("Enter the path of the current file: ")
        suggestions = get_context_suggestions(self.project_state.file_structure, current_file)
        for suggestion in suggestions:
            print_colored(suggestion, RESULT_COLOR)

    def generate_docs(self):
        docs = generate_project_docs()
        print_colored(docs, RESULT_COLOR)
        with open("project_documentation.md", "w") as f:
            f.write(docs)
        print_colored("Documentation saved to project_documentation.md", RESULT_COLOR)

    def run(self):
        while True:
            user_input = input(f"\n{USER_COLOR}You: {Style.RESET_ALL}")
            if user_input.lower() == 'exit':
                print_colored("Thank you for using the AI Coding Assistant. Goodbye!", CLAUDE_COLOR)
                break

            if user_input.startswith("/"):
                command = user_input.split()[0]
                if command in self.commands:
                    self.commands[command]()
                else:
                    print_colored(f"Unknown command: {command}. Type /help for a list of commands.", RESULT_COLOR)
            else:
                response = self.ai_interface.chat(user_input, self.project_state.conversation_history, self.system_prompt, self.tools)
                print_colored(f"\nAI: {response}", CLAUDE_COLOR)
                self.project_state.add_to_history({"role": "user", "content": user_input})
                self.project_state.add_to_history({"role": "assistant", "content": response})

            self.project_state.update_file_structure()