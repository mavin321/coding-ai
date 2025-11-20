# model_client.py (LoRA-aware version)

import torch
from transformers import AutoTokenizer, AutoModelForCausalLM
from peft import PeftModel

from .config import MODEL_NAME, DEVICE, MAX_NEW_TOKENS, TEMPERATURE, TOP_P, TOP_K, SEED

BASE_MODEL_NAME = MODEL_NAME
LORA_PATH = "lora-output"  # where train_lora.py saved weights

_tokenizer = None
_model = None

def _load_model_if_needed():
    global _tokenizer, _model
    if _tokenizer is not None and _model is not None:
        return

    print(f"[model_client] Loading base model: {BASE_MODEL_NAME}")
    _tokenizer = AutoTokenizer.from_pretrained(BASE_MODEL_NAME)
    if _tokenizer.pad_token is None:
        _tokenizer.pad_token = _tokenizer.eos_token

    base_model = AutoModelForCausalLM.from_pretrained(BASE_MODEL_NAME)
    print(f"[model_client] Loading LoRA adapter from {LORA_PATH}")
    _model = PeftModel.from_pretrained(base_model, LORA_PATH)

    _model.to(DEVICE)
    _model.eval()
