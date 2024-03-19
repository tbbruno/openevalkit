from openevalkit.core.prompt_processor import PromptProcessor

class ProcessorsChainer(PromptProcessor):
    """
    ProcessorsChainer is a special implemntation of PromptProcessor. It simply chains two other prompt processors together.

    This class takes two prompt processors as input and chains them together.
    The output of the first processor is passed as input to the second processor,
    and the final output is returned.

    Attributes:
        _processor1 (PromptProcessor): The first prompt processor in the chain.
        _processor2 (PromptProcessor): The second prompt processor in the chain.
    """

    def __init__(self, processor1, processor2):
        """
        Initializes a new instance of the ProcessorsChainer class.

        Args:
            processor1 (PromptProcessor): The first prompt processor in the chain.
            processor2 (PromptProcessor): The second prompt processor in the chain.
        """
        self._processor1 = processor1
        self._processor2 = processor2

    @property
    def processor_identifier(self):
            """
            Returns the identifier of the chained processors.

            The identifier is made up of the identifiers of the two processors
            that are chained together, separated by an underscore.

            Returns:
                str: The identifier of the chained processors.
            """
            return self._processor1.processor_identifier + '_' + self._processor2.processor_identifier

    def process(self, prompt):
        """
        Processes the prompt using the chained processors.

        Args:
            prompt (str): The prompt to be processed.

        Returns:
            Any: The final output after processing the prompt using the chained processors.
        """
        intermediate_output = self._processor1.process(prompt)
        final_output = self._processor2.process(intermediate_output)
        return final_output
