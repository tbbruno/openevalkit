import json
import os

from openevalkit.modules.processors.openai_prompt_processor import OpenAIPromptProcessor
from openevalkit.modules.coderunners.docker_python_code_runner import DockerPythonCodeRunner
from openevalkit.modules.coderunners.unsafe_python_code_runner import UnsafePythonCodeRunner
from openevalkit.modules.evaluators.mbpp_code_evaluator import MBPPCodeEvaluator
from openevalkit.modules.processors.ollama_prompt_processor import OllamaPromptProcessor
from openevalkit.modules.processors.custom_function_prompt_processor import CustomFunctionPromptProcessor
from openevalkit.core.processors_chainer import ProcessorsChainer

OPENAI_API_KEY = "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"
# mbpp_dataset_path = 'test_sample-mbpp.json'
mbpp_dataset_path = 'sanitized-mbpp.json'

# Get the absolute path of the file
dataset_file_full_path = os.path.abspath(os.path.join(os.path.dirname(__file__), mbpp_dataset_path))

# Create an instance of PromptProcessor
# system_prompt = "You are a Python programmer. You'll be given a task and should produce Python code to execute this task. The output should be ONLY the code in plain text, without any surrounding tags."
system_prompt = "You are a Python programmer. You'll be given a task and should produce Python code to execute this task. DON'T include any kind of tags, identifiers or anything besides the actual code in plain text in the output. The output should be able to be pasted into an empty script file and run as is."
# structured_system_prompt = "You are a Python programmer. You'll be given a task and should produce Python code to execute this task. DON'T include any kind of tags, identifiers or anything besides the actual code in plain text in the output. The output should be able to be pasted into an empty script file and run as is. Return to me a valid JSON with just the code in plain-text under the \"code\" key, without any surrounding tags or additional explanation."
# gpt_prompt_processor = OpenAIPromptProcessor(api_key=OPENAI_API_KEY, model_name="gpt-4-turbo-preview", system_prompt=structured_system_prompt, json_mode=True)
prompt_processor = OllamaPromptProcessor(model_name="codellama", system_prompt=system_prompt)
# prompt_processor = OllamaPromptProcessor(model_name="llama2", system_prompt=system_prompt)

extractor_system_prompt = """
You are a code extractor. Extract the Python code from the provided prompt and DON'T include any type of tag surrounding it (like [PYTHON] or ```). Return to me a valid JSON with just the code in plain-text under the "code" key, without any surrounding tags or additional explanation.
"""
code_extractor_processor = OpenAIPromptProcessor(api_key=OPENAI_API_KEY, model_name="gpt-4-turbo-preview", system_prompt=extractor_system_prompt, json_mode=True)

def process_prompt(prompt):
    response = prompt_processor.process(prompt)
    processed_response = code_extractor_processor.process(response)
    json_data = json.loads(processed_response)
    code = json_data["code"]
    return code

custom_processor = CustomFunctionPromptProcessor(
    processor_identifier="fn_processor_code_extractor",
    process_function=process_prompt
)

# def process_prompt(prompt):
#     response = gpt_prompt_processor.process(prompt)
#     json_data = json.loads(response)
#     code = json_data["code"]
#     return code

# gpt_custom_processor = CustomFunctionPromptProcessor(
#     processor_identifier=f"{gpt_prompt_processor.processor_identifier}-fn_processor_code_extractor",
#     process_function=process_prompt
# )

# processors_chainer = ProcessorsChainer(prompt_processor, custom_processor)

# Create an instance of CodeRunner
code_runner = DockerPythonCodeRunner()
# code_runner = UnsafePythonCodeRunner()

# Create an instance of CodeEvaluator
# evaluator = MBPPCodeEvaluator(prompt_processor=prompt_processor, code_runner=code_runner, mbpp_dataset_json_path=dataset_file_full_path)
evaluator = MBPPCodeEvaluator(prompt_processor=custom_processor, code_runner=code_runner, mbpp_dataset_json_path=dataset_file_full_path)
# evaluator = MBPPCodeEvaluator(prompt_processor=gpt_custom_processor, code_runner=code_runner, mbpp_dataset_json_path=dataset_file_full_path)

# Evaluate the code
results = evaluator.evaluate_and_save_results()
