import os

from google.genai import types

schema_get_files_info = types.FunctionDeclaration(
    name="get_files_info",
    description="Lists files in the specified directory along with their sizes, constrained to the working directory.",
    parameters=types.Schema(
        type=types.Type.OBJECT,
        properties={
            "directory": types.Schema(
                type=types.Type.STRING,
                description="The directory to list files from, relative to the working directory. If not provided, lists files in the working directory itself.",
            )
        },
    ),
)


def get_files_info(working_directory, directory="."):
    """
    List files and directorys from the provided directory
    """
    try:
        working = os.path.abspath(working_directory)
        parent = os.path.abspath(os.path.join(working, directory))
        if parent.count(working) <= 0:
            print(
                f'Error: Cannot list "{directory}" as it is outside the permitted working directory'
            )
            return

        if not os.path.isdir(parent):
            print(f'Error: "{directory}" is not a directory')
            return

        full_path = os.path.join(working, directory)
        dir_contents = os.listdir(full_path)
        for item in dir_contents:
            file_size = os.path.getsize(os.path.join(working, directory, item))
            is_dir = os.path.isdir(os.path.join(working, directory, item))
            print(f"- {item}: file_size={file_size}, is_dir={is_dir}")
    except Exception as e:
        print(f"Error: unknown error has occurred, {e}")
