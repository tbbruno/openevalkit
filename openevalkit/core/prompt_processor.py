from abc import ABC, abstractmethod

class PromptProcessor(ABC):
    """
    Abstract base class for prompt processors.

    Prompt processors are responsible for processing prompts and generating responses.
    This abstract base class serves as a blueprint for concrete implementations of prompt processors.

    Concrete implementations of this class can abstract existing LLM models, but they can also utilize
    other strategies such as fine-tuned LLMs, prompt engineering, RAG, custom LangChain chains, and
    any other techniques to refine the output.

    By subclassing this abstract base class, developers can create their own prompt processors tailored
    to their specific needs and requirements.
    """

    @property
    @abstractmethod
    def processor_identifier(self) -> str:
        """
        Get the identifier of the prompt processor.

        Returns:
            str: The identifier of the prompt processor.
        """
        pass

    @abstractmethod
    def process(self, prompt: str) -> str:
        """
        Process the given prompt and generate a response.

        Args:
            prompt (str): The prompt to process.

        Returns:
            str: The generated response.
        """
        pass
