# prompts.py

from textwrap import dedent

def make_explain_prompt(code: str, language: str = "python") -> str:
    return dedent(f"""
    You are an expert {language} developer.

    Task: Explain the following code ONCE in a clear, concise way suitable for a beginner.
    Do not repeat the explanation, do not restate the question, and do not generate multiple sections.

    Code:
    ```{language}
    {code}
    ```

    Provide a single explanation below.
    Explanation (one response only):
    """)


def make_generate_prompt(instruction: str, language: str = "python") -> str:
    return dedent(f"""
    You are an expert {language} developer.

    Task: Generate clean, idiomatic {language} code that satisfies the request BELOW.
    Output ONLY the final code — do not repeat the request, do not add multiple versions.

    Request:
    {instruction}

    Final {language} code (one response only):
    """)

def make_refactor_prompt(code: str, language: str = "python") -> str:
    return dedent(f"""
    You are an expert {language} developer.

    Task: Refactor the code below to be more readable, maintainable, and idiomatic.
    Then give a SHORT explanation of the changes.
    Provide ONLY ONE refactored version and ONE explanation — no repeated sections.

    Original code:
    ```{language}
    {code}
    ```

    Refactored code:
    Explanation of changes (one response only):
    """)

def make_tests_prompt(code: str, function_name: str, language: str = "python") -> str:
    return dedent(f"""
    You are an expert {language} developer and test engineer.

    Task: Write a SINGLE comprehensive test suite for the function `{function_name}`.
    Include:
    - normal cases
    - edge cases
    - error/invalid inputs

    Do NOT repeat the tests or generate multiple sets.

    Code to test:
    ```{language}
    {code}
    ```

    Final test suite (one response only):
    """)
