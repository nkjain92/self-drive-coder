import subprocess
import sys
import tempfile
import os

def execute_code(code):
    with tempfile.NamedTemporaryFile(mode='w', suffix='.py', delete=False) as temp_file:
        temp_file.write(code)
        temp_file_path = temp_file.name

    try:
        result = subprocess.run([sys.executable, temp_file_path],
                                capture_output=True, text=True, timeout=10)
        output = result.stdout
        error = result.stderr
    except subprocess.TimeoutExpired:
        output = ""
        error = "Execution timed out after 10 seconds."
    finally:
        os.unlink(temp_file_path)

    return output, error

def safe_execute_code(code):
    # Add any additional security measures here
    return execute_code(code)