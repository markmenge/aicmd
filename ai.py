import argparse
import json
import openai
import os


def get_prompt(task):
    """Gets the prompt for the specified task from the config file."""
    with open('ai.json', 'r') as f:
        config = json.load(f)

    return config['macros'][task]['cmd']


def execute_command(command):
    """Executes the specified command in a new shell process."""
    os.system(command)


def main():
    parser = argparse.ArgumentParser(description='AI Command Line Tool', epilog='Example:python ai.py cmd "list all the .py files"')
    parser.add_argument('macro', type=str, help='The macro to perform (cmd, bash, esp32, python, none)')
    parser.add_argument('query', type=str, help='The natural language query')
    parser.add_argument('--no-exec', dest='no_exec', action='store_true',
                        help='Do not execute the command after generating it')
    # parser.epilog('Example: python ai.py cmd list all the .py files')
    args = parser.parse_args()

    # Configure the OpenAI API client
    with open('ai.json', 'r') as f:
        config = json.load(f)

    openai.api_key = config['settings']['api_key']
    openai.api_base = config['settings']['api_endpoint']

    # Build the prompt
    prompt = get_prompt(args.macro) + ' ' + args.query

    # Generate the command using OpenAI's GPT-3 API
    
    response = openai.Completion.create(
        engine="text-davinci-002",
        prompt=prompt,
        max_tokens=128,
        n=1,
        stop=None,
        temperature=0.25,
    )
    output = response.choices[0].text.strip()
    
    # output = 'dir /s'
    print(f"Openai.com was asked to:\n{prompt}") 
    print(f"Openai.com responds with:\n{output}\n")
    
    
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
