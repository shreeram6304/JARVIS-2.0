from builder.runner import ProjectRunner

runner = ProjectRunner()

result = runner.run("generated_projects/CalculatorWebsite")

print(result)