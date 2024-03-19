import ollama

from openevalkit.core.prompt_processor import PromptProcessor

class OllamaPromptProcessor(PromptProcessor):
    """
    A basic Ollama wrapper for processing prompts.

    Note: Before using this processor, make sure that the Ollama is running locally on the machine.

    Args:
        model_name (str): The name of the model Ollama should use.
        system_prompt (str, optional): The system prompt to include in the conversation. Defaults to None.
    """

    def __init__(self, model_name: str, system_prompt: str = None):
        self._model_name = model_name
        
        if system_prompt is not None:
            modelfile = f"FROM {self._model_name}\nSYSTEM \"\"\"{system_prompt}\"\"\""
            print("\n\n")
            print("OllamaPromptProcessor - modelfile: ", modelfile)
            print("\n\n")
            self._model_name = f'{self._model_name}_custom'
            ollama.create(model=self._model_name, modelfile=modelfile)

    @property
    def processor_identifier(self) -> str:
        """
        Gets the identifier of the prompt processor.

        Returns:
            str: The model name as the identifier of the prompt processor.
        """
        return self._model_name

    def process(self, prompt: str) -> str:
        """
        Processes the given prompt and generates a response using Ollama.

        Args:
            prompt (str): The user prompt to process.

        Returns:
            str: The generated response from the model running through Ollama.
        """
        print("OllamaPromptProcessor - prompt: ", prompt)

        messages = [{'role': 'user', 'content': prompt}]
        
        response = ollama.chat(
            model=self._model_name,
            messages=messages
        )
        result = response['message']['content'].strip()
        
        print("OllamaPromptProcessor - result: ", result)
        return result
