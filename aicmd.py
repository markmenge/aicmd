import argparse
import json
import openai
import os

config = None

def execute_command(command):
    """Executes the specified command in a new shell process."""
    os.system(command)

def main():
    parser = argparse.ArgumentParser(description='AI Command Line Tool', epilog='Example:python aicmd.py cmd "list all the .py files"')
    parser.add_argument('macro', type=str, help='The macro to perform (cmd, bash, esp32, python, none)')
    parser.add_argument('query', type=str, help='The natural language query')
    parser.add_argument('--no-exec', dest='no_exec', action='store_true',
                        help='Do not execute the command after generating it')
    # parser.epilog('Example: python aicmd.py cmd list all the .py files')
    args = parser.parse_args()

    dir_path = os.path.dirname(os.path.realpath(__file__))
    settings_path = os.path.join(dir_path, "aicmd.settings.json")
    if not os.path.exists(settings_path):
        print(f"File {settings_path} does not exist, please run setup.py")
        exit
    with open(settings_path, 'r') as f:
        settings = json.load(f)
    openai.api_key = settings['api_key']
    openai.api_base = settings['api_endpoint']

    # Build the prompt
    json_path = os.path.join(dir_path, "aicmd.json")
    if not os.path.exists(json_path):
        print(f"File {json_path} does not exist")
        exit
    with open(json_path, 'r') as f:
        config = json.load(f)
    prompt = config['macros'][args.macro]['cmd'] + args.query
    prompt = prompt.strip()
    if config['macros'][args.macro]['exec']:
        prompt = prompt + " Shorter is better and offer no explanation."
    
    # Generate the response using OpenAI's GPT-3 API
    response = openai.Completion.create(
        engine="text-davinci-002",
        prompt=prompt,
        max_tokens=1024,
        n=1,
        stop=None,
        temperature=0.5,
    )
    output = response.choices[0].text.strip()

    # output = 'dir /s'
    print(f"Openai.com was asked:\n{prompt}") 
    print(f"Openai.com responded:\n{output}\n")
    
    # Execute the command if requested
    if not args.no_exec and config['macros'][args.macro]['exec']:
        ans = input("Execute this command (y/n)?")
        if ans == 'y':
            file = None
            try:
                file = config['macros'][args.macro]['file']
            except:
                pass
            if file is not None:
                with open(file, 'w') as f:
                    f.write(output)
                execute_command(file)
            else:
                execute_command(output)

if __name__ == '__main__':
    main()
