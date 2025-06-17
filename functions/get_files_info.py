import os

def get_file_size(directory, file):
        # Get file size
        try:
            file_size = os.path.getsize(os.path.join(directory, file))
        except OSError as e:
            return f"Error: {e}"
        return file_size

def files_info_string(target_directory):
        # Check if the directory input is indeed a directory or not
        if os.path.isdir(target_directory) == False:
            return f'Error: "{target_directory}" is not a directory'
        
        # Return file/subdirectory info for all files/subdirectories contained in the directory input
        contents_list = []
        try:
            directory_contents = os.listdir(target_directory)
        except OSError as e:
            return f"Error: {e}"

        for content in directory_contents:
            size_result = get_file_size(target_directory, content)
            if isinstance(size_result, str) and size_result.startswith("Error:"):
                size_display = size_result  # Don't add "bytes" to error messages
            else:
                size_display = f"{size_result} bytes"

            contents_list.append(f"- {content}: file_size={size_display} bytes, is_dir={os.path.isdir(os.path.join(target_directory, content))}")
        return "\n".join(contents_list)

def get_files_info(working_directory, directory=None):
    # absolute_path = None # Is it neccessary to declare the absolute_path variable now?
    # If directory == None, continue with working directory
    if directory == None:
        target_directory = os.path.abspath(working_directory)
        return files_info_string(target_directory)
    else:
        target_directory = os.path.abspath(directory)
        # Check if the directory input is in the working directory
        if target_directory.startswith(os.path.abspath(working_directory)):
            return files_info_string(target_directory)
        # Return error string if directory input not in working directory
        else:
            return f'Error: Cannot list "{directory}" as it is outside the permitted working directory'
    
        


    # Format for file info to be returned
    # - README.md: file_size=1032 bytes, is_dir=False
    # - src: file_size=128 bytes, is_dir=True
    # - package.json: file_size=1234 bytes, is_dir=False
