import json
import os
import sys
import time
from pathlib import Path

from google import genai
from google.genai.errors import ClientError

from .provider import LLMProvider


def get_base_dir():
    if getattr(sys, "frozen", False):
        return Path(sys.executable).parent
    return Path(__file__).resolve().parent.parent


BASE_DIR = get_base_dir()
API_CONFIG_PATH = BASE_DIR / "config" / "api_keys.json"


class GeminiProvider(LLMProvider):
    """
    Google Gemini implementation with retry support.
    """

    DEFAULT_MODEL = "gemini-flash-latest"

    def __init__(self, model=None):

        api_key = os.getenv("GEMINI_API_KEY")

        if not api_key:

            with open(API_CONFIG_PATH, "r", encoding="utf-8") as f:
                api_key = json.load(f)["gemini_api_key"]

        self.client = genai.Client(api_key=api_key)

        self.model = model or self.DEFAULT_MODEL

    def generate(self, prompt: str):

        max_attempts = 5

        for attempt in range(max_attempts):

            try:

                print(
                    f"[Gemini] Generating... "
                    f"(Attempt {attempt + 1}/{max_attempts})"
                )

                response = self.client.models.generate_content(
                    model=self.model,
                    contents=prompt,
                )

                if getattr(response, "text", None):
                    return response.text

                return str(response)

            except ClientError as e:

                message = str(e)

                print(f"[Gemini] Error: {message}")

                if any(code in message for code in (
                    "429",
                    "RESOURCE_EXHAUSTED",
                    "503",
                    "UNAVAILABLE",
                )):

                    wait = min(2 ** attempt, 30)

                    print(f"[Gemini] Retrying in {wait} second(s)...")

                    time.sleep(wait)

                    continue

                raise

            except Exception:

                raise

        raise RuntimeError(
            f"Gemini failed after {max_attempts} retry attempts."
        )