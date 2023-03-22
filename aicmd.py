import os
import subprocess
import argparse
import json
import openai
from check_imports import check_imports

config = None
args = None
key = None  # API key starts with sk-

# if testing, set the following 4 variables including bTesting=True
bTesting = False
macro = "python"
prompt = "hello world"
output = '''import numpy as np
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D

# Generate x, y values for the surface
x = np.linspace(-np.pi, np.pi, 50)
y = np.linspace(-np.pi, np.pi, 50)
X, Y = np.meshgrid(x, y)

# Calculate Z values
Z = np.sin(X) + np.cos(Y)

# Initialize the figure and axis
fig = plt.figure()
ax = fig.add_subplot(111, projection='3d')

# Plot the surface
ax.plot_surface(X, Y, Z)

# Add labels and title
ax.set_xlabel("x")
ax.set_ylabel("y")
ax.set_zlabel("z")
plt.title("z = sin(x) + cos(y)")

# Show the plot
plt.show()'''

# main program
def main():
    global prompt
    global output
    global macro
    global args
    # argument parsing
    parser = argparse.ArgumentParser(description='AI Command Line Tool', epilog='Example:python aicmd.py cmd "list all the .py files"')
    parser.add_argument('macro', type=str, help='The macro to perform (cmd, bash, esp32, python, none etc)')
    parser.add_argument('query', type=str, help='The natural language query')

    if (bTesting is False):
        args = parser.parse_args()
        macro = args.macro

    openai.api_key = os.environ["OPENAI_API_KEY"]
    # Load aicmd.settings.json which is in same directory as aicmd.py
    dir_path = os.path.dirname(os.path.realpath(__file__))
    
    # Build the prompt by expanding the macro stored in aicmd.json
    json_path = os.path.join(dir_path, "aicmd.json")
    if not os.path.exists(json_path):
        print(f"File {json_path} does not exist")
        exit
    with open(json_path, 'r') as f:
        config = json.load(f)
    
    if (bTesting is False):
        openai.api_base = config['settings']['api_endpoint']
        prompt = config['macros'][macro]['cmd'] + args.query
        prompt = prompt.strip()
        if config['macros'][macro]['exec']:
            prompt = prompt + ". Shorter is better and offer no explanation."
    
        response = openai.Completion.create(
            engine="text-davinci-002",
            prompt=prompt,
            max_tokens=1024,
            n=1,
            stop=None,
            temperature=0.5,
        )
        output = response.choices[0].text.strip()

    print(f"Openai.com was asked:\n{prompt}") 
    print(f"Openai.com responded:\n{output}\n") 
    # Execute the command if requested
    exec = config['macros'][macro]['exec']
    if (exec):
        ans = input("Execute (y/n)?")
        if ans == 'y':
            file = None
            try:
                file = config['macros'][macro]['file']
            except:
                pass
            if file is not None:
                print(f"writing file: {file}")
                with open(file, 'w') as f:
                    f.write(output)
                if (macro == "python" and config['macros']['python']['check_imports']):
                    check_imports(file)
                result = subprocess.run([exec, file], capture_output=True)
                print(result.stdout.decode())
            else:
                 os.system(output)

# walk user through setting up OPENAI_APY_KEY
def set_openai_api_key():
    global key
    set_env_var = input("To run aicmd.py, you need to set the environment variable OPENAI_API_KEY. I can help you do that.\nDo you want to permanently set the environment variable OPENAI_API_KEY? (y/n, default=y): ")
    if set_env_var.lower() != "y" and set_env_var != "":
        return
    key = input("Please enter your OpenAI API key (go to https://beta.openai.com/account/api-keys): ")
    # handle differences between Windows and Unix systems
    set_all_users = input("Do you want to set the environment variable OPENAI_API_KEY for all users? (y/n, default=y): ")
    if os.name == 'nt':
        if set_all_users.lower() == "y" or set_all_users == "":
            os.system(f'setx OPENAI_API_KEY "{key}" /M')
        else:
            os.system(f'setx OPENAI_API_KEY "{key}"')
        os.system("cmd /c start cmd")
    else:
        # Untested
        print("Untested on unix")
        if os.geteuid() == 0:
            # running as root, set the environment variable for all users
            with open("/etc/environment", "a") as f:
                f.write(f"\nOPENAI_API_KEY={key}")
            os.environ["OPENAI_API_KEY"] = key
        else:
            # not running as root, set the environment variable for the current user
            with open(os.path.expanduser("~/.bashrc"), "a") as f:
                f.write(f"\nexport OPENAI_API_KEY={key}")
        os.system("sh &")
    print("Use new window with the environment variable OPENAI_API_KEY set")
    exit(0)

if __name__ == '__main__':
    key = os.getenv("OPENAI_API_KEY")
    if key is None or len(key) < 50:
        print(f"Environment variable OPENAI_API_KEY not set!\n")
        set_openai_api_key()
        print(f"OPENAI_API_KEY set to {key}")
    main()
