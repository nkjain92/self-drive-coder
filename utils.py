from colorama import init, Fore, Style

# Initialize colorama
init()

# Color constants
USER_COLOR = Fore.WHITE
CLAUDE_COLOR = Fore.BLUE
GPT_COLOR = Fore.GREEN
TOOL_COLOR = Fore.YELLOW
RESULT_COLOR = Fore.CYAN

def print_colored(text, color):
    print(f"{color}{text}{Style.RESET_ALL}")

def format_code(code, language):
    # Implement code formatting logic here if needed
    # For now, we'll just return the code as is
    return code