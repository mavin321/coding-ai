# 🚀 AI Coding Assistant

A full-stack AI-powered coding assistant built with:

- **Python (FastAPI)** for the backend
- **React** for the frontend
- **PyTorch + HuggingFace Transformers** for the AI model
- **LoRA fine-tuning** support for custom training

This tool can:

- ✨ Explain code
- ✨ Generate code
- ✨ Refactor code
- ✨ Create unit tests
- ✨ Fine-tune itself on your own dataset to improve performance

---

# 📦 Features

### 🧠 AI-Powered Code Assistant

Your model can perform:

| Feature              | Description                                     |
| -------------------- | ----------------------------------------------- |
| **Explain code**     | Breaks down code into human explanations        |
| **Generate code**    | Creates code from natural-language instructions |
| **Refactor code**    | Produces cleaner, more Pythonic versions        |
| **Write unit tests** | Generates test suites for any function          |

The AI backend uses your own model defined in `backend/model_client.py`
and can be swapped for a fine-tuned LoRA model.

---

### 🌐 Full Web Application (React + FastAPI)

- Beautiful browser interface
- Interactive forms
- Text areas for input/output
- API calls to backend via Axios
- Real-time responses

---

### 🏋️‍♂ Fine-tuning Support (Level 2)

Train the AI on your own dataset using:

- HuggingFace Transformers
- LoRA adapters (PEFT)
- Custom instruction-based datasets

Training code lives inside:

```
backend/finetune/
```

---

# 📂 Project Structure

```
coding-ai/
│
├── backend/
│   ├── __init__.py
│   ├── main.py
│   ├── model_client.py
│   ├── config.py
│   ├── prompts.py
│   └── routers/
│       ├── __init__.py
│       └── ai.py
│
├── frontend/
│   ├── package.json
│   ├── public/
│   └── src/
│       ├── App.js
│       ├── api.js
│       └── index.js
│
├── data/
│   ├── train.jsonl
│   └── val.jsonl
│
└── README.md
```

---

# 🛠️ Installation Instructions

This project has **two parts**:

- Backend (FastAPI + Model)
- Frontend (React App)

Follow the steps below.

---

# ⚙️ Backend Setup (FastAPI + Model)

### 1. Create virtual environment

```bash
cd coding-ai
python -m venv venv
```

Activate it:

**Windows**

```bash
venv\Scripts\activate
```

**Mac/Linux**

```bash
source venv/bin/activate
```

---

### 2. Install backend dependencies

Inside `venv`, run:

```bash
pip install -r backend/requirements.txt
```

If you don't have a requirements file, install manually:

```bash
pip install fastapi uvicorn transformers torch peft datasets accelerate
```

---

### 3. Start the backend server

Make sure you are inside the **project root** (`coding-ai`), then run:

```bash
uvicorn backend.main:app --reload --port 8000
```

Your API will run at:

```
http://localhost:8000
```

API docs:

```
http://localhost:8000/docs
```

---

# 🌐 Frontend Setup (React)

### 1. Install dependencies

```bash
cd frontend
npm install
```

### 2. Run frontend

```bash
npm start
```

Frontend will open at:

```
http://localhost:3000
```

---

# 🔌 How Backend & Frontend Communicate

The frontend sends JSON requests to FastAPI:

```
POST /api/ai/explain
POST /api/ai/generate
POST /api/ai/refactor
POST /api/ai/tests
```

Each returns:

```json
{
  "response": "...AI output..."
}
```

---

# 🧠 AI Model Configuration

Your model is defined in:

```
backend/config.py
```

Change:

```python
MODEL_NAME = "Salesforce/codegen-350M-multi"
```

to your preferred model.

---

# 🧩 Prompts

The prompts that control model behavior are stored in:

```
backend/prompts.py
```

You can edit:

- Explanation style
- Refactor style
- Test structure
- Code generation quality

---

# 🏋️ Fine-Tuning (Level 2)

Fine-tuning uses:

- HuggingFace Datasets
- LoRA (PEFT)
- Training scripts in:

```
backend/finetune/
```

### 1. Add training data

Format (JSONL):

```json
{
  "instruction": "Explain this code",
  "input": "def x(a): return a+1",
  "output": "Adds 1 to a"
}
```

Place files in:

```
data/train.jsonl
data/val.jsonl
```

---

### 2. Run fine-tuning

```bash
cd backend/finetune
python train_lora.py
```

Your LoRA weights will be saved in:

```
lora-output/
```

---

### 3. Use fine-tuned model

Edit `backend/model_client.py`:

```python
LORA_PATH = "lora-output"
```

Now your backend will load the trained model.

---

# 🧪 Example API Calls

### Explain code

```
POST http://localhost:8000/api/ai/explain
{
  "code": "def add(a,b): return a+b"
}
```

### Generate code

```
POST http://localhost:8000/api/ai/generate
{
  "instruction": "Write a function that checks if a number is prime."
}
```

---

# 🚀 Future Improvements (Planned)

- Streaming responses (like ChatGPT typing)
- Monaco editor (VS Code in browser)
- File uploads
- Multi-file analysis
- Dark mode
- Project-level code assistance
- Python execution sandbox

---

# 🤝 Contributing

Pull requests welcome!
Always test backend + frontend together before submitting changes.

---

# 📝 License

MIT License (Free to use, modify, distribute)

---

# 🎉 Final Notes

This project is a **full standalone AI developer assistant**.
You can:

- Run it locally
- Deploy it on a server
- Improve the model through training
- Extend the UI
