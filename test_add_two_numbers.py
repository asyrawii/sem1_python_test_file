import ast
import subprocess
import sys

def test_variable_x():
    with open("exercise_2.py") as f:
        tree = ast.parse(f.read())

    assert any(
        isinstance(node, ast.Assign)
        and any(
            isinstance(target, ast.Name) and target.id == "x"
            for target in node.targets
        )
        and isinstance(node.value, ast.Constant)
        and type(node.value.value) is int
        and node.value.value == 5
        for node in tree.body
    )

def test_variable_y():
    with open("exercise_2.py") as f:
        tree = ast.parse(f.read())

    assert any(
        isinstance(node, ast.Assign)
        and any(
            isinstance(target, ast.Name) and target.id == "y"
            for target in node.targets
        )
        and isinstance(node.value, ast.Constant)
        and type(node.value.value) is int
        and node.value.value == 13
        for node in tree.body
    )

def test_output():
    result = subprocess.run(
        [sys.executable, "exercise_2.py"],
        capture_output=True,
        text=True,
        timeout=5
    )

    assert result.returncode == 0
    assert result.stdout.strip() == "18"
