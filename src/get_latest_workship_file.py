from sys import getwindowsversion
from glob import glob
from os.path import getctime
from typing import Literal


def get_latest_file(file_path: str) -> str:
    """
    Retrieves the path of the latest file in the specified directory based on its creation time.

    Args:
        file_path (str): The path (with potential wildcards) indicating where to search for files.

    Returns:
        str: The path to the latest file in the specified directory.
    """
    list_of_files = glob(file_path)
    latest_file: str = max(list_of_files, key=getctime)
    return latest_file


def get_windows_version() -> Literal[10, 11]:
    """
    Determines the major version of the current Windows OS.

    Based on the build number, this function identifies whether the Windows version is 10 or 11.

    Returns:
        Literal[10, 11]: Returns 10 if the Windows build number is less than or equal to 22000.
                         Returns 11 otherwise.
    """
    win_version = getwindowsversion().build

    if win_version <= 22000:
        return 10
    else:
        return 11


if __name__ == "__main__":
    import os
    import unittest

    dir_path = os.path.dirname(os.path.realpath(__file__))
    temp_txt_path = os.path.join(dir_path, "test_files/test.txt")
    dir_path = os.path.join(dir_path, "test_files/*")

    class TestStringMethods(unittest.TestCase):
        def test_windows_version(self):
            self.assertEqual(get_windows_version(), 11)

        def test_get_latest_file(self):
            with open(temp_txt_path, "w") as file:
                file.write("Hello, World!")
            print(get_latest_file(dir_path))
            self.assertEqual(
                get_latest_file(dir_path),
                r"F:\programming\OW-to-gs-CSV\src\test_files\test.txt",
            )
            os.remove(temp_txt_path)

    unittest.main()
