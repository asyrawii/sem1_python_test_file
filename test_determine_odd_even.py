import ast
import subprocess
import sys
import pytest

FILE = "exercise_6.py"

@pytest.fixture
def tree():
    with open(FILE, encoding="utf-8-sig") as f:
        return ast.parse(f.read())


def test_input_prompt(tree):
    inputs = [
        node for node in ast.walk(tree)
        if isinstance(node, ast.Call)
        and isinstance(node.func, ast.Name)
        and node.func.id == "input"
    ]

    assert inputs, "input() is required"

    assert any(
        node.args
        and isinstance(node.args[0], ast.Constant)
        and isinstance(node.args[0].value, str)
        and node.args[0].value.strip()
        for node in inputs
    ), "A non-empty input prompt is required"


def test_if_else(tree):
    conditions = [
        node for node in ast.walk(tree)
        if isinstance(node, ast.If) and node.orelse
    ]

    assert conditions, "An if-else statement is required"


@pytest.mark.parametrize("number, expected", [
    (2, "Even"),
    (5, "Odd"),
    (10, "Even"),
    (7, "Odd"),
    (0, "Even"),
    (-4, "Even"),
    (-3, "Odd")
])
def test_odd_even(number, expected):
    result = subprocess.run(
        [sys.executable, FILE],
        input=f"{number}\n",
        capture_output=True,
        text=True,
        timeout=5
    )

    assert result.returncode == 0
    assert result.stdout.strip().splitlines()[-1] == expected
