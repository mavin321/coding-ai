# finetune/dataset.py

from datasets import load_dataset
from typing import Dict

def load_instruction_dataset(path: str) -> Dict:
    """
    Loads a JSONL instruction dataset from a local path.
    """
    dataset = load_dataset("json", data_files={"train": f"{path}/train.jsonl",
                                              "validation": f"{path}/val.jsonl"})
    return dataset


def format_example(example: Dict) -> str:
    """
    Turns one {instruction, input, output} into a single text string for a causal LM.
    We'll use a simple chat-like format.
    """
    instruction = example.get("instruction", "").strip()
    inp = example.get("input", "").strip()
    output = example.get("output", "").strip()

    if inp:
        # instruction + input
        prompt = (
            "### Instruction:\n"
            f"{instruction}\n\n"
            "### Input:\n"
            f"{inp}\n\n"
            "### Response:\n"
        )
    else:
        prompt = (
            "### Instruction:\n"
            f"{instruction}\n\n"
            "### Response:\n"
        )

    # For training we concatenate prompt + output
    full_text = prompt + output
    return full_text
