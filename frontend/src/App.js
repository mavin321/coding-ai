import React, { useState } from "react";
import { explainCode, generateCode, refactorCode, generateTests } from "./api";

function App() {
  const [mode, setMode] = useState("explain");

  const [input, setInput] = useState("");
  const [extra, setExtra] = useState(""); // used only for "tests" mode
  const [output, setOutput] = useState("");

  async function handleSubmit() {
    let result = "";

    if (mode === "explain") {
      result = await explainCode(input);
    } else if (mode === "generate") {
      result = await generateCode(input);
    } else if (mode === "refactor") {
      result = await refactorCode(input);
    } else if (mode === "tests") {
      result = await generateTests(input, extra);
    }

    setOutput(result);
  }

  return (
    <div style={{ padding: 30, fontFamily: "Arial" }}>
      <h1>AI Coding Assistant</h1>

      <select onChange={(e) => setMode(e.target.value)} value={mode}>
        <option value="explain">Explain Code</option>
        <option value="generate">Generate Code</option>
        <option value="refactor">Refactor Code</option>
        <option value="tests">Generate Tests</option>
      </select>

      <br />
      <br />

      <textarea
        rows="10"
        cols="80"
        placeholder={
          mode === "generate"
            ? "Describe the code you want me to generate..."
            : "Paste your code here..."
        }
        value={input}
        onChange={(e) => setInput(e.target.value)}
      />

      {mode === "tests" && (
        <>
          <br />
          <br />
          <input
            placeholder="Function Name"
            value={extra}
            onChange={(e) => setExtra(e.target.value)}
          />
        </>
      )}

      <br />
      <br />

      <button onClick={handleSubmit}>Run</button>

      <h2>Output:</h2>
      <pre
        style={{ background: "#f4f4f4", padding: 20, whiteSpace: "pre-wrap" }}
      >
        {output}
      </pre>
    </div>
  );
}

export default App;
