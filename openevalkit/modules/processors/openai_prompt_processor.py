from openai import OpenAI
from openevalkit.core.prompt_processor import PromptProcessor

class OpenAIPromptProcessor(PromptProcessor):
    def __init__(self, api_key: str, model_name: str):
        self._client = OpenAI(api_key=api_key)
        self._model_name = model_name

    @property
    def processor_identifier(self) -> str:
        """
        Get the identifier of the prompt processor.

        Returns:
            str: The identifier of the prompt processor.
        """
        return self._model_name

    def process(self, prompt: str) -> str:
        print("OpenAIPromptProcessor - prompt: ", prompt)
        chat_completion = self._client.chat.completions.create(
            model=self._model_name,
            messages=[
                {"role": "system", "content": "You are a Python programmer. You'll be given a task and should produce Python code to execute this task. The output should be ONLY the code in plain text, without any surrounding tags."},
                {"role": "user", "content": prompt}
            ]
        )
        result = chat_completion.choices[0].message.content.strip()
        print("OpenAIPromptProcessor - result: ", result)
        return result
