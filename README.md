# AI Command Line Interface

This Python script, `ai.py`, allows you to access ChatGPT from the command line!

Wouldn't you like to do this?
python ai.py none "who was picasso?"
python ai.py none "write python code to generate a 3D surface plot of z = sin(x) + cos(y)"

Instructions
1. Install python. Use method of choice, I'm running Windows 10 and I ran: winget install Python.Python.3.9
2. Create an openai.com account. Be warned, you'll need a phone number. Don't worry it's backed by Microsoft.
3. Generate an API key here: https://beta.openai.com/account/api-keys
4. Open ai.json in notepad and edit "api_key": and replace "your sk key here" with your key.

To run the script, use the following command:
python ai.py [macro] "english description of what you want to do"

Example macros (stored in ai.json):
- 'none' for no prompt string other than what you typed
- 'bash' for Linux and macOS systems command prompts
- 'cmd' for Windows command prompt
- 'esp32' for ESP32 Arduino board code generation
- 'python' for python code

Examples:
py ai.py none "who was picasso?"
python ai.py cmd "List files sorted by size"
python ai.py bash "How much memory does this computer have"
python ai.py python "create a webserver that says hello world, with a button that when you push it says hello to you!"
python ai.py esp32 "create a webserver that says hello and the voltages on the pins. Create the access point named arduino with no password."  
