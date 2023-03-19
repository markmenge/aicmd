import subprocess
import sys
import os

def install_module(module_name):
    """Install the given module using pip."""
    print(f"Trying to call ")
    cmd = f"python -m pip install {module_name}"
    print(f"Trying to execute:{cmd}")
    result = subprocess.run([cmd], capture_output=True)
    print(result.stdout.decode())
    # subprocess.check_call([sys.executable, "-m", "pip", "install", module_name])

def check_imports(file_path):
    """Analyze the given Python file and prompt to install any missing import modules."""
    with open(file_path, "r") as f:
        code = f.read()

    # Split the code into lines and check each line for import statements
    lines = code.split("\n")
    for line in lines:
        if line.startswith("import "):
            # Extract the module name
            module_name = line.split()[1]
            try:
                # Attempt to import the module
                __import__(module_name)
            except ImportError:
                # The module is not installed
                install_module(module_name)

if __name__ == "__main__":
    file_path = "example.py" # replace with the path to your Python file
    check_imports(file_path)
