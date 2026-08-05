from pathlib import Path


class ProjectWriter:
    """
    Writes a generated project to disk.
    """

    def __init__(self, workspace="generated_projects"):

        self.workspace = Path(workspace)
        self.workspace.mkdir(parents=True, exist_ok=True)

    def write(self, project_name, files):

        project_dir = self.workspace / project_name
        project_dir.mkdir(parents=True, exist_ok=True)

        for file in files:

            path = project_dir / file["path"]

            path.parent.mkdir(parents=True, exist_ok=True)

            path.write_text(
                file["content"],
                encoding="utf-8",
            )

        print(f"[Writer] Project written to: {project_dir}")

        # Return the PROJECT DIRECTORY, not a list of files.
        return str(project_dir)