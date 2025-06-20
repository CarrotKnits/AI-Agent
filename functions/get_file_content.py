import os

def get_file_content(working_directory, file_path):
    target_file_path = os.path.abspath(os.path.join(working_directory,file_path))

    # Check if the target file is in working directory
    if target_file_path.startswith(os.path.abspath(working_directory)):
        # Check if file is really a file or not
        if os.path.isfile(target_file_path) == False:
            return f'Error: File not found or is not a regular file: "{file_path}"'
    
        # Maxixum characters to be returned from file
        MAX_CHARS = 10000
    
        # Return contents of target file as a string
        try:
            with open(target_file_path, "r") as f:
                file_content_string = f.read()
                # Trencate file to 10000 chars if count is > 10000
                if len(file_content_string) > 10000:
                    file_content_string = file_content_string[:MAX_CHARS] + f'[...File "{file_path}" truncated at 10000 characters]'
        except OSError as e:
            return f"Error: {e}"
        return file_content_string
    # Return error string if target file not in working directory
    else:
       return f'Error: Cannot read "{file_path}" as it is outside the permitted working directory'
