import os
import ast

def analyze_project_structure(root_dir="."):
    structure = {}
    for root, dirs, files in os.walk(root_dir):
        structure[root] = {"dirs": dirs, "files": files}
    return structure

def analyze_file_content(file_path):
    with open(file_path, 'r') as file:
        content = file.read()

    tree = ast.parse(content)
    functions = [node.name for node in ast.walk(tree) if isinstance(node, ast.FunctionDef)]
    classes = [node.name for node in ast.walk(tree) if isinstance(node, ast.ClassDef)]
    imports = [node.names[0].name for node in ast.walk(tree) if isinstance(node, ast.Import)]
    imports.extend([node.module for node in ast.walk(tree) if isinstance(node, ast.ImportFrom)])

    return {
        "functions": functions,
        "classes": classes,
        "imports": imports
    }

def get_context_suggestions(project_structure, current_file):
    suggestions = []
    file_analysis = analyze_file_content(current_file)

    suggestions.append(f"Current file contains {len(file_analysis['functions'])} functions and {len(file_analysis['classes'])} classes.")
    suggestions.append(f"Imported modules: {', '.join(file_analysis['imports'])}")

    return suggestions