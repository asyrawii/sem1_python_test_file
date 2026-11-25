import ast
import subprocess
import sys
import math
import re
import pytest

FILE = "exercise_1.py"


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


def test_positive_condition(tree):
    assert any(
        isinstance(n, ast.If)
        and isinstance(n.test, ast.Compare)
        and isinstance(n.test.ops[0], ast.Gt)
        for n in ast.walk(tree)
    ), "Check whether radius > 0."


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

    assert numbers, "Area was not printed."

    actual = float(numbers[-1])
    expected = math.pi * radius ** 2

    assert math.isclose(
        actual, expected,
        rel_tol=0.001,
        abs_tol=0.02
    ), "Incorrect area calculation."


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

    # No numeric area should be printed
    numbers = re.findall(
        r"[-+]?\d*\.?\d+(?:[eE][-+]?\d+)?",
        result.stdout
    )

    assert not numbers, "Do not calculate or print area for non-positive radius."
