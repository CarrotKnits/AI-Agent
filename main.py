import os
import sys
from dotenv import load_dotenv
from google import genai
from google.genai import types


load_dotenv()
api_key = os.environ.get("GEMINI_API_KEY")
client = genai.Client(api_key=api_key)


# Print error in case of no prompt provided
if len(sys.argv) < 2: 
    print('ERROR: Must provide prompt. (e.g. "insert prompt in quotes")')
    sys.exit(1)

system_prompt = """
You are a helpful AI coding agent.

When a user asks a question or makes a request, make a function call plan. You can perform the following operations:

- List files and directories
- Read file contents
- Execute Python files with optional arguments
- Write or overwrite files

All paths you provide should be relative to the working directory. You do not need to specify the working directory in your function calls as it is automatically injected for security reasons.
"""

schema_get_files_info = types.FunctionDeclaration(
    name="get_files_info",
    description="Lists files in the specified directory along with their sizes, constrained to the working directory.",
    parameters=types.Schema(
        type=types.Type.OBJECT,
        properties={
            "directory": types.Schema(
                type=types.Type.STRING,
                description="The directory to list files from, relative to the working directory. If not provided, lists files in the working directory itself.",
            ),
        },
    ),
)

schema_get_file_content = types.FunctionDeclaration(
    name="get_file_content",
    description="Gets the contents of a file in the specified directory and returns upto the first 10000 characters of the file's contents.",
    parameters=types.Schema(
        type=types.Type.OBJECT,
        properties={
            "file_path": types.Schema(
                type=types.Type.STRING,
                description="The file path to get and return the file content from. If not provided, will return an error.",
            ),
        },
    ),
)

schema_write_file = types.FunctionDeclaration(
    name="write_file",
    description="Overwites a specified file with provided content, relative to the working directory.",
    parameters=types.Schema(
        type=types.Type.OBJECT,
        properties={
            "file_path": types.Schema(
                type=types.Type.STRING,
                description="The file path to the specified file to be overwritten, relative to the working directory. If the file doesn't exist, fill create the file and the missing directories provided.",
            ),
            "content": types.Schema(
                type=types.Type.STRING,
                description="The content to be used to overwrite the specified file."
            ),
        },
    ),
)

schema_run_python_file = types.FunctionDeclaration(
    name="run_python_file",
    description="Runs/executes a specified python file relative to the working directory.",
    parameters=types.Schema(
        type=types.Type.OBJECT,
        properties={
            "file_path": types.Schema(
                type=types.Type.STRING,
                description="The file path for the specified python file to be ran/executed.",
            ),
        },
    ),
)

available_functions = types.Tool(
    function_declarations=[
        schema_get_files_info,
        schema_write_file,
        schema_get_file_content,
        schema_run_python_file
    ]
)



# Commandline arguments
user_prompt = sys.argv[1]

# Storage of all messages in chatbot conversation
messages = [
    types.Content(role="user", parts=[types.Part(text=user_prompt)]),
]

# Variable of prompt response
response = client.models.generate_content(
    model="gemini-2.0-flash-001",
    contents=messages,
    config=types.GenerateContentConfig(
        tools=[available_functions], system_instruction=system_prompt
    )
)

if response.function_calls:
    for function_call in response.function_calls:
        print(f"Calling function: {function_call.name}({function_call.args})")
else:
    # Print response to prompt
    print(response.text)

# If --verbose flag is added
if "--verbose" in sys.argv[2:]:
    print(f"User prompt: {user_prompt}")
    print(f"Prompt tokens: {response.usage_metadata.prompt_token_count}\nResponse tokens: {response.usage_metadata.candidates_token_count}")

