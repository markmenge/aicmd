# filename: ai.py
# pip install openai
# pip install check_imports
# pip install requests
# pip install keyboard

import os
import argparse
from AICommand import AICommand, APIKeyNotSetupException

def help():
    print("Commands:\nai <text> - Issue natural language query\nx - attempt to execute previous commands.\ncmd <command> - issue a DOS command.\ncd <dir> - change directory.\n")

def main():
    print("AI.py - AI powered command prompt.\n")

    try:
        ai_cmd = AICommand()
    except APIKeyNotSetupException as e:
        print(e)
        return

    while True:
        new_input = input(f"AI {os.getcwd()}>")
        if new_input.strip().lower() == "quit":
            break
        elif new_input.strip().lower() == 'y' or  new_input.strip().lower() == 'x':
            commands = ai_cmd.get_code_blocks(response)
            ai_cmd.execute_commands(commands)
            continue
        elif new_input.startswith('ai '):
            ai_cmd.add_message("user", new_input)            
            response = ai_cmd.session()  # Send the message history, get a new response             
            ai_cmd.add_message("assistant", response)
            print(response)
        elif new_input.startswith("cmd "):
            if len(new_input) < 4:
                ValueError = input("Enter a command:")
            else:
                new_input = new_input[4:]
            ai_cmd.cli_command(new_input)  
        elif (new_input == ''):
            pass         
        else:
            help()

if __name__ == "__main__":
    main()
