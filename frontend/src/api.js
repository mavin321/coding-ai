import axios from "axios";

const API_BASE = "http://localhost:8000/api/ai";

export async function explainCode(code, language = "python") {
  const res = await axios.post(`${API_BASE}/explain`, {
    code,
    language,
  });
  return res.data.response;
}

export async function generateCode(instruction, language = "python") {
  const res = await axios.post(`${API_BASE}/generate`, {
    instruction,
    language,
  });
  return res.data.response;
}

export async function refactorCode(code, language = "python") {
  const res = await axios.post(`${API_BASE}/refactor`, {
    code,
    language,
  });
  return res.data.response;
}

export async function generateTests(code, functionName, language = "python") {
  const res = await axios.post(`${API_BASE}/tests`, {
    code,
    function_name: functionName,
    language,
  });
  return res.data.response;
}
