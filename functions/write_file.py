import os


def write_file(working_directory, file_path, content):
    """
    Writes content to file path
    """
    try:
        working = os.path.abspath(working_directory)
        parent = os.path.abspath(os.path.join(working, file_path))
        if parent.count(working) <= 0:
            print(
                f'Error: Cannot write to "{file_path}" as it is outside the permitted working directory'
            )
            return

        full_path = os.path.join(working, file_path)
        with open(full_path, "wt", encoding="utf8") as output_file:
            output_file.write(content)

        print(
            f'Successfully wrote to "{file_path}" ({len(content)} characters written)'
        )

    except Exception as e:
        print(f"Error: unknown error occurred, {e}")


if __name__ == "__main__":
    write_file("calculator", "lorem.txt", "test")
