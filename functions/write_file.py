import os



def write_file(working_directory, file_path, content):
    target_file_path = os.path.abspath(os.path.join(working_directory,file_path))

# Check if the target file is in working directory
    if target_file_path.startswith(os.path.abspath(working_directory)):
        # Check if file_path exists
        if os.path.exists(target_file_path):
            # Overwrite contents of file
            try:
                with open(target_file_path, "w") as f:
                    f.write(content)
                    return f'Successfully wrote to "{file_path}" ({len(content)} characters written)'
            except OSError as e:
                return f'Error: {e}'

        else:
            # Create file path
            try:
                os.makedirs(os.path.dirname(target_file_path), exist_ok=True)
            except OSError as e:
                return f'Error: {e}'
            
            # Write contents to newly created file
            try:
                with open(target_file_path, "w") as f:
                    f.write(content)
                    return f'Successfully wrote to "{file_path}" ({len(content)} characters written)'
            except OSError as e:
                return f'Error: {e}'

    # Return error string if target file not in working directory
    else:
        return f'Error: Cannot write to "{file_path}" as it is outside the permitted working directory'