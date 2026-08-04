import re


class ProjectVerifier:
    """
    Analyzes project execution results and returns
    detailed diagnostics.
    """

    def verify(self, run_result):

        if run_result["success"]:
            return {
                "success": True,
                "problem": None,
                "solution": None,
                "details": None,
            }

        error = run_result.get("stderr", "")

        if not error:
            error = "Unknown error."

        # Try to extract file and line number
        file_match = re.search(r'File "(.*?)", line (\d+)', error)

        location = None

        if file_match:
            location = {
                "file": file_match.group(1),
                "line": file_match.group(2),
            }

        if "ModuleNotFoundError" in error:

            return {
                "success": False,
                "problem": "Missing package",
                "solution": "Install required dependency",
                "details": error,
                "location": location,
            }

        elif "SyntaxError" in error:

            return {
                "success": False,
                "problem": "Syntax Error",
                "solution": "Rewrite affected source file",
                "details": error,
                "location": location,
            }

        elif "NameError" in error:

            return {
                "success": False,
                "problem": "Undefined variable",
                "solution": "Declare missing variable",
                "details": error,
                "location": location,
            }

        elif "ImportError" in error:

            return {
                "success": False,
                "problem": "Import Error",
                "solution": "Fix import statement",
                "details": error,
                "location": location,
            }

        elif "TypeError" in error:

            return {
                "success": False,
                "problem": "Type Error",
                "solution": "Fix incorrect data types",
                "details": error,
                "location": location,
            }

        elif "AttributeError" in error:

            return {
                "success": False,
                "problem": "Attribute Error",
                "solution": "Fix missing attribute or method",
                "details": error,
                "location": location,
            }

        elif "ValueError" in error:

            return {
                "success": False,
                "problem": "Value Error",
                "solution": "Validate input values",
                "details": error,
                "location": location,
            }

        return {
            "success": False,
            "problem": "Unknown Error",
            "solution": "Review execution log",
            "details": error,
            "location": location,
        }