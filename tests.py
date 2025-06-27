from functions.get_files_info import *

if __name__ == "__main__":
    print(get_files_info("calculator", "."))
    print(get_files_info("calculator", "pkg"))
    print(get_files_info("calculator", "/bin")) # this should return an error
    print(get_files_info("calculator", "../")) # this should return an error
    