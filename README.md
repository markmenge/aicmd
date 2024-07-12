# AI Command Line Interface

This Python script, `aicmd.py`, allows you to with a single command ask ChatGPT to do tasks from the command line, allowing natural language to quickly do amazing things!

# Installation Instructions
- Install python from eg https://www.python.org/
- pip install openai
- Go to openai.com and create an openai.com account
- Generate an API key here: https://beta.openai.com/account/api-keys
- The first time you run aicmd.py it will ask for the API key if environment variable OPENAI_API_KEY is not set. You might need to be administrator.

# Usage
python aicmd.py [context] "english description of what you want to do"

# Examples
- python aicmd.py none "who was picasso?"
<pre>
Pablo Picasso was a Spanish painter, sculptor, printmaker, and ceramicist who is widely regarded as one of the most influential artists of the 20th century. Born in 1881 in Malaga, Spain, he spent most of his adult life in France, where he became a central figure in the avant-garde movements of the early 1900s, including Cubism and Surrealism.
</pre>

- python aicmd.py cmd "List files sorted by size"
<pre>
F:\proj\aicmd>dir /os
 Volume in drive F is WDC3GB
 Volume Serial Number is FAED-0C9C

 Directory of F:\proj\aicmd

04/05/2023  11:14 AM    <DIR>          .
04/05/2023  11:14 AM    <DIR>          ..
03/20/2023  01:52 PM    <DIR>          __pycache__
03/20/2023  01:52 PM                15 requirements.txt
03/23/2023  02:23 PM               141 ChatGPT.py
03/20/2023  01:52 PM               616 aicmd.json
03/20/2023  01:52 PM             1,066 LICENSE
03/20/2023  01:52 PM             1,192 check_imports.py
03/20/2023  01:52 PM             1,436 README.md
03/20/2023  01:52 PM             5,028 aicmd.py
</pre>

- python aicmd.py bash "How much memory does this computer have"
<pre>
$ free -h
               total        used        free      shared  buff/cache   available
Mem:           7.7Gi       326Mi       6.2Gi        22Mi       1.2Gi       7.1Gi
Swap:          2.0Gi          0B       2.0Gi
</pre>

- python aicmd.py python "create a webserver that says hello world, with a button that when you push it says hello to you!"

- python aicmd.py esp32 "create a webserver that says hello and the voltages on the pins. Create the access point named arduino with no password."  

- python aicmd.py python "show a 3D surface plot of z = sin(x) + cos(y)"

![image](https://user-images.githubusercontent.com/10154651/230124326-0fb44dbd-857a-4785-98f1-c79502631613.png)

# Configuration
There is a file aicmd.json next to aicmd.py which is intended to help you.
- 'bash' for Linux and macOS systems command prompts. Not tested.
- 'cmd' for Windows command prompt
- 'esp32' for ESP32 Arduino board code generation. Not finished. I intend to execute code on the esp32 with one natural language request.
- 'python' for python code
- 'none' for no prompt string other than what you typed
