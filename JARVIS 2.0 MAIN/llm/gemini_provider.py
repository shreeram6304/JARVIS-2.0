import json
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
    Google Gemini implementation with automatic retry support.
    """

    def __init__(self):

        with open(API_CONFIG_PATH, "r", encoding="utf-8") as f:
            api_key = json.load(f)["gemini_api_key"]

        self.client = genai.Client(api_key=api_key)

        # Centralize model selection here
        self.model = "gemini-flash-latest"

    def generate(self, prompt: str):

        max_attempts = 5

        for attempt in range(max_attempts):

            try:

                print(f"[Gemini] Generating... (Attempt {attempt + 1}/{max_attempts})")

                response = self.client.models.generate_content(
                    model=self.model,
                    contents=prompt,
                )

                # Safely return text
                if hasattr(response, "text") and response.text:
                    return response.text

                return str(response)

            except ClientError as e:

                message = str(e)

                print(f"[Gemini] Error: {message}")

                # Retry on temporary failures
                if (
                    "429" in message
                    or "RESOURCE_EXHAUSTED" in message
                    or "503" in message
                    or "UNAVAILABLE" in message
                ):

                    wait = 2 ** attempt

                    print(f"[Gemini] Retrying in {wait} second(s)...")

                    time.sleep(wait)

                    continue

                # Non-retryable error
                raise

            except Exception as e:

                print(f"[Gemini] Unexpected Error: {e}")
                raise

        raise RuntimeError(
            f"Gemini failed after {max_attempts} retry attempts."
        )