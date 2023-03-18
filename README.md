# AI Command Line Interface

This Python script, `aicmd.py`, allows you to access ChatGPT from the command line!

Before using, set the "api_key" setting in ai.json. Currently you generate a key here: https://beta.openai.com/account/api-keys

To run the script, use the following command:

python aicmd.py [macro] "english description of what you want to do"

Example macros (stored in ai.json):
- 'bash' for Linux and macOS systems command prompts
- 'cmd' for Windows command prompt
- 'esp32' for ESP32 Arduino board code generation
- 'python' for python code
- 'none' for no prompt string other than what you typed
- 
Examples:

py aicmd.py none "who was picasso?"

python aicmd.py cmd "List files sorted by size"
python aicmd.py bash "How much memory does this computer have"
python aicmd.py python "create a webserver that says hello world, with a button that when you push it says hello to you!"
python aicmd.py esp32 "create a webserver that says hello and the voltages on the pins. Create the access point named arduino with no password."  
