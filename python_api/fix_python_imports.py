import os
import sys
from pathlib import Path


def get_current_folder():
    return Path(os.path.dirname(os.path.realpath(__file__)))


def get_parent_folder():
    return Path(os.path.dirname(os.path.realpath(__file__))).parent


def fix_path_import():
    current_folder = get_current_folder()
    parent_folder = get_parent_folder()
    sys.path.append(str(current_folder))
    sys.path.append(str(parent_folder))


fix_path_import()


def __main():
    current_folder = get_current_folder()
    print(current_folder)
    return


if __name__ == '__main__':
    __main()
