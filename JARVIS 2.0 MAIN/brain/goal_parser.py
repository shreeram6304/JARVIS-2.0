from dataclasses import dataclass
from typing import Optional


@dataclass
class Goal:
    intent: str
    target: str

    domain: Optional[str] = None
    project_type: Optional[str] = None

    framework: Optional[str] = None
    backend: Optional[str] = None
    database: Optional[str] = None
    language: Optional[str] = None

    authentication: bool = False
    api: bool = False
    ai: bool = False

    difficulty: str = "medium"


class GoalParser:

    def parse(self, user_input: str) -> Goal:

        text = user_input.lower()

        goal = Goal(
            intent="unknown",
            target=user_input
        )

        # Intent
        if any(word in text for word in ["build", "create", "develop", "make"]):
            goal.intent = "build"

        # Domain
        if "website" in text or "web" in text:
            goal.domain = "website"
            goal.project_type = "web"

        elif "desktop" in text:
            goal.domain = "desktop"
            goal.project_type = "desktop"

        elif "mobile" in text or "android" in text:
            goal.domain = "mobile"
            goal.project_type = "mobile"

        elif "api" in text:
            goal.domain = "api"
            goal.project_type = "backend"

        # Framework
        if "flask" in text:
            goal.framework = "flask"

        elif "django" in text:
            goal.framework = "django"

        elif "react" in text:
            goal.framework = "react"

        elif "fastapi" in text:
            goal.framework = "fastapi"

        # Backend
        if "firebase" in text:
            goal.backend = "firebase"

        elif "node" in text:
            goal.backend = "node"

        # Database
        if "mysql" in text:
            goal.database = "mysql"

        elif "postgres" in text:
            goal.database = "postgres"

        elif "mongodb" in text:
            goal.database = "mongodb"

        # Language
        if "python" in text:
            goal.language = "python"

        elif "javascript" in text:
            goal.language = "javascript"

        elif "java" in text:
            goal.language = "java"

        # Features
        goal.authentication = (
            "login" in text or
            "signup" in text or
            "authentication" in text
        )

        goal.api = "api" in text

        goal.ai = (
            "ai" in text or
            "llm" in text or
            "chatbot" in text
        )

        return goal