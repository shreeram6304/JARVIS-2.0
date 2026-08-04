from builder.pipeline import DevelopmentPipeline

response = """
<JARVIS_PROJECT>

<FILE path="app.py">
print("Pipeline Works!")
</FILE>

</JARVIS_PROJECT>
"""

pipeline = DevelopmentPipeline()

report = pipeline.execute(
    "PipelineDemo",
    response
)

print(report)