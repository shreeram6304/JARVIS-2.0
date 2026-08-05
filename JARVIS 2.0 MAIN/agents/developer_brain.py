from llm.model_router import ModelRouter
from llm.prompts import DEVELOPER_SYSTEM_PROMPT


class DeveloperBrain:
    """
    Main software engineering intelligence for JARVIS.
    """

    def __init__(self):

        self.router = ModelRouter()
        self.llm = self.router.get("coding")

    def build_prompt(self, goal, plan):

        prompt = DEVELOPER_SYSTEM_PROMPT

        prompt += "\n\nPROJECT GOAL\n\n"
        prompt += goal

        prompt += "\n\nPROJECT PLAN\n"

        for i, task in enumerate(plan.tasks, start=1):
            prompt += f"\n{i}. {task.name}"

        prompt += """

Generate the COMPLETE project.

Return EVERY file using EXACTLY this format.

<FILE: app.py>
# file contents
</FILE>

<FILE: requirements.txt>
# file contents
</FILE>

<FILE: README.md>
# file contents
</FILE>

If there are templates:

<FILE: templates/index.html>
...
</FILE>

If there are static files:

<FILE: static/style.css>
...
</FILE>

Rules:

- Return ONLY file blocks.
- Do NOT explain.
- Do NOT use Markdown.
- Do NOT use ``` code fences.
- Every file MUST begin with <FILE: path>
- Every file MUST end with </FILE>
"""

        return prompt

    def generate_project(self, goal, plan):
        """
        Generate a complete software project.
        """

        prompt = self.build_prompt(goal, plan)

        return self.llm.generate(prompt)