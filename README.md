# AI Command Line Interface

This Python script, `aicmd.py`, allows you to access ChatGPT from the command line!

# Installation Instructions
- Install python from eg https://www.python.org/
- pip install openai
- Go to openai.com and create an openai.com account
- Generate an API key here: https://beta.openai.com/account/api-keys
- The first time you run aicmd.py it will ask for the API key if environment variable OPENAI_API_KEY is not set.

# Usage
python aicmd.py [macro] "english description of what you want to do"

# Examples
- python aicmd.py none "who was picasso?"
- python aicmd.py cmd "List files sorted by size"
- python aicmd.py bash "How much memory does this computer have"
- python aicmd.py python "create a webserver that says hello world, with a button that when you push it says hello to you!"
- python aicmd.py esp32 "create a webserver that says hello and the voltages on the pins. Create the access point named arduino with no password."  
- python aicmd.py python "show a 3D surface plot of z = sin(x) + cos(y)"

# Configuration
There is a file next to aicmd.py which was intended to help you.
- 'bash' for Linux and macOS systems command prompts. Not tested.
- 'cmd' for Windows command prompt
- 'esp32' for ESP32 Arduino board code generation. Not finished. I intend to execute code on the esp32 with one natural language request.
- 'python' for python code
- 'none' for no prompt string other than what you typed
