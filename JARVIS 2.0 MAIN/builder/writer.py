from pathlib import Path


class ProjectWriter:
    """
    Writes a generated project to disk.
    """

    def __init__(self, workspace="generated_projects"):
        self.workspace = Path(workspace)
        self.workspace.mkdir(exist_ok=True)

    def write(self, project_name, files):

        project_dir = self.workspace / project_name
        project_dir.mkdir(parents=True, exist_ok=True)

        written = []

        for file in files:

            path = project_dir / file["path"]

            path.parent.mkdir(parents=True, exist_ok=True)

            path.write_text(
                file["content"],
                encoding="utf-8"
            )

            written.append(path)

        return written