import ast
import subprocess
import sys
import pytest

def test_sum_two_numbers():

    with open("exercise_2.py", encoding="utf-8-sig") as f:
        source = f.read()

    try:
        tree = ast.parse(source)
    except SyntaxError:
        pytest.fail("Syntax error in your program.", pytrace=False)

    # Check variable declarations
    variables = {}

    for node in tree.body:
        if isinstance(node, ast.Assign):
            for target in node.targets:
                if isinstance(target, ast.Name):
                    if isinstance(node.value, ast.Constant):
                        variables[target.id] = node.value.value

    assert variables.get("x") == 5, (
        "Variable x must be declared with value 5."
    )

    assert variables.get("y") == 13, (
        "Variable y must be declared with value 13."
    )

    # Run student's program
    result = subprocess.run(
        [sys.executable, "exercise_2.py"],
        capture_output=True,
        text=True,
        timeout=5
    )

    assert result.returncode == 0, "Program failed to run."

    assert result.stdout.strip() == "18", (
        "Incorrect output! Expected: 18"
    )
