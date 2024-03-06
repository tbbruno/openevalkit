from openevalkit.core.code_runner import CodeRunner

class UnsafePythonCodeRunner(CodeRunner):
    """
    A code runner that executes Python code in an unsafe manner.

    WARNING: Use this implementation cautiously and only in sandbox environments.
    It runs LLM-generated code that is unverified and potentially dangerous.
    """

    def exec(self, code: str) -> None:
        """
        Execute the given Python code using Python's built-in exec function.

        Args:
            code (str): The Python code to execute.

        Raises:
            Any exception that occurs during code execution.
        """
        exec(code)
