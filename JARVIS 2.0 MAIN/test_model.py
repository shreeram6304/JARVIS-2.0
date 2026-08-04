import json
import sys
from pathlib import Path

from google import genai


def get_base_dir():
    if getattr(sys, "frozen", False):
        return Path(sys.executable).parent
    return Path(__file__).resolve().parent


BASE_DIR = get_base_dir()
CONFIG = BASE_DIR / "config" / "api_keys.json"

with open(CONFIG, "r", encoding="utf-8") as f:
    api_key = json.load(f)["gemini_api_key"]

client = genai.Client(api_key=api_key)

print("Available Models:\n")

for model in client.models.list():
    print(model.name)