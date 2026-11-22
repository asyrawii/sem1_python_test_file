import ast
import subprocess
import sys
import pytest

FILE = "exercise_3.py"


def test_name_input_output():

    with open(FILE, encoding="utf-8-sig") as f:
        source = f.read()

    try:
        tree = ast.parse(source)
    except SyntaxError:
        pytest.fail("Syntax error.", pytrace=False)

    # Check input() with a prompt
    input_calls = [
        node for node in ast.walk(tree)
        if isinstance(node, ast.Call)
        and isinstance(node.func, ast.Name)
        and node.func.id == "input"
    ]

    assert any(
        len(node.args) == 1
        and isinstance(node.args[0], ast.Constant)
        and isinstance(node.args[0].value, str)
        and node.args[0].value.strip()
        for node in input_calls
    ), "Use input() with a prompt."

    # Check print()
    assert any(
        isinstance(node, ast.Call)
        and isinstance(node.func, ast.Name)
        and node.func.id == "print"
        for node in ast.walk(tree)
    ), "Use print()."

    # Test different names
    for name in ["Ali", "Siti Aminah", "John123"]:

        result = subprocess.run(
            [sys.executable, FILE],
            input=name + "\n",
            capture_output=True,
            text=True,
            timeout=5
        )

        assert result.returncode == 0, "Program failed."

        # Remove the input prompt from the output
        prompts = [
            node.args[0].value
            for node in input_calls
            if len(node.args) == 1
            and isinstance(node.args[0], ast.Constant)
            and isinstance(node.args[0].value, str)
        ]

        output = result.stdout

        for prompt in prompts:
            output = output.replace(prompt, "", 1)

        assert output.strip() == name, (
            "The program must print the entered name."
        )
