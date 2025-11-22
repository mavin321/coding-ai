import React, { useState } from "react";
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
  Card,
  CardContent,
  CardHeader,
  Divider,
  CircularProgress,
} from "@mui/material";
import { explainCode, generateCode, refactorCode, generateTests } from "./api";

/**
 * Production‑ready, visually improved UI for the AI Coding Assistant.
 * Uses a card‑based layout, modern spacing, responsive structure,
 * and improved UX for inputs, loading states, and output display.
 */
export default function App() {
  const [mode, setMode] = useState("explain");
  const [input, setInput] = useState("");
  const [extra, setExtra] = useState("");
  const [output, setOutput] = useState("");
  const [loading, setLoading] = useState(false);

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
      if (mode === "explain") result = await explainCode(input);
      else if (mode === "generate") result = await generateCode(input);
      else if (mode === "refactor") result = await refactorCode(input);
      else if (mode === "tests") result = await generateTests(input, extra);
    } catch (error) {
      result = `An error occurred: ${error.message}`;
    }

    setOutput(result);
    setLoading(false);
  }

  return (
    <Container maxWidth="md" sx={{ py: 6 }}>
      <Box textAlign="center" mb={5}>
        <Typography variant="h3" fontWeight={700} gutterBottom>
          AI Coding Assistant
        </Typography>
        <Typography variant="h6" color="text.secondary">
          Improve, generate, refactor, and explain code with ease
        </Typography>
      </Box>

      <Card elevation={4} sx={{ borderRadius: 4 }}>
        <CardHeader
          title="Task Configuration"
          titleTypographyProps={{ variant: "h5", fontWeight: 600 }}
          sx={{ pb: 0, mt: 1 }}
        />

        <CardContent>
          {/* Mode Selection */}
          <FormControl fullWidth sx={{ mb: 3 }}>
            <InputLabel id="mode-select-label">Select Mode</InputLabel>
            <Select
              labelId="mode-select-label"
              value={mode}
              label="Select Mode"
              onChange={(e) => {
                setMode(e.target.value);
                if (e.target.value !== "tests") setExtra("");
              }}
            >
              {modes.map((m) => (
                <MenuItem key={m.value} value={m.value}>
                  {m.label}
                </MenuItem>
              ))}
            </Select>
          </FormControl>

          {/* Main Input */}
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

          {/* Tests Extra Field */}
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
            fullWidth
            onClick={handleSubmit}
            disabled={loading || !input.trim()}
            sx={{ py: 1.6, fontSize: "1.05rem", fontWeight: 600 }}
          >
            {loading ? (
              <CircularProgress size={28} color="inherit" />
            ) : (
              "Run Assistant"
            )}
          </Button>
        </CardContent>
      </Card>

      <Card elevation={3} sx={{ mt: 5, borderRadius: 4 }}>
        <CardHeader
          title="Output"
          titleTypographyProps={{ variant: "h5", fontWeight: 600 }}
        />
        <Divider />
        <CardContent>
          <Paper
            variant="outlined"
            sx={{
              p: 2,
              minHeight: 200,
              fontFamily: "monospace",
              whiteSpace: "pre-wrap",
              backgroundColor: "#fafafa",
            }}
          >
            {output || "Output will appear here..."}
          </Paper>
        </CardContent>
      </Card>
    </Container>
  );
}
