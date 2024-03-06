from abc import ABC, abstractmethod

class CodeRunner(ABC):
    """Abstract base class for code runners."""

    @abstractmethod
    def exec(self, code: str) -> None:
        """Execute the given code.

        Args:
            code (str): The code to be executed.

        Returns:
            None
        """
        pass
