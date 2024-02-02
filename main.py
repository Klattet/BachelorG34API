import gc, os, traceback

from testing import test_llama_cpp_n_dump, parse_tokens_per_second
from testing import LLMTester
from lib import LLM, LLamaCpp

prompt_template = """\
You are a student assistant. You must answer in a way that helps students arrive at the correct answer themselves.
The students are all programming and software engineer students. You will never give a direct solution to students' tasks.
Help the student learn in a way that is natural for a human conversation.

Student question: I need help with a task for school. {{prompt}}

Answer: \
"""

prompt = "How can I create a class in Java that represents a celestial body, and create subclasses that represent things like planets and moons?"

test_data_path = r"./data/test_data.json"
test_tps_path = r"./data/test_tps.json"
test_responses_path = r"./data/test_responses.txt"
llm_path = r"E:\LLM"

def test_llamacpp_model(model_path: str):
    try:
        print("Loading:", model_path)
        llm = LLamaCpp(
            model_path = model_path,
            model_kwargs = {"verbose": False, "n_gpu_layers": -1},
            generation_kwargs = {"max_tokens": 600, "temperature": 0.25}
        )
        print("Testing:", model_path)
        tester = LLMTester(llm)
        tester.run_n(10, prompt_template, prompt)
        tester.dump_all(test_data_path)
        tester.dump_average_tps(test_tps_path)
        tester.dump_format_responses(test_responses_path)
        print("Finished:", model_path)
    except Exception:
        print("Failed:", model_path)
        print(traceback.format_exc())

def test_models():
    for root, dirs, files in os.walk(llm_path):
        for file in files:
            model_path = os.path.join(root, file)
            test_llamacpp_model(model_path)
            gc.collect()


def parse_test():
    tps_list = parse_tokens_per_second(test_data_path)
    sorted_tps = sorted(tps_list, key = lambda e: e[1], reverse = True)

    for file, tps in sorted_tps:
        print(f"{file:45} | Average tps:{tps:.3f}")

if __name__ == "__main__":
    test_llamacpp_model(r"C:\Users\Lex\Downloads\RWKV-v5-Eagle-World-7B-v2-20240128-ctx4096.pth")