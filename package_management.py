import subprocess
import re
from importlib.metadata import distributions

def update_requirements(file_content):
    imports = re.findall(r'^import\s+(\w+)|^from\s+(\w+)', file_content, re.MULTILINE)
    packages = set(import_name for group in imports for import_name in group if import_name)

    installed_packages = {dist.metadata['Name'].lower() for dist in distributions()}
    new_packages = packages - installed_packages

    if new_packages:
        with open('requirements.txt', 'a') as req_file:
            for package in new_packages:
                req_file.write(f"{package}\\n")
        return f"Added {', '.join(new_packages)} to requirements.txt"
    return "No new packages to add."

def install_packages():
    try:
        subprocess.run(["pip", "install", "-r", "requirements.txt"], check=True)
        return "Packages installed successfully."
    except subprocess.CalledProcessError as e:
        return f"Error installing packages: {str(e)}"