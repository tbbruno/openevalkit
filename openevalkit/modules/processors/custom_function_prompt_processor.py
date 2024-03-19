from openevalkit.core.prompt_processor import PromptProcessor

class CustomFunctionPromptProcessor(PromptProcessor):
    def __init__(self, processor_identifier: str, process_function: callable):
        self._processor_identifier = processor_identifier
        self._process_function = process_function

    @property
    def processor_identifier(self) -> str:
        return self._processor_identifier

    def process(self, prompt: str) -> str:
        print("\nCustomFunctionPromptProcessor - prompt: ", prompt)
        result = self._process_function(prompt)
        print("CustomFunctionPromptProcessor - result: ", result)
        print("\n")
        return result
