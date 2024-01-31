import json
from typing import Any

from haystack_integrations.components.generators.llama_cpp import LlamaCppGenerator

from lib import LLM
from testing import LLMTester

__all__ = "test_llama_cpp_n", "test_llama_cpp_n_dump", "parse_tokens_per_second"

def _test_llama_cpp_n(prompt_template: str, prompt: str, run_n: int, *args, **kwargs) -> LLMTester:
    generator = LlamaCppGenerator(*args, **kwargs)
    llm = LLM.from_generator(generator)

    tester = LLMTester(llm)
    tester.run_n(run_n, prompt_template, prompt)

    return tester

def test_llama_cpp_n(prompt_template: str, prompt: str, run_n: int, *args, **kwargs) -> dict[str, Any]:
    return _test_llama_cpp_n(prompt_template, prompt, run_n, *args, **kwargs).to_dict()

def test_llama_cpp_n_dump(prompt_template: str, prompt: str, run_n: int, dump_path: str, *args, **kwargs) -> None:
    _test_llama_cpp_n(prompt_template, prompt, run_n, *args, **kwargs).dump(dump_path)

def parse_tokens_per_second(file_path: str) -> list[tuple[str, float]]:
    with open(file_path, "r") as file:
        test_data: dict[str, Any] = json.load(file)

    result: list[tuple[str, float]] = []
    for file_name, responses in test_data.items():
        data_length = len(responses)
        tps_sum = sum(response["token_count"] / response["generation_time"] for response in responses)
        result.append((file_name, tps_sum / data_length))

    return result