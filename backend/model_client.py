# backend/model_client.py

import torch
from transformers import AutoTokenizer, AutoModelForCausalLM
from peft import PeftModel

from backend.config import (
    MODEL_NAME,
    DEVICE,
    MAX_NEW_TOKENS,
    TEMPERATURE,
    TOP_P,
    TOP_K,
    SEED,
)

# Base model name
BASE_MODEL_NAME = MODEL_NAME

# LoRA adapter folder (created during fine-tuning)
LORA_PATH = "lora-output"

# Lazy-loaded globals
_tokenizer = None
_model = None


def _load_model_if_needed():
    """
    Loads tokenizer + base model + LoRA adapter (if present).
    Only loads once, even if called multiple times.
    """
    global _tokenizer, _model

    # Prevent re-loading
    if _tokenizer is not None and _model is not None:
        return

    print(f"[model_client] Loading tokenizer: {BASE_MODEL_NAME}")
    _tokenizer = AutoTokenizer.from_pretrained(BASE_MODEL_NAME)

    if _tokenizer.pad_token is None:
        _tokenizer.pad_token = _tokenizer.eos_token

    print(f"[model_client] Loading base model: {BASE_MODEL_NAME}")
    base_model = AutoModelForCausalLM.from_pretrained(BASE_MODEL_NAME)

    # Attempt LoRA load
    try:
        print(f"[model_client] Attempting to load LoRA adapter from: {LORA_PATH}")
        _model = PeftModel.from_pretrained(base_model, LORA_PATH)
        print("[model_client] LoRA adapter loaded successfully!")
    except Exception as e:
        print("[model_client] No LoRA adapter found, using base model only.")
        print(f"[model_client] Error: {e}")
        _model = base_model

    _model.to(DEVICE)
    _model.eval()


@torch.no_grad()
def generate_response(prompt: str) -> str:
    """
    Generates a completion from the model for a given prompt.
    Used by all FastAPI routes.
    """
    _load_model_if_needed()

    inputs = _tokenizer(
        prompt,
        return_tensors="pt",
        truncation=True,
        padding=True,
    )

    input_ids = inputs["input_ids"].to(DEVICE)
    attention_mask = inputs["attention_mask"].to(DEVICE)

    output_ids = _model.generate(
        input_ids=input_ids,
        attention_mask=attention_mask,
        max_new_tokens=MAX_NEW_TOKENS,
        temperature=TEMPERATURE,
        top_p=TOP_P,
        top_k=TOP_K,
        do_sample=True,
        pad_token_id=_tokenizer.pad_token_id,
        eos_token_id=_tokenizer.eos_token_id,
    )

    # Only grab *new* tokens
    new_tokens = output_ids[0][input_ids.shape[1]:]
    response_text = _tokenizer.decode(new_tokens, skip_special_tokens=True)

    return response_text.strip()
