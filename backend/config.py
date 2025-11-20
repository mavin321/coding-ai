# config.py

import torch

# 👇 Choose a small-ish code model here.
# You can change this later to your fine-tuned model.
MODEL_NAME = "Salesforce/codegen-350M-multi"  # example; replace if you prefer
MAX_NEW_TOKENS = 256

# Generation settings – you can tweak
TEMPERATURE = 0.2
TOP_P = 0.9
TOP_K = 50

# Device: auto-pick GPU if available
DEVICE = "cuda" if torch.cuda.is_available() else "cpu"

# For reproducibility (optional)
SEED = 42
