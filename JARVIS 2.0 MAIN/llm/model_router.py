from llm.gemini_provider import GeminiProvider


class ModelRouter:
    """
    Central model router.

    Every AI component should request a model
    through this class instead of creating one
    directly.
    """

    def __init__(self):

        self._models = {
            "coding": GeminiProvider(),
            "review": GeminiProvider(),
            "repair": GeminiProvider(),
            "general": GeminiProvider(),
        }

    def get(self, task="general"):

        return self._models.get(
            task,
            self._models["general"]
        )