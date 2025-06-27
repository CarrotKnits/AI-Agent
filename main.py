import os
import sys
from dotenv import load_dotenv
from google import genai
from google.genai import types
from functions.get_file_content import *
from functions.get_files_info import *
from functions.write_file import *
from functions.run_python import *

load_dotenv()
api_key = os.environ.get("GEMINI_API_KEY")
client = genai.Client(api_key=api_key)

def function_call_tree(function_call_part):
    if function_call_tree == "get_files_info":
        get_files_info()
    elif function_call_part == "get_file_content":
        get_file_content()
    elif function_call_part == "write_file":
        write_file()
    elif function_call_part == "run_python_file":
        run_python_file()


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
# If need to change working directory change it here
working_directory = {"working_directory": "./calculator"}

def function_call_branches(function_call_part):
            if function_call_part.name == "get_files_info":
                args_with_working_dir = {**function_call_part.args, **working_directory}
                function_result = get_files_info(**args_with_working_dir)
                return types.Content(
                    role="tool",
                    parts=[
                        types.Part.from_function_response(
                            name="get_files_info",
                            response={"result": function_result},
                        )
                    ],
                )
            elif function_call_part.name == "get_file_content":
                args_with_working_dir = {**function_call_part.args, **working_directory}
                function_result = get_file_content(**args_with_working_dir)
                return types.Content(
                    role="tool",
                    parts=[
                        types.Part.from_function_response(
                            name="get_file_content",
                            response={"result": function_result},
                        )
                    ],
                )
            elif function_call_part.name == "write_file":
                args_with_working_dir = {**function_call_part.args, **working_directory}
                function_result = write_file(**args_with_working_dir)
                return types.Content(
                    role="tool",
                    parts=[
                        types.Part.from_function_response(
                            name="write_file",
                            response={"result": function_result},
                        )
                    ],
                )
            elif function_call_part.name == "run_python_file":
                args_with_working_dir = {**function_call_part.args, **working_directory}
                function_result = run_python_file(**args_with_working_dir)
                return types.Content(
                    role="tool",
                    parts=[
                        types.Part.from_function_response(
                            name="run_python_file",
                            response={"result": function_result},
                        )
                    ],
                )
            else:
                return types.Content(
                    role="tool",
                    parts=[
                        types.Part.from_function_response(
                            name=function_call_part.name,
                            response={"error": f"Unknown function: {function_call_part.name}"},
                        )
                    ],
                )


# Will have the AI agengt actually call a function from the available functions implemented in 'available_functionts'
def call_function(function_call_part, verbose=False):
    if verbose == True:
        print(f"Calling function: {function_call_part.name}({function_call_part.args})")
        return function_call_branches(function_call_part)
    else:
        print(f" - Calling function: {function_call_part.name}")
        return function_call_branches(function_call_part)


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


# Main program starts here
if response.function_calls:
    for function_call in response.function_calls:
        call_function(function_call, sys.argv[2])
else:
    # Print response to prompt
    print(response.text)

# If --verbose flag is added
if "--verbose" in sys.argv[2:]:
    print(f"User prompt: {user_prompt}")
    print(f"Prompt tokens: {response.usage_metadata.prompt_token_count}\nResponse tokens: {response.usage_metadata.candidates_token_count}")

