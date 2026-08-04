import re


class ProjectParser:
    """
    Parses the raw LLM response into individual project files.

    Expected format:

    <FILE: app.py>
    ...
    </FILE>

    <FILE: templates/index.html>
    ...
    </FILE>
    """

    FILE_PATTERN = re.compile(
        r"<FILE:\s*(.*?)>(.*?)</FILE>",
        re.DOTALL | re.IGNORECASE,
    )

    def parse(self, text):
        """
        Extract all files from the LLM response.
        """

        files = []

        if not text:
            print("[Parser] Empty response from LLM.")
            return files

        matches = self.FILE_PATTERN.findall(text)

        for path, content in matches:
            files.append(
                {
                    "path": path.strip(),
                    "content": content.strip(),
                }
            )

        print(f"[Parser] Extracted {len(files)} file(s).")

        if len(files) == 0:
            print("\n========== RAW LLM RESPONSE ==========\n")
            print(text[:3000])  # Print first 3000 characters
            print("\n======================================\n")

        return files