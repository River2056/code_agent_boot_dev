import os
import sys

from dotenv import load_dotenv
from google import genai
from google.genai import types

from functions.get_files_info import schema_get_files_info, get_files_info
from functions.get_file_content import schema_get_file_content, get_file_content
from functions.write_file import schema_write_file, write_file
from functions.run_python_file import schema_run_python_file, run_python_file
from functions.call_functions import call_function


def main():
    args = sys.argv[1:]
    if len(args) <= 0:
        print("please provide prompt! aborting...")
        sys.exit(1)

    # check for verbose
    is_verbose = len(list(filter(lambda x: x == "--verbose", args))) > 0

    user_prompt = args[0]
    if is_verbose:
        print(f"User prompt: {user_prompt}")

    load_dotenv()
    api_key = os.environ.get("GEMINI_API_KEY")

    # available functions
    available_functions_schema = types.Tool(
        function_declarations=[
            schema_get_files_info,
            schema_get_file_content,
            schema_write_file,
            schema_run_python_file,
        ]
    )

    # system prompt
    system_prompt = """
        You are a helpful AI coding agent.

        When a user asks a question or makes a request, make a function call plan. You can perform the following operations:

        - List files and directories

        - Read file contents

        - Execute Python files with optional arguments

        - Write or overwrite files

        All paths you provide should be relative to the working directory. You do not need to specify the working directory in your function calls as it is automatically injected for security reasons.
    """

    # messages
    messages = [types.Content(role="user", parts=[types.Part(text=user_prompt)])]

    # initialize client
    client = genai.Client(api_key=api_key)
    res = client.models.generate_content(
        model="gemini-2.0-flash-001",
        contents=messages,
        config=types.GenerateContentConfig(
            tools=[available_functions_schema], system_instruction=system_prompt
        ),
    )

    token_count = res.usage_metadata.prompt_token_count if res.usage_metadata else 0
    response_tokens = res.usage_metadata.total_token_count if res.usage_metadata else 0
    response = res.text or ""
    function_calls = res.function_calls if res.function_calls else []

    if is_verbose:
        print(f"Prompt tokens: {token_count}")
        print(f"Response tokens: {response_tokens}")
    print(f"Response: {response}")
    if function_calls and len(function_calls) > 0:
        func_res = []
        for fc in function_calls:
            print(f"calling function: {fc.name}, {fc.args}")
            func_args = fc.args if fc.args else {}
            content = call_function(fc, verbose=is_verbose, **func_args)
            if not content.parts:
                raise Exception(f"Error: content doesn't contain parts")
            if not content.parts[0].function_response:
                raise Exception(f"Error: malform function response")

            func_res.append(content.parts[0].function_response)
            if is_verbose:
                print(f"-> {content.parts[0].function_response.response}")


def test():
    args = sys.argv[1:]
    print(args)


if __name__ == "__main__":
    main()
