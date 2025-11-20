# cli.py

import argparse
from pathlib import Path
from typing import Tuple

from backend.model_client import generate_response
from backend.prompts import (
    make_explain_prompt,
    make_generate_prompt,
    make_refactor_prompt,
    make_tests_prompt,
)

LANGUAGE_EXT_MAP = {
    ".py": "python",
    ".js": "javascript",
    ".ts": "typescript",
    ".java": "java",
    ".cpp": "cpp",
    ".c": "c",
    ".cs": "csharp",
}


def detect_language_from_path(path: Path) -> str:
    return LANGUAGE_EXT_MAP.get(path.suffix.lower(), "python")


def read_code_segment(path: Path, start_line: int, end_line: int) -> str:
    lines = path.read_text(encoding="utf-8").splitlines()
    # Clamp to valid range
    start_line = max(1, start_line)
    end_line = min(len(lines), end_line)
    segment = "\n".join(lines[start_line - 1 : end_line])
    return segment


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="AI Code Assistant (Level 1 & Level 2 ready)"
    )

    subparsers = parser.add_subparsers(dest="command", required=True)

    # explain
    explain_parser = subparsers.add_parser("explain", help="Explain a code segment")
    explain_parser.add_argument("file", help="Path to the code file")
    explain_parser.add_argument("--start", type=int, default=1, help="Start line (1-based)")
    explain_parser.add_argument("--end", type=int, default=100, help="End line (inclusive)")

    # generate
    gen_parser = subparsers.add_parser("generate", help="Generate code from instruction")
    gen_parser.add_argument("instruction", help="Text describing what you want")

    # refactor
    ref_parser = subparsers.add_parser("refactor", help="Refactor a code segment")
    ref_parser.add_argument("file", help="Path to the code file")
    ref_parser.add_argument("--start", type=int, default=1)
    ref_parser.add_argument("--end", type=int, default=100)

    # tests
    tests_parser = subparsers.add_parser("tests", help="Generate unit tests for a function")
    tests_parser.add_argument("file", help="Path to the code file")
    tests_parser.add_argument("function_name", help="Name of the function to test")
    tests_parser.add_argument("--start", type=int, default=1)
    tests_parser.add_argument("--end", type=int, default=200)

    return parser.parse_args()


def handle_explain(file: str, start: int, end: int):
    path = Path(file)
    language = detect_language_from_path(path)
    code = read_code_segment(path, start, end)
    prompt = make_explain_prompt(code, language=language)
    output = generate_response(prompt)
    print("\n=== Explanation ===\n")
    print(output)


def handle_generate(instruction: str):
    # default language is python; you could add a flag to pick others
    prompt = make_generate_prompt(instruction, language="python")
    output = generate_response(prompt)
    print("\n=== Generated Code ===\n")
    print(output)
    print("\n```")  # close code fence if the model didn't


def handle_refactor(file: str, start: int, end: int):
    path = Path(file)
    language = detect_language_from_path(path)
    code = read_code_segment(path, start, end)
    prompt = make_refactor_prompt(code, language=language)
    output = generate_response(prompt)
    print("\n=== Refactor Suggestion ===\n")
    print(output)


def handle_tests(file: str, function_name: str, start: int, end: int):
    path = Path(file)
    language = detect_language_from_path(path)
    code = read_code_segment(path, start, end)
    prompt = make_tests_prompt(code, function_name=function_name, language=language)
    output = generate_response(prompt)
    print("\n=== Suggested Tests ===\n")
    print(output)


def main():
    args = parse_args()

    if args.command == "explain":
        handle_explain(args.file, args.start, args.end)
    elif args.command == "generate":
        handle_generate(args.instruction)
    elif args.command == "refactor":
        handle_refactor(args.file, args.start, args.end)
    elif args.command == "tests":
        handle_tests(args.file, args.function_name, args.start, args.end)
    else:
        raise ValueError(f"Unknown command: {args.command}")


if __name__ == "__main__":
    main()
