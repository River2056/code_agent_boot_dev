from google.genai import types

from functions.get_files_info import get_files_info
from functions.get_file_content import get_file_content
from functions.write_file import write_file
from functions.run_python_file import run_python_file


def call_function(
    function_call_part: types.FunctionCall, verbose=False, **kwargs
) -> types.Content:
    if verbose:
        print(f"Calling function: {function_call_part.name}({function_call_part.args})")
    else:
        print(f" - Calling function: {function_call_part.name}")

    func_name = function_call_part.name if function_call_part.name else ""
    available_functions = {
        "get_files_info": get_files_info,
        "get_file_content": get_file_content,
        "write_file": write_file,
        "run_python_file": run_python_file,
    }
    func_to_call = available_functions.get(func_name)
    print(f"name: {func_name}, func: {func_to_call}")

    if not func_to_call:
        return generate_content(func_name, "", True)

    result = func_to_call(working_directory="./calculator", **kwargs)
    return generate_content(func_name, result)


def generate_content(func_name: str, func_result: str, is_error=False):
    ret_obj = {}
    if is_error:
        ret_obj = {"error": f"Unknown function: {func_name}"}
    else:
        ret_obj = {"result": func_result}

    return types.Content(
        role="tool",
        parts=[types.Part.from_function_response(name=func_name, response=ret_obj)],
    )
