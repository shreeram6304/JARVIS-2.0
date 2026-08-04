import subprocess
import sys
import time
from pathlib import Path


class ProjectRunner:
    """
    Installs dependencies and runs generated projects.
    Supports both console applications and web applications.
    """

    def install_requirements(self, project_path):

        requirements = project_path / "requirements.txt"

        if not requirements.exists():
            print("[Runner] No requirements.txt found.")
            return True

        print("[Runner] Installing dependencies...")

        result = subprocess.run(
            [
                sys.executable,
                "-m",
                "pip",
                "install",
                "-r",
                "requirements.txt",
            ],
            cwd=project_path,
            capture_output=True,
            text=True,
        )

        if result.returncode != 0:

            print("\n========== PIP ERROR ==========")
            print(result.stderr)
            print("================================\n")

            return False

        print("[Runner] Dependencies installed successfully.")

        return True

    def run(self, project_path):

        project_path = Path(project_path)

        app = project_path / "app.py"

        if not app.exists():

            return {
                "success": False,
                "stdout": "",
                "stderr": "No runnable project found.",
            }

        if not self.install_requirements(project_path):

            return {
                "success": False,
                "stdout": "",
                "stderr": "Dependency installation failed.",
            }

        print("[Runner] Launching application...")

        process = subprocess.Popen(
            [sys.executable, "app.py"],
            cwd=project_path,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            text=True,
        )

        # Allow application to start
        time.sleep(5)

        # Still running? Treat as successful web application.
        if process.poll() is None:

            print("[Runner] Application is running.")

            process.terminate()

            try:
                process.wait(timeout=5)
            except subprocess.TimeoutExpired:
                process.kill()

            return {
                "success": True,
                "stdout": "Application started successfully.",
                "stderr": "",
            }

        stdout, stderr = process.communicate()

        print("\n========== APPLICATION OUTPUT ==========")

        if stdout.strip():
            print("\nSTDOUT:\n")
            print(stdout)

        if stderr.strip():
            print("\nSTDERR:\n")
            print(stderr)

        print("========================================\n")

        return {
            "success": process.returncode == 0,
            "stdout": stdout,
            "stderr": stderr,
        }