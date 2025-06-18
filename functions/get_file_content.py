import os

def cat_file_content(target_file_path):
    pass

def get_file_content(working_directory, file_path):
        target_file_path = os.path.abspath(file_path)
        # Check if the target file is in the working directory
        if target_file_path.startswith(os.path.abspath(working_directory)):
            return cat_file_content(target_file_path)
        # Return error string if target file not in working directory
        else:
            f'Error: Cannot read "{file_path}" as it is outside the permitted working directory'