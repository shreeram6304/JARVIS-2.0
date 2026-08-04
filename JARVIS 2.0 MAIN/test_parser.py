from builder.parser import ProjectParser

response = """
<JARVIS_PROJECT>

<FILE path="app.py">
print("Hello")
</FILE>

<FILE path="requirements.txt">
flask
</FILE>

</JARVIS_PROJECT>
"""

parser = ProjectParser()

files = parser.parse(response)

print(files)