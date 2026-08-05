from builder.parser import ProjectParser
from builder.writer import ProjectWriter
from builder.reviewer import ProjectReviewer
from builder.runner import ProjectRunner
from builder.verifier import ProjectVerifier
from builder.repair import ProjectRepairer


class DevelopmentPipeline:
    """
    Autonomous software development pipeline.

    Flow:

    Parse
        ↓
    Write
        ↓
    Review
        ↓
    Run
        ↓
    Verify
        ↓
    Repair (if needed)
        ↓
    Retry
    """

    MAX_REPAIR_ATTEMPTS = 3

    def __init__(self):

        self.parser = ProjectParser()
        self.writer = ProjectWriter()
        self.reviewer = ProjectReviewer()
        self.runner = ProjectRunner()
        self.verifier = ProjectVerifier()
        self.repairer = ProjectRepairer()

    def execute(self, project_name, llm_response):

        print("[Pipeline] Parsing project...")

        files = self.parser.parse(llm_response)

        if not files:

            return {
                "success": False,
                "problem": "Parser Error",
                "solution": "No files were extracted from the LLM response."
            }

        print("[Pipeline] Writing project...")

        project_path = self.writer.write(
            project_name,
            files
        )

        if project_path is None:
            project_path = f"generated_projects/{project_name}"

        for attempt in range(self.MAX_REPAIR_ATTEMPTS + 1):

            print(f"\n========== ATTEMPT {attempt + 1} ==========\n")

            print("[Pipeline] Reviewing project...")

            review = self.reviewer.review(project_path)

            print("\n========== REVIEW ==========")
            print(review)
            print("============================\n")

            print("[Pipeline] Running project...")

            run_result = self.runner.run(project_path)

            print("[Pipeline] Verifying...")

            report = self.verifier.verify(run_result)

            report["review"] = review

            if report["success"]:

                print("\n[Pipeline] Project completed successfully.\n")

                return report

            if attempt >= self.MAX_REPAIR_ATTEMPTS:

                print("\n[Pipeline] Maximum repair attempts reached.\n")

                return report

            print("\n[Pipeline] Repairing project...\n")

            repaired = self.repairer.repair(
                project_name=project_name,
                project_path=project_path,
                review=review,
                runtime_error=run_result["stderr"],
            )

            if not repaired:

                print("[Pipeline] Repair failed.")

                return report

        return {
            "success": False,
            "problem": "Unexpected pipeline failure",
            "solution": None,
        }