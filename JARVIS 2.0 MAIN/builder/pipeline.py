from builder.parser import ProjectParser
from builder.writer import ProjectWriter
from builder.runner import ProjectRunner
from builder.verifier import ProjectVerifier


class DevelopmentPipeline:
    """
    Complete software development pipeline.
    """

    def __init__(self):

        self.parser = ProjectParser()
        self.writer = ProjectWriter()
        self.runner = ProjectRunner()
        self.verifier = ProjectVerifier()

    def execute(self, project_name, llm_response):

        print("[Pipeline] Parsing project...")

        files = self.parser.parse(llm_response)

        print("[Pipeline] Writing files...")

        self.writer.write(project_name, files)

        print("[Pipeline] Running project...")

        result = self.runner.run(
            f"generated_projects/{project_name}"
        )

        print("[Pipeline] Verifying...")

        report = self.verifier.verify(result)

        return report