import os
import subprocess

def run_python_file(working_directory, file_path):
    target_file_path = os.path.abspath(os.path.join(working_directory,file_path))

    # Check if the target file is in working directory
    if target_file_path.startswith(os.path.abspath(working_directory)):
        # Check if file_path exists
        if os.path.exists(target_file_path):
            # Check if the file is a '.py' file
            if target_file_path.endswith(".py"):
                try:
                    # Execute python file
                    result = subprocess.run(["python3", file_path], cwd=os.path.abspath(working_directory), text=True, capture_output=True, timeout=30)
                except OSError as e:
                    return f"Error: executing Python file: {e}"
                
                try:
                    # Check if process exits with a non-zero code
                    if result.returncode != 0:
                        output = f'STDOUT:{result.stdout}\nSTDERR:{result.stderr}\nProcess exited with code {result.returncode}'
                    elif result.returncode == 0:
                        output = f'STDOUT:{result.stdout}\nSTDERR:{result.stderr}'
                    else:
                        return "No output produced."
                except OSError as e:
                    return f"Error: executing Python file: {e}"
                return output
            
            else:
                f'Error: "{file_path}" is not a Python file.'

        else:
            f'Error: File "{file_path}" not found.'

    else:
        return f'Error: Cannot execute "{file_path}" as it is outside the permitted working directory'