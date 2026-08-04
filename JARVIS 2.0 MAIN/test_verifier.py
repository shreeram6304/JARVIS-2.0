from builder.verifier import ProjectVerifier

verifier = ProjectVerifier()

result = verifier.verify({
    "success": False,
    "stderr": "ModuleNotFoundError: No module named flask"
})

print(result)