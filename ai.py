import argparse
import json
import openai
import os


def get_prompt(task):
    """Gets the prompt for the specified task from the config file."""
    with open('ai.json', 'r') as f:
        config = json.load(f)

    return config['prompts'][task]['cmd']


def execute_command(command):
    """Executes the specified command in a new shell process."""
    os.system(command)


def main():
    parser = argparse.ArgumentParser(description='AI Command Line Tool', epilog='Example:python ai.py cmd "list all the .py files"')
    parser.add_argument('task', type=str, help='The task to perform (cmd, bash, esp32, py)')
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
    prompt = get_prompt(args.task) + ' ' + args.query + '. Include no explanation.'

    # Generate the command using OpenAI's GPT-3 API
    response = openai.Completion.create(
        engine="text-davinci-002",
        prompt=prompt,
        max_tokens=128,
        n=1,
        stop=None,
        temperature=0.25,
    )
    print(f"Openin was asked to {prompt}")
    output = response.choices[0].text.strip()
    # Execute the command if requested
    if not args.no_exec and config['prompts'][args.task]['exec']:
        ans = input(f"Openai responds with: {output}\nPress y and <enter> to execute")
        if ans == 'y':
            execute_command(output)
    else:
        print(f"{output}");

if __name__ == '__main__':
    main()
