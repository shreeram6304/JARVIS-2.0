from pathlib import Path

from llm.gemini_provider import GeminiProvider
from builder.parser import ProjectParser
from builder.writer import ProjectWriter


class ProjectRepairer:
    """
    Repairs generated projects using the LLM.
    """

    def __init__(self):

        self.llm = GeminiProvider()
        self.parser = ProjectParser()
        self.writer = ProjectWriter()

    def load_project(self, project_path):

        project_path = Path(project_path)

        project = ""

        for file in project_path.rglob("*"):

            if not file.is_file():
                continue

            if "__pycache__" in str(file):
                continue

            if file.suffix in [".pyc", ".db"]:
                continue

            try:

                relative = file.relative_to(project_path)

                project += f"\n\n<FILE: {relative}>\n"

                project += file.read_text(
                    encoding="utf-8",
                    errors="ignore",
                )

                project += "\n</FILE>\n"

            except Exception:
                pass

        return project

    def build_prompt(self, project, review, runtime_error):

        return f"""
You are a Senior Software Engineer.

The following software project failed.

YOUR JOB

Repair the project.

Rules

- Fix every syntax error.
- Fix every import error.
- Fix every runtime error.
- Preserve the project architecture.
- Modify ONLY files that require changes.

Return ONLY file blocks.

Example

<FILE: app.py>
...
</FILE>

PROJECT

{project}

REVIEW

{review}

RUNTIME ERROR

{runtime_error}
"""

    def repair(self, project_name, project_path, review, runtime_error):

        print("[Repair] Loading project...")

        project = self.load_project(project_path)

        prompt = self.build_prompt(
            project,
            review,
            runtime_error,
        )

        print("[Repair] Asking Gemini to repair project...")

        response = self.llm.generate(prompt)

        files = self.parser.parse(response)

        if not files:

            print("[Repair] No repaired files returned.")

            return False

        self.writer.write(
            project_name,
            files,
        )

        print(f"[Repair] Applied {len(files)} repaired file(s).")

        return True