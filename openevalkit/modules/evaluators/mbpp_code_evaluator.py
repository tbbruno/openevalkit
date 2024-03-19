import json

from openevalkit.core.code_runner import CodeRunner
from openevalkit.core.evaluator import Evaluator
from openevalkit.core.prompt_processor import PromptProcessor

class MBPPCodeEvaluator(Evaluator):
    def __init__(self, prompt_processor: PromptProcessor, 
                 code_runner: CodeRunner, 
                 mbpp_dataset_json_path: str):
        super().__init__(prompt_processor)
        self._code_runner = code_runner
        self._dataset = self._read_dataset_from_json(mbpp_dataset_json_path)

    @property
    def evaluator_name(self) -> str:
      return "MBPP"

    def _read_dataset_from_json(self, mbpp_dataset_json_path: str) -> list:
        with open(mbpp_dataset_json_path, 'r') as file:
            dataset = json.load(file)
        return dataset

    def _evaluate(self) -> tuple[float, list[dict]]:
        results = []
        successful_tasks = 0
        
        full_dataset_len = len(self._dataset)
        for index, entry in enumerate(self._dataset):
            print(f"MBPPCodeEvaluator - 🙋‍♂️ evaluating task {index + 1} of {full_dataset_len}")
            task_id = entry["task_id"]
            task_prompt = entry["prompt"]
            test_cases = entry["test_list"]
            full_prompt = self._few_shots_prompt(task_prompt, test_cases)
            
            generated_code = self._prompt_processor.process(full_prompt)
            
            task_result = {
                "task_id": task_id,
                "prompt": task_prompt,
                "processed_prompt_output": str(generated_code),
                "successful": True,
                "test_cases": []
            }
            
            for test_case in test_cases:
                test_result = {"test_case": test_case, "successful": True}
                test_code = generated_code + "\n" + test_case
                
                try:
                    self._code_runner.exec(test_code)
                except Exception as e:
                    task_result["successful"] = False
                    test_result["successful"] = False
                    test_result["error"] = str(e)
                
                task_result["test_cases"].append(test_result)
            
            if task_result["successful"]:
                successful_tasks += 1
            
            print("MBPPCodeEvaluator - task_result: ", task_result)
            print("MBPPCodeEvaluator - successful_tasks: ", successful_tasks)
            print("\n\n")
            results.append(task_result)
        
        score = successful_tasks / len(self._dataset)
        
        return score, results
    
    def _few_shots_prompt(self, prompt: str, test_cases: list) -> str:
        full_prompt = prompt + "\n"
        full_prompt += "Your code should satisfy these tests:\n"
        
        for test_case in test_cases:
            full_prompt += test_case + "\n"
        
        return full_prompt
