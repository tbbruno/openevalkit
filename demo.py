# Criando o PromptProcessor
system_prompt = "You are a Python programmer. You'll be given a task and should produce Python code to execute this task. DON'T include any kind of tags, identifiers or anything besides the actual code in plain text in the output. The output should be able to be pasted into an empty script file and run as is."
prompt_processor = OllamaPromptProcessor(model_name="codellama", system_prompt=system_prompt)

# Extraindo o código
extractor_system_prompt = "You are a code extractor. Extract the Python code from the provided prompt and DON'T include any type of tag surrounding it (like [PYTHON] or ```). Return to me a valid JSON with just the code in plain-text under the 'code' key, without any surrounding tags or additional explanation."
code_extractor_processor = OpenAIPromptProcessor(api_key=OPENAI_API_KEY,
    model_name="gpt-4-turbo-preview",
    system_prompt=extractor_system_prompt,
    json_mode=True)
def process_prompt(prompt):
    response = prompt_processor.process(prompt)
    processed_response = code_extractor_processor.process(response)
    json_data = json.loads(response)
    code = json_data["code"]
    return code
custom_processor = CustomFunctionPromptProcessor(
    processor_identifier="fn_processor_code_extractor",
    process_function=process_prompt
)

# Create an instance of CodeRunner
code_runner = DockerPythonCodeRunner()
# Create an instance of CodeEvaluator
evaluator = MBPPCodeEvaluator(
    prompt_processor=custom_processor,
    code_runner=code_runner,
    mbpp_dataset_json_path=dataset_file_full_path
)
# Evaluate the code
results = evaluator.evaluate_and_save_results()
