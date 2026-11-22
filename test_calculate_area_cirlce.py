import ast
import subprocess
import sys
import math
import re
import pytest

FILE = "exercise_4.py"


def test_input_prompt():
    with open(FILE, encoding="utf-8-sig") as f:
        tree = ast.parse(f.read())

    assert any(
        isinstance(node, ast.Call)
        and isinstance(node.func, ast.Name)
        and node.func.id == "input"
        and len(node.args) >= 1
        and isinstance(node.args[0], ast.Constant)
        and isinstance(node.args[0].value, str)
        and node.args[0].value.strip()
        for node in ast.walk(tree)
    ), "Use input() with a prompt."


@pytest.mark.parametrize("radius", [2, 5, 10, 7.5, 0, 1])
def test_circle_area(radius):

    result = subprocess.run(
        [sys.executable, FILE],
        input=f"{radius}\n",
        capture_output=True,
        text=True,
        timeout=5
    )

    assert result.returncode == 0, "Program failed to run."

    # Extract numeric output from last line
    output = result.stdout.strip().splitlines()[-1]

    numbers = re.findall(
        r"-?\d+(?:\.\d+)?",
        output
    )

    assert numbers, "No numeric output found."

    actual = float(numbers[-1])
    expected = math.pi * radius ** 2

    assert math.isclose(
        actual,
        expected,
        rel_tol=0.001,
        abs_tol=0.02
    ), (
        f"Radius: {radius}\n"
        f"Expected: {expected:.4f}\n"
        f"Received: {actual:.4f}"
    )
