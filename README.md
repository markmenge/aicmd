# AI Command Line Interface

This Python script, `ai.py`, allows you to access ChatGPT from the command line in case you can't remember every command line argument.

Before using, set the "api_key" setting in ai.json. Currently you generate a key here: https://beta.openai.com/account/api-keys and 

To run the script, use the following command:

python ai.py [macro] "english description of what you want to do"

Example macros (stored in ai.json):
- 'bash' for Linux and macOS systems command prompts
- 'cmd' for Windows command prompt
- 'esp32' for ESP32 Arduino board code generation
- 'python' for python code
- 'none' for no prompt string other than what you typed
- 
Examples:

py ai.py none "who was picasso?"

py ai.py cmd "List files sorted by size"

py ai.py bash "How much memory does this computer have"

py ai.py python "create a webserver that says hello world, with a button that when you push it says hello to you!"

py ai.py esp32 "have a webserver that says hello and the voltages on the pins. Create the access point named arduino with no password."
