from builder.writer import ProjectWriter

files = [
    {
        "path": "app.py",
        "content": 'print("Hello World")'
    },
    {
        "path": "templates/index.html",
        "content": "<h1>Hello</h1>"
    },
    {
        "path": "requirements.txt",
        "content": "flask"
    }
]

writer = ProjectWriter()

written = writer.write(
    "CalculatorWebsite",
    files
)

for file in written:
    print(file)