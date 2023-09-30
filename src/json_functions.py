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
