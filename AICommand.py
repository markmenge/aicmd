# filename: AICommand.py
# pip install openai
# pip install requests
# pip install keyboard

import os
import openai
import subprocess

class APIKeyNotSetupException(Exception):
    pass

class AICommand:
    def __init__(self):
        self.api_key = self.setup_openai_api_key()
        if not self.api_key:
            raise APIKeyNotSetupException("OpenAI API key was not set up correctly.")
        self.messages = []

    def setup_openai_api_key(self):
        key = os.getenv("OPENAI_API_KEY")
        if key and len(key) >= 50:
            return key
        
        set_env_var = input("To run aicmd.py, you need to set the environment variable OPENAI_API_KEY. I can help you do that.\nDo you want to permanently set the environment variable OPENAI_API_KEY? (y/n, default=y): ")
        if set_env_var.lower() != "y" and set_env_var != "":
            return None
        
        key = input("Please enter your OpenAI API key (go to https://beta.openai.com/account/api-keys): ")
        
        # Handle differences between Windows and Unix systems
        set_all_users = input("Do you want to set the environment variable OPENAI_API_KEY for all users? (y/n, default=y): ")
        if os.name == 'nt':
            if set_all_users.lower() == "y" or set_all_users == "":
                os.system(f'setx OPENAI_API_KEY "{key}" /M')
            else:
                os.system(f'setx OPENAI_API_KEY "{key}"')
            os.system("cmd /c start cmd")
        else:
            # Untested
            print("Untested on Unix")
            if os.geteuid() == 0:
                # Running as root, set the environment variable for all users
                with open("/etc/environment", "a") as f:
                    f.write(f"\nOPENAI_API_KEY={key}")
                os.environ["OPENAI_API_KEY"] = key
            else:
                # Not running as root, set the environment variable for the current user
                with open(os.path.expanduser("~/.bashrc"), "a") as f:
                    f.write(f"\nexport OPENAI_API_KEY={key}")
            os.system("sh &")
        
        print("Use a new window with the environment variable OPENAI_API_KEY set")
        return key

    def cleanup_cmd(self, output):
        output = output.replace('```bash', '').replace('```', '').strip()
        return output

    def get_code_blocks(self, output):
        code_blocks = []
        # Extract code blocks delimited by ```
        while True:
            code_block_start = output.find("```")
            if code_block_start != -1:
                code_block_end = output.find("```", code_block_start + 3)
                if code_block_end != -1:
                    # Append the code block content to code_blocks list
                    lines = output[code_block_start + 3:code_block_end].strip()
                    code_blocks = code_blocks + lines.split('\n')
                    # code_blocks.append(code_blocks_tmp)
                    # Update the output to remove the processed code block
                    output = output[code_block_end + 3:]
                else:
                    break
            else:
                break
        # Handle the case where there is no matching end delimiter for the code block
        # or if there are no code blocks
        if not code_blocks:
            lines = output.strip().split('\n')
            code_blocks = [line.strip() for line in lines if line.strip()]
        return code_blocks

    def add_prompt(self, prompt):
        self.messages.append({"role": "user", "content": prompt})

    def add_message(self, role, message):
        self.messages.append({"role": role, "content": message})
        self._trim_messages()

    def _trim_messages(self):
        total_tokens = sum(len(message["content"].split()) for message in self.messages)
        while total_tokens > 15000:  # Trim to keep a safe margin
            self.messages.pop(0)
            total_tokens = sum(len(message["content"].split()) for message in self.messages)

    def session(self):
        response = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",
            messages=self.messages,
            max_tokens=1024,
            n=1,
            stop=None,
            temperature=0.5,
        )
        return response.choices[0]['message']['content']

    def execute(self, cmd):
        outputs = []
        current_directory = os.getcwd()  # Track the current directory
        try:
            if cmd.startswith("cd "):
                new_directory = cmd.split("cd ", 1)[1].strip()
                os.chdir(new_directory)  # Change directory
                current_directory = os.getcwd()  # Update the current directory
                outputs.append((f"Changed directory to {current_directory}", ""))
            else:
                result = subprocess.run(cmd, shell=True, capture_output=True, text=True, cwd=current_directory)  # Execute command
                outputs.append((result.stdout, result.stderr))
        except Exception as e:
            outputs.append(("", f"Error: {e}"))

        return outputs

    def execute_commands(self, commands):
        of_str = ''
        for i, command in enumerate(commands, start=1):
            if len(commands) > 1:
                of_str = f"({i} of {len(commands)}) "
            choice = input(f"AICMD {os.getcwd()}>\n{of_str}AICmd wants to execute: {command}\nExecute (y/n/N/cmd)?")
            if choice.lower() == 'y':
                outputs = self.execute(command)  # Execute the command
                for stdout, stderr in outputs:
                    print(f"{stdout} {stderr}")
                    self.add_message("system", f"{stdout}{stderr}")
            elif choice.startswith("cmd "):
                if len(choice) < 4:
                    choice = input("Enter a command:")
                else:
                    choice[4:] = choice
                self.cli_command(choice)
                           
            elif choice == 'N':
                print("Aborting all further commands.")
                break
            else:
                print("Command skipped.")
    
    def cli_command(self, cmd):
        outputs = self.execute(cmd)  # Execute the command
        for stdout, stderr in outputs:
            print(f"{stdout} {stderr}")
            self.add_message("system", f"{stdout}{stderr}")
