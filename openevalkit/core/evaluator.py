from abc import ABC, abstractmethod
import datetime
import json
import os

from .prompt_processor import PromptProcessor

class Evaluator(ABC):
    """
    An evaluator is used to evaluate a PromptProcessor against a specific benchmark or evaluation metric.

    Attributes:
        _prompt_processor (PromptProcessor): The prompt processor used by the evaluator.
    """

    def __init__(self, prompt_processor: PromptProcessor):
        """
        Initializes a new instance of the Evaluator class.

        Args:
            prompt_processor (PromptProcessor): The prompt processor used by the evaluator.
        """
        self._prompt_processor = prompt_processor
    
    def evaluate_and_save_results(self) -> None:
        """
        Evaluates the prompt processor and saves the results to a file.
        """
        score, results = self._evaluate()
        
        output = {
            "evaluator": self.evaluator_name,
            "prompt_processor": self._prompt_processor.processor_identifier,
            "score": score,
            "results": results
        }
        
        output_file_path = self._output_file_path()
        
        with open(output_file_path, 'w') as file:
            json.dump(output, file)

    @abstractmethod
    def _evaluate(self) -> tuple[float, list[dict]]:
        """
        Abstract method to be implemented by subclasses.

        This method should perform the evaluation of the prompt processor and return a tuple containing the score
        and the results.

        Returns:
            tuple[float, list[dict]]: A tuple containing the score and the results of the evaluation.
        """
        pass

    @property
    @abstractmethod
    def evaluator_name(self) -> str:
        """
        Abstract property that returns the name of the evaluator.

        Returns:
            str: The name of the evaluator.
        """
        pass

    def _output_file_path(self) -> str:
        """
        Generates the output file path based on the output file name.

        Returns:
            str: The output file path.
        """
        output_dir = "output"
        if not os.path.exists(output_dir):
            os.makedirs(output_dir)
        return f"{output_dir}/{self._output_file_name()}"

    def _output_file_name(self) -> str:
        """
        Generates the output file name based on the evaluator name, prompt processor model name, and current time.

        Returns:
            str: The output file name.
        """
        current_time = datetime.datetime.now().strftime("%H%M%S")
        return f"{self.evaluator_name}-{self._prompt_processor.processor_identifier}-{current_time}.json"
