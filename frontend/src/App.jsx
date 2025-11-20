import React, { useState } from "react";
// Import necessary MUI components
import {
  Container,
  Box,
  Typography,
  TextField,
  Button,
  FormControl,
  Select,
  MenuItem,
  InputLabel,
  Paper,
  CssBaseline, // Optional: for consistent baseline styling
} from "@mui/material";

// Placeholder for your API functions (ensure these are correctly imported in your actual project)
// import { explainCode, generateCode, refactorCode, generateTests } from "./api";

// Mock API functions for demonstration:
const explainCode = async (code) => `Explanation for: \n${code}`;
const generateCode = async (prompt) =>
  `Generated code based on prompt: \n${prompt}`;
const refactorCode = async (code) => `Refactored code for: \n${code}`;
const generateTests = async (code, funcName) =>
  `Tests for function '${funcName}' in code: \n${code}`;

function App() {
  const [mode, setMode] = useState("explain");
  const [input, setInput] = useState("");
  const [extra, setExtra] = useState(""); // for function name
  const [output, setOutput] = useState("");
  const [loading, setLoading] = useState(false); // State for loading indicator

  const modes = [
    { value: "explain", label: "Explain Code" },
    { value: "generate", label: "Generate Code" },
    { value: "refactor", label: "Refactor Code" },
    { value: "tests", label: "Generate Tests" },
  ];

  const inputPlaceholder =
    mode === "generate"
      ? "Describe the code you want..."
      : "Paste code here...";

  async function handleSubmit() {
    setLoading(true);
    let result = "";

    try {
      if (mode === "explain") {
        result = await explainCode(input);
      } else if (mode === "generate") {
        result = await generateCode(input);
      } else if (mode === "refactor") {
        result = await refactorCode(input);
      } else if (mode === "tests") {
        result = await generateTests(input, extra);
      }
    } catch (error) {
      result = `An error occurred: ${error.message}`;
    }

    setOutput(result);
    setLoading(false);
  }

  return (
    // <CssBaseline /> is recommended if you use the MUI theme/styles globally
    <Container maxWidth="md">
      <Box sx={{ my: 4, textAlign: "center" }}>
        <Typography variant="h3" component="h1" gutterBottom color="primary">
          🤖 AI Coding Assistant
        </Typography>
      </Box>

      <Paper elevation={3} sx={{ p: 3 }}>
        {/* Mode Selection */}
        <FormControl fullWidth sx={{ mb: 3 }}>
          <InputLabel id="mode-select-label">Select Mode</InputLabel>
          <Select
            labelId="mode-select-label"
            id="mode-select"
            value={mode}
            label="Select Mode"
            onChange={(e) => {
              setMode(e.target.value);
              // Clear extra field when mode changes, unless it's 'tests'
              if (e.target.value !== "tests") {
                setExtra("");
              }
            }}
          >
            {modes.map((m) => (
              <MenuItem key={m.value} value={m.value}>
                {m.label}
              </MenuItem>
            ))}
          </Select>
        </FormControl>

        {/* Main Input Area */}
        <TextField
          fullWidth
          multiline
          rows={10}
          label={mode === "generate" ? "Code Description" : "Source Code"}
          placeholder={inputPlaceholder}
          value={input}
          onChange={(e) => setInput(e.target.value)}
          variant="outlined"
          sx={{ mb: 3 }}
        />

        {/* Extra Input for Generate Tests Mode */}
        {mode === "tests" && (
          <TextField
            fullWidth
            label="Function Name (Required for Tests)"
            placeholder="e.g., calculateTotal"
            value={extra}
            onChange={(e) => setExtra(e.target.value)}
            variant="outlined"
            sx={{ mb: 3 }}
          />
        )}

        {/* Submit Button */}
        <Button
          variant="contained"
          size="large"
          onClick={handleSubmit}
          disabled={loading}
          fullWidth
          sx={{ mb: 4, py: 1.5 }} // py adds vertical padding to make button taller
        >
          {loading ? "Running..." : "Run Assistant"}
        </Button>

        <Typography variant="h5" component="h2" gutterBottom>
          🚀 Output:
        </Typography>

        {/* Output Area */}
        <Paper
          variant="outlined"
          sx={{
            p: 2,
            backgroundColor: "action.hover", // Light background for code
            whiteSpace: "pre-wrap",
            fontFamily: "monospace",
            minHeight: 150, // Ensure a minimum height
          }}
        >
          {output || "Output will appear here..."}
        </Paper>
      </Paper>
    </Container>
  );
}

export default App;
