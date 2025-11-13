import os
import subprocess


def run_python_file(working_directory, file_path, args=[]):
    working = os.path.abspath(working_directory)
    parent = os.path.abspath(os.path.join(working, file_path))
    if parent.count(working) <= 0:
        print(
            f'Error: Cannot execute "{file_path}" as it is outside the permitted working directory'
        )
        return

    full_path = os.path.join(working, file_path)
    if not os.path.exists(full_path):
        print(f'Error: File "{file_path}" not found.')
        return

    _, ext = os.path.splitext(full_path)
    if ".py" != ext:
        print(f'Error: "{file_path}" is not a Python file.')
        return

    commands = ["python3", full_path, *args]
    try:
        output = subprocess.run(commands, capture_output=True, timeout=30)
        stdout = output.stdout
        stderr = output.stderr
        if stdout is not None and stderr is not None:
            print(f"STDOUT: {stdout}")
            print(f"STDERR: {stderr}")
        else:
            print(f"No output produced")

        if output.returncode != 0:
            print(f"Process exited with code {output.returncode}")
    except Exception as e:
        print(f"Error: executing Python file: {e}")


if __name__ == "__main__":
    run_python_file("calculator", "main.py")
    run_python_file("calculator", "tests.py")
    run_python_file("calculator", "../main.py")
    run_python_file("calculator", "nonexistent.py")
    run_python_file("calculator", "lorem.txt")
    run_python_file("calculator", "main.py", ["3 + 5"])
