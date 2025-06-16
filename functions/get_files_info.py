import os

def get_files_info(working_directory, directory=None):    
    # Get absolute path for the directory input or, if no directory input, get absolute path for the working directory
    if directory == None:
        absolute_path = os.path.abspath(working_directory)
    else:
        absolute_path = os.path.abspath(directory)
    
    # Check if the directory input is in the working directory
    if absolute_path.startswith(os.path.abspath(working_directory)):
        # Check if the directory input is indeed a directory or not
        if os.path.isdir(directory) == False:
            return f'Error: "{directory}" is not a directory'
        # Return file/subdirectory info for all files/subdirectories contained in the directory input
        contents_list = []
        directory_contents = os.listdir(directory)
        for content in directory_contents:
            contents_list.append(f"- {content}: file_size={os.path.getsize(os.path.join(absolute_path, content))}, is_dir={os.path.isdir(os.path.join(absolute_path, content))}")
        return "\n".join(contents_list)
    # Return error string if directory input not in working directory
    else:
        return f'Error: Cannot list "{directory}" as it is outside the permitted working directory'
    
        


    # Format for file info to be returned
    # - README.md: file_size=1032 bytes, is_dir=False
    # - src: file_size=128 bytes, is_dir=True
    # - package.json: file_size=1234 bytes, is_dir=False
