from functions.run_python import run_python_file

if __name__ == "__main__":
    print(run_python_file("calculator", "main.py"))
    print(run_python_file("calculator", "tests.py"))
    print(run_python_file("calculator", "../main.py")) # this should return an error
    print(run_python_file("calculator", "nonexistent.py")) # this should return an error
    