import ast
import os

def generate_function_docs(func_node):
    doc = f"def {func_node.name}({', '.join([a.arg for a in func_node.args.args])}):\\n"
    if func_node.body and isinstance(func_node.body[0], ast.Expr) and isinstance(func_node.body[0].value, ast.Str):
        doc += f"    \\\"\\\"\\\"{func_node.body[0].value.s}\\\"\\\"\\\"\n"
    else:
        doc += f"    \\\"\\\"\\\"TODO: Add function description\\\"\\\"\\\"\n"
    return doc

def generate_class_docs(class_node):
    doc = f"class {class_node.name}:\\n"
    if class_node.body and isinstance(class_node.body[0], ast.Expr) and isinstance(class_node.body[0].value, ast.Str):
        doc += f"    \\\"\\\"\\\"{class_node.body[0].value.s}\\\"\\\"\\\"\n"
    else:
        doc += f"    \\\"\\\"\\\"TODO: Add class description\\\"\\\"\\\"\n"
    return doc

def generate_module_docs(file_path):
    with open(file_path, 'r') as file:
        content = file.read()

    tree = ast.parse(content)
    docs = f"# {os.path.basename(file_path)}\\n\\n"

    for node in ast.iter_child_nodes(tree):
        if isinstance(node, ast.FunctionDef):
            docs += generate_function_docs(node) + "\\n"
        elif isinstance(node, ast.ClassDef):
            docs += generate_class_docs(node) + "\\n"

    return docs

def generate_project_docs(root_dir="."):
    docs = "# Project Documentation\\n\\n"
    for root, dirs, files in os.walk(root_dir):
        for file in files:
            if file.endswith(".py"):
                file_path = os.path.join(root, file)
                docs += generate_module_docs(file_path) + "\\n"
    return docs