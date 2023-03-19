import subprocess
import argparse
import json
import openai
import os

config = None
args = None
key = None  # API key starts with sk-

# if testing, set the following 4 variables including bTesting=True
bTesting = True
macro = "python"
prompt = "hello world"
output = "print('hello world')"

# main program
def main():
    global prompt
    global output
    global macro
    # argument parsing
    parser = argparse.ArgumentParser(description='AI Command Line Tool', epilog='Example:python aicmd.py cmd "list all the .py files"')
    parser.add_argument('macro', type=str, help='The macro to perform (cmd, bash, esp32, python, none)')
    parser.add_argument('query', type=str, help='The natural language query')
    parser.add_argument('--no-exec', dest='no_exec', action='store_true',
                        help='Do not execute the command after generating it')
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
        openai.api_base = config['api_endpoint']
        prompt = config['macros'][args.macro]['cmd'] + args.query
        prompt = prompt.strip()
        if config['macros'][args.macro]['exec']:
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
    if (bTesting or not args.no_exec) and exec:
        ans = input("Execute this command (y/n)?")
        if ans == 'y':
            file = None
            try:
                file = config['macros'][macro]['file']
            except:
                pass
            if file is not None:
				print(f"Writing file:{file}")
                with open(file, 'w') as f:
                    f.write(output)
                result = subprocess.run([exec, file], capture_output=True)
                print(result.stdout.decode())
            else:
                result = subprocess.run([exec, output], capture_output=True)
                print(result.stdout.decode())

# walk user through setting up OPENAI_APY_KEY
def set_openai_api_key():
    global key
    set_env_var = input("To run aicmd.py, you need to set the environment variable OPENAI_API_KEY. I can help you do that.\nDo you want to permanently set the environment variable OPENAI_API_KEY? (y/n, default=y): ")
    if set_env_var.lower() != "y" and set_env_var != "":
        return
    key = input("Please enter your OpenAI API key: ")
    # handle differences between Windows and Unix systems
    set_all_users = input("Do you want to set the environment variable OPENAI_API_KEY for all users? (y/n, default=y): ")
    if os.name == 'nt':
        if set_all_users.lower() == "y" or set_all_users == "":
            os.system(f'setx OPENAI_API_KEY "{key}" /M')
        else:
            os.system(f'setx OPENAI_API_KEY "{key}"')
            os.environ["OPENAI_API_KEY"] = key
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
            os.environ["OPENAI_API_KEY"] = key

if __name__ == '__main__':
    key = os.getenv("OPENAI_API_KEY")
    if key is None or len(key) < 50:
        set_openai_api_key()
        print(f"OPENAI_API_KEY set to {key}")
    main()
