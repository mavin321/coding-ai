# prompts.py

from textwrap import dedent

def make_explain_prompt(code: str, language: str = "python") -> str:
    return dedent(f"""
    You are an expert {language} developer.
    Explain the following code in clear, simple language for a beginner.
    Include what it does, how it works, and any potential issues.

    ```{language}
    {code}
    ```

    Explanation:
    """)

def make_generate_prompt(instruction: str, language: str = "python") -> str:
    return dedent(f"""
    You are an expert {language} developer.
    Write idiomatic, clean {language} code that satisfies the following request.
    Add minimal helpful comments where appropriate.

    Request:
    {instruction}

    Code:
    """)

def make_refactor_prompt(code: str, language: str = "python") -> str:
    return dedent(f"""
    You are an expert {language} developer.
    Refactor the following code to be more readable, maintainable, and Pythonic.
    Preserve behavior. Then briefly explain what you changed.

    Original code:
    {code}

    Refactored code and explanation:
    """)

def make_tests_prompt(code: str, function_name: str, language: str = "python") -> str:
    return dedent(f"""
    You are an expert {language} developer and test engineer.
    Given the following {language} code, write thorough unit tests for the function `{function_name}`.

    Focus on:
    - normal cases
    - edge cases
    - invalid input where appropriate

    Use a standard testing framework (e.g., pytest for Python).

    Code:
    {code}

    Tests:
    """)

