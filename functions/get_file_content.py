import os

def file_contents(directory, file_path):
    # Maxixum characters to be returned from file
    MAX_CHARS = 10000
    # Return contents of target file as a string
    try:
        with open(os.path.join(directory, file_path), "r") as f:
            file_content_string = f.read(MAX_CHARS) + f'[...File "{file_path}" truncated at 10000 characters]'
    except OSError as e:
         return f"Error: {e}"
    return file_content_string
     

def get_file_content(working_directory, file_path):
    # If file == None return an error
    if file_path == None:
        return f"Error: No file selected"
    else:
        target_file_path = os.path.abspath(file_path)
        # Check if the target file is in working directory
        if target_file_path.startswith(os.path.abspath(working_directory)):
            return file_contents(target_file_path)
        # Return error string if target file not in working directory
        else:
            f'Error: Cannot read "{file_path}" as it is outside the permitted working directory'