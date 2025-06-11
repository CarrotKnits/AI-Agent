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

# Commandline arguments
user_prompt = sys.argv[1]

# Storage of all messages in chatbot conversation
messages = [
    types.Content(role="user", parts=[types.Part(text=user_prompt)]),
]

# Variable of prompt response
response = client.models.generate_content(model="gemini-2.0-flash-001", contents=messages)

# Print response to prompt
print(response.text)

# If --verbose flag is added
if "--verbose" in sys.argv[2:]:
    print(f"User prompt: {user_prompt}")
    print(f"Prompt tokens: {response.usage_metadata.prompt_token_count}\nResponse tokens: {response.usage_metadata.candidates_token_count}")

