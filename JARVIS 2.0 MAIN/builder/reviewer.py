import json
from pathlib import Path

from llm.gemini_provider import GeminiProvider


class ProjectReviewer:
    """
    Reviews generated projects and returns structured JSON.
    """

    def __init__(self):

        self.llm = GeminiProvider()

    def load_project(self, project_path):

        project_path = Path(project_path)

        project_text = ""

        for file in project_path.rglob("*"):

            if not file.is_file():
                continue

            if "__pycache__" in str(file):
                continue

            if file.suffix in [".pyc", ".db"]:
                continue

            try:

                relative = file.relative_to(project_path)

                project_text += f"\n\n===== FILE: {relative} =====\n"

                project_text += file.read_text(
                    encoding="utf-8",
                    errors="ignore"
                )

            except Exception:
                pass

        return project_text

    def build_prompt(self, project_text):

        return f"""
You are a Senior Software Architect.

Review the following software project.

Return ONLY valid JSON.

Schema:

{{
    "status":"PASS or FAIL",
    "score":0,
    "summary":"",
    "issues":[
        {{
            "file":"",
            "problem":"",
            "severity":"LOW|MEDIUM|HIGH|CRITICAL"
        }}
    ],
    "files_to_fix":[]
}}

Scoring:

100 = Production ready

80 = Minor improvements

60 = Several bugs

40 = Serious issues

0 = Completely broken

PROJECT

{project_text}
"""

    def review(self, project_path):

        print("[Reviewer] Reviewing generated project...")

        project = self.load_project(project_path)

        prompt = self.build_prompt(project)

        response = self.llm.generate(prompt)

        print("[Reviewer] Review complete.")

        # Remove Markdown fences if Gemini adds them
        cleaned = response.strip()

        if cleaned.startswith("```json"):
            cleaned = cleaned[7:]

        if cleaned.startswith("```"):
            cleaned = cleaned[3:]

        if cleaned.endswith("```"):
            cleaned = cleaned[:-3]

        cleaned = cleaned.strip()

        try:

            return json.loads(cleaned)

        except Exception:

            print("[Reviewer] Invalid JSON received.")

            return {
                "status": "FAIL",
                "score": 0,
                "summary": "Reviewer returned invalid JSON.",
                "issues": [],
                "files_to_fix": []
            }