import ast
import subprocess
import sys
import math
import re
import pytest

FILE = "exercise_5.py"


@pytest.fixture(scope="module")
def tree():
    with open(FILE, encoding="utf-8-sig") as f:
        return ast.parse(f.read())


def test_input_prompt(tree):
    assert any(
        isinstance(n, ast.Call)
        and isinstance(n.func, ast.Name)
        and n.func.id == "input"
        and len(n.args) >= 1
        and isinstance(n.args[0], ast.Constant)
        and isinstance(n.args[0].value, str)
        and n.args[0].value.strip()
        for n in ast.walk(tree)
    ), "Use input() with a prompt."


def test_if_statement(tree):
    assert any(
        isinstance(n, ast.If)
        and isinstance(n.test, ast.Compare)
        and isinstance(n.test.left, ast.Name)
        and isinstance(n.test.ops[0], ast.Gt)
        for n in ast.walk(tree)
    ), "Use an if statement to check radius > 0."


@pytest.mark.parametrize("radius", [2, 5, 10, 7.5])
def test_positive_radius(radius):
    result = subprocess.run(
        [sys.executable, FILE],
        input=f"{radius}\n",
        capture_output=True,
        text=True,
        timeout=5
    )

    assert result.returncode == 0

    numbers = re.findall(
        r"[-+]?\d*\.?\d+(?:[eE][-+]?\d+)?",
        result.stdout
    )

    assert numbers, "No area was printed."

    actual = float(numbers[-1])
    expected = math.pi * radius ** 2

    assert math.isclose(actual, expected, rel_tol=0.001)


@pytest.mark.parametrize("radius", [0, -2, -5])
def test_non_positive_radius(radius):
    result = subprocess.run(
        [sys.executable, FILE],
        input=f"{radius}\n",
        capture_output=True,
        text=True,
        timeout=5
    )

    assert result.returncode == 0
    assert not result.stdout.strip().splitlines()[-1].strip().replace(".", "").isdigit() \
        if result.stdout.strip() else True
