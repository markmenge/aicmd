
import argparse
import json
import openai
import os

dir_path = os.path.dirname(os.path.realpath(__file__))

settings_path = os.path.join(dir_path, "aicmd.settings.json")
if os.path.exists(settings_path):
            ans = input(f"File {settings_path}exists, are you sure you want to continue (y/n)?")
            if ans != 'y':
                exit
settings = {
    "api_key": "sk-your key here",
    "api_endpoint": "https://api.openai.com/v1",
}
settings["api_key"] = input("Enter you openai API key:")
with open(settings_path, "w") as file:
    json.dump(settings, file, indent=4)
