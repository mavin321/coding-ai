# finetune/train_lora.py

import os
from dataclasses import dataclass
from typing import Dict, List

import torch
from datasets import DatasetDict
from transformers import (
    AutoModelForCausalLM,
    AutoTokenizer,
    TrainingArguments,
    Trainer,
    DataCollatorForLanguageModeling,
)
from peft import LoraConfig, get_peft_model

from dataset import load_instruction_dataset, format_example
from backend.config import MODEL_NAME, DEVICE, SEED


@dataclass
class FinetuneConfig:
    data_path: str = "data"
    output_dir: str = "lora-output"
    num_train_epochs: int = 3
    per_device_train_batch_size: int = 1
    per_device_eval_batch_size: int = 1
    learning_rate: float = 2e-4
    warmup_steps: int = 50
    logging_steps: int = 10
    save_steps: int = 100
    max_seq_length: int = 512


def tokenize_function(example, tokenizer, max_seq_length: int):
    text = format_example(example)
    return tokenizer(
        text,
        truncation=True,
        max_length=max_seq_length,
        padding="max_length",
    )


def main():
    cfg = FinetuneConfig()
    torch.manual_seed(SEED)

    print(f"[finetune] Loading base model: {MODEL_NAME}")
    tokenizer = AutoTokenizer.from_pretrained(MODEL_NAME)
    if tokenizer.pad_token is None:
        tokenizer.pad_token = tokenizer.eos_token

    base_model = AutoModelForCausalLM.from_pretrained(MODEL_NAME)
    base_model.to(DEVICE)

    # PEFT / LoRA config
    lora_config = LoraConfig(
        r=8,                      # rank
        lora_alpha=16,
        target_modules=["q_proj", "v_proj", "k_proj", "o_proj"],  # depends on model; adjust if needed
        lora_dropout=0.05,
        bias="none",
        task_type="CAUSAL_LM",
    )

    model = get_peft_model(base_model, lora_config)
    model.print_trainable_parameters()

    print("[finetune] Loading dataset...")
    dataset_dict: DatasetDict = load_instruction_dataset(cfg.data_path)

    def tok_fn(example):
        return tokenize_function(example, tokenizer, cfg.max_seq_length)

    tokenized = dataset_dict.map(tok_fn, batched=False)

    data_collator = DataCollatorForLanguageModeling(
        tokenizer=tokenizer,
        mlm=False,
    )

    training_args = TrainingArguments(
        output_dir=cfg.output_dir,
        num_train_epochs=cfg.num_train_epochs,
        per_device_train_batch_size=cfg.per_device_train_batch_size,
        per_device_eval_batch_size=cfg.per_device_eval_batch_size,
        learning_rate=cfg.learning_rate,
        warmup_steps=cfg.warmup_steps,
        logging_steps=cfg.logging_steps,
        save_steps=cfg.save_steps,
        evaluation_strategy="steps",
        eval_steps=cfg.save_steps,
        weight_decay=0.01,
        fp16=torch.cuda.is_available(),
        report_to=[],
        seed=SEED,
    )

    trainer = Trainer(
        model=model,
        args=training_args,
        train_dataset=tokenized["train"],
        eval_dataset=tokenized["validation"],
        data_collator=data_collator,
    )

    print("[finetune] Starting training...")
    trainer.train()

    print(f"[finetune] Saving LoRA model to {cfg.output_dir}")
    trainer.save_model(cfg.output_dir)
    tokenizer.save_pretrained(cfg.output_dir)


if __name__ == "__main__":
    main()
