from openai import OpenAI
from openevalkit.core.prompt_processor import PromptProcessor

class OpenAIPromptProcessor(PromptProcessor):
    def __init__(self, api_key: str, model_name: str, system_prompt: str = None, json_mode: bool = False):
        self._client = OpenAI(api_key=api_key)
        self._model_name = model_name
        self._system_prompt = system_prompt
        self._json_mode = json_mode

    @property
    def processor_identifier(self) -> str:
        """
        Get the identifier of the prompt processor.

        Returns:
            str: The model name as the identifier of the prompt processor.
        """
        return self._model_name

    def process(self, prompt: str) -> str:
        print("OpenAIPromptProcessor - prompt: ", prompt)
        messages = []
        if self._system_prompt:
            messages.append({"role": "system", "content": self._system_prompt})
        messages.append({"role": "user", "content": prompt})
        chat_completion = self._client.chat.completions.create(
            model=self._model_name,
            messages=messages,
            response_format= { "type": "json_object" } if self._json_mode else { "type": "text" }
        )
        result = chat_completion.choices[0].message.content.strip()
        print("OpenAIPromptProcessor - result: ", result)
        return result
