from typing import Any, Self, Sequence, Iterator, Iterable
from abc import abstractmethod, ABCMeta
from dataclasses import dataclass
from time import perf_counter
from pprint import pprint

from llama_cpp import Llama, CreateCompletionStreamResponse, CreateCompletionResponse


__all__ = "LLMResult",


type LlamaCppResult = CreateCompletionResponse | Iterator[CreateCompletionStreamResponse]


# Using a dataclass to save info about each LLM prompt run.
# Use slots for performance because there's no reason not to.
@dataclass(slots = True)
class Result:
    model_id: str
    model_path: str
    prompt_text: str
    response_text: str | Iterator[str]
    prompt_token_count: int
    response_token_count: int
    total_token_count: int
    generation_time: float
    finish_reason: str

class LLM(Llama):

    def __init__(self, model_path: str, **kwargs):
        super().__init__(model_path, **kwargs)

    def __call__(self, *args, **kwargs) -> Result:
        ...


def test():

    llm = Llama(
        model_path = "D:/LLM/orca-2-7b.Q4_K_M.gguf",
        n_ctx = 0,
        n_threads = 12
    )

    prompt = "Tell me a hilarious programming joke."

    result = llm(
        prompt = prompt,
        max_tokens = 1000,
        stream = True
    )

    stream_result = StreamResult(result)

    for chunk in stream_result:
        pprint(chunk)

test()

