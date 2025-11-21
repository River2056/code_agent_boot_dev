import os

from google.genai import types

from functions.config import MAX_CHARS

schema_get_file_content = types.FunctionDeclaration(
    name="get_file_content",
    description="Read file contents from the provided file path",
    parameters=types.Schema(
        type=types.Type.OBJECT,
        properties={
            "file_path": types.Schema(
                type=types.Type.STRING, description="the file path of the target file"
            )
        },
    ),
)


def get_file_content(working_directory, file_path):
    """
    Read contents from a file and prints to standard output
    """
    try:
        working = os.path.abspath(working_directory)
        parent = os.path.abspath(os.path.join(working, file_path))
        if parent.count(working) <= 0:
            print(
                f'Error: Cannot read "{file_path}" as it is outside the permitted working directory'
            )
            return

        if not os.path.isfile(parent):
            print(f'Error: File not found or is not a regular file: "{file_path}"')
            return

        full_path = os.path.join(working, file_path)
        with open(full_path, encoding="utf8") as file:
            contents = file.read(MAX_CHARS)
            if len(contents) == MAX_CHARS:
                contents += f'[...File "{file_path}" truncated at 10000 characters]'
            print(contents)

    except Exception as e:
        print(f"Error: unknown error has occurred, {e}")
