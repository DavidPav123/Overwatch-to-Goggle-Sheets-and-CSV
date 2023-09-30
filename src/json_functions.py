from json import load
from typing import Optional, List


def get_spreadsheet_id(file_name: str) -> Optional[str]:
    """
    Extracts the Spreadsheet ID from a given file.

    This function reads the provided file, expecting it to be in a specific
    format (e.g., JSON) and retrieves the value associated with the key "Spreadsheet ID".

    Args:
        file_name (str): The path to the file containing the spreadsheet details.

    Returns:
        Optional[str]: The Spreadsheet ID if found; otherwise, returns None.
    """
    with open(file_name, "r") as file:
        data = load(file)
        return data.get("Spreadsheet ID", None)


def get_spreadsheet_pages(file_name: str) -> Optional[List[str]]:
    """
    Extracts the list of Spreadsheet Pages from a given file.

    This function reads the provided file, expecting it to be in a specific
    format (e.g., JSON) and retrieves the value associated with the key "Spreadsheet Pages".

    Args:
        file_name (str): The path to the file containing the spreadsheet details.

    Returns:
        Optional[List[str]]: A list of Spreadsheet Pages if found; otherwise, returns None.
    """
    with open(file_name, "r") as file:
        data = load(file)
        return data.get("Spreadsheet Pages", None)


if __name__ == "__main__":
    import os
    import unittest

    dir_path = os.path.dirname(os.path.realpath(__file__))
    config_path = os.path.join(dir_path, "test_files/config.json")

    class TestStringMethods(unittest.TestCase):
        def test_get_spreadsheet_pages(self):
            self.assertEqual(
                get_spreadsheet_pages(config_path),
                ["Sheet1", "Sheet2", "Sheet3", "Sheet4", "Sheet5"],
            )

        def test_get_spreadsheet_id(self):
            self.assertEqual(
                get_spreadsheet_id(config_path),
                "1_s8kTUCKG7wWY43Fa24knmBPAW-iV0uoNBLLUXUxLA0",
            )

    unittest.main()
