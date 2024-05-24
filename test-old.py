import os

from openevalkit.modules.processors.openai_prompt_processor import OpenAIPromptProcessor
from openevalkit.modules.coderunners.docker_python_code_runner import DockerPythonCodeRunner
from openevalkit.modules.coderunners.unsafe_python_code_runner import UnsafePythonCodeRunner
from openevalkit.modules.evaluators.mbpp_code_evaluator import MBPPCodeEvaluator
from openevalkit.modules.processors.ollama_prompt_processor import OllamaPromptProcessor
from openevalkit.core.processors_chainer import ProcessorsChainer

OPENAI_API_KEY = "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"
test_sample_mbpp_dataset_path = 'test_sample-mbpp.json'
# Get the absolute path of the file
abs_test_sample_mbpp_dataset_path = os.path.abspath(os.path.join(os.path.dirname(__file__), test_sample_mbpp_dataset_path))

# Create an instance of PromptProcessor
# system_prompt = "You are a Python programmer. You'll be given a task and should produce Python code to execute this task. The output should be ONLY the code in plain text, without any surrounding tags."
system_prompt = "You are a Python programmer. You'll be given a task and should produce Python code to execute this task. DON'T include any kind of tags, identifiers or anything besides the actual code in plain text in the output. The output should be able to be pasted into an empty script file and run as is."
# prompt_processor = OpenAIPromptProcessor(api_key=OPENAI_API_KEY, model_name="gpt-4-turbo-preview")
# prompt_processor = OllamaPromptProcessor(model_name="llama2", system_prompt=system_prompt)
prompt_processor = OllamaPromptProcessor(model_name="codellama", system_prompt=system_prompt)

extractor_system_prompt = """
You are a code extractor. Extract the Python code from the provided prompt and DON'T include any type of tag surrounding it (like [PYTHON] or ```). Return to me JUST the code in plain text, without any surrounding tags or additional explanation.

Here's an example of what an output format should look like:
def heap_queue_largest(numbers, n):
    h = []
    for num in numbers:
        heappush(h, -num)
    largest = []
    for i in range(n):
        largest.append(-heappop(h))
    return largest
"""
code_extractor_processor = OllamaPromptProcessor(model_name="codellama", system_prompt=extractor_system_prompt)

processors_chainer = ProcessorsChainer(prompt_processor, code_extractor_processor)

# Create an instance of CodeRunner
code_runner = DockerPythonCodeRunner()
# code_runner = UnsafePythonCodeRunner()

# Create an instance of CodeEvaluator
# evaluator = MBPPCodeEvaluator(prompt_processor=prompt_processor, code_runner=code_runner, mbpp_dataset_json_path=abs_test_sample_mbpp_dataset_path)
evaluator = MBPPCodeEvaluator(prompt_processor=processors_chainer, code_runner=code_runner, mbpp_dataset_json_path=abs_test_sample_mbpp_dataset_path)

# Evaluate the code
results = evaluator.evaluate_and_save_results()


## Test model file creation

# code_extractor_processor._create_model_file(extractor_system_prompt)
