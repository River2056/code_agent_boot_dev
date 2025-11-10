import os
import sys

from dotenv import load_dotenv
from google import genai
from google.genai import types


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

    messages = [types.Content(role="user", parts=[types.Part(text=user_prompt)])]

    client = genai.Client(api_key=api_key)
    res = client.models.generate_content(
        model="gemini-2.0-flash-001",
        contents=messages,
    )

    token_count = res.usage_metadata.prompt_token_count if res.usage_metadata else 0
    response_tokens = res.usage_metadata.total_token_count if res.usage_metadata else 0
    response = res.text or ""

    if is_verbose:
        print(f"Prompt tokens: {token_count}")
        print(f"Response tokens: {response_tokens}")
    print(f"Response: {response}")


def test():
    args = sys.argv[1:]
    print(args)


if __name__ == "__main__":
    main()
