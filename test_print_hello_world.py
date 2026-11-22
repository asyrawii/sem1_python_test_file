import subprocess
import sys

def test_hello_world():
    result = subprocess.run(
        [sys.executable, "exercise_1.py"],
        capture_output=True,
        text=True,
        timeout=5
    )

    assert result.returncode == 0, "Program failed to run."

    assert result.stdout.strip() == "Hello, world!", (
        "Incorrect output!\n"
        "Expected: Hello, world!\n"
        f"Received: {result.stdout.strip()}"
    )
