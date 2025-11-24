import os

from google.genai import types

schema_write_file = types.FunctionDeclaration(
    name="write_file",
    description="Write or overwrite files with the provided content at provided file path",
    parameters=types.Schema(
        type=types.Type.OBJECT,
        properties={
            "file_path": types.Schema(
                type=types.Type.STRING, description="file path of the target file"
            ),
            "content": types.Schema(
                type=types.Type.STRING,
                description="the content to write into the target file",
            ),
        },
    ),
)


def write_file(working_directory, file_path, content):
    """
    Writes content to file path
    """
    try:
        working = os.path.abspath(working_directory)
        parent = os.path.abspath(os.path.join(working, file_path))
        if parent.count(working) <= 0:
            return f'Error: Cannot write to "{file_path}" as it is outside the permitted working directory'

        full_path = os.path.join(working, file_path)
        with open(full_path, "wt", encoding="utf8") as output_file:
            output_file.write(content)

        return (
            f'Successfully wrote to "{file_path}" ({len(content)} characters written)'
        )

    except Exception as e:
        return f"Error: unknown error occurred, {e}"


if __name__ == "__main__":
    write_file("calculator", "lorem.txt", "test")
