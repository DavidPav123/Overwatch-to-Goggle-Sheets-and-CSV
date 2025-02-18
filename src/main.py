from time import sleep
from google_sheets_push import update_sheet
from os.path import exists, expanduser
from json_functions import get_spreadsheet_id, get_spreadsheet_pages
from get_latest_workshop_file import get_latest_file, get_windows_version
from csv_functions import (
    read_csv_file,
    export_to_csv,
    check_file_change,
    file_len,
)

# List of pages for google sheets to write to
pages_to_update: list[str] = [
    "Placeholder1",
    "Placeholder2",
]
# Variable for switching pages when new file is detected
current_page: int = 0
# Range to update in sheets
range_name: str = f"{pages_to_update[current_page]}!A1:Z26"
# Name of the current map
current_map: str = ""


def update_page(page_list: list[str], current_page: int) -> str:
    """
    Generates a string reference for a specific range in a spreadsheet page.

    The function uses the provided page list and the current page index to determine
    the name of the page. It then generates a string reference to a specific range (A1:Z26)
    in that page.

    Args:
        page_list (list): A list of page names.
        current_page (int): The index of the current page in the page_list.

    Returns:
        str: A string reference to the range A1:Z26 in the specified page.
    """
    return f"{page_list[current_page]}!A1:Z26"


if __name__ == "__main__":
    credentials_exist = exists("credentials.json")
    spreadsheet_id = get_spreadsheet_id("config.json")
    spreadsheet_pages_exists = False
    windows_version = get_windows_version()

    if windows_version == 10:
        workshop_file_path = f"{expanduser('~/Documents')}/Overwatch/Workshop/*"
    else:
        workshop_file_path = (
            f"{expanduser('~/')}/OneDrive/Documents/Overwatch/Workshop/*"
        )

    if credentials_exist:
        if spreadsheet_id:
            print(f"Spreadsheet ID found: {spreadsheet_id}")
            try:
                pages_to_update_temp = get_spreadsheet_pages("config.json")
                if pages_to_update_temp == [] or pages_to_update_temp == None:
                    print("No spreadsheet pages found!")
                else:
                    print(
                        f"Uploading to spreadsheet pages: {pages_to_update_temp}"
                    )
                    pages_to_update.extend(pages_to_update_temp)
                    spreadsheet_pages_exists = True
            except:
                print("No spreadsheet pages found!")
        else:
            print("No spreadsheet ID found!")

    else:
        print("No credentials.json found!")

    if credentials_exist and spreadsheet_pages_exists and spreadsheet_id:
        upload = True
    else:
        upload = False
        print("Not uploading to Google Sheets!")

    file = get_latest_file(workshop_file_path)
    current_map_temp = check_file_change(file)

    while True:
        current_map_temp = check_file_change(file)

        if current_map != current_map_temp:
            current_map = current_map_temp
            current_page += 1
            if upload == True:
                try:
                    range_name = update_page(pages_to_update, current_page)
                except IndexError:
                    print("No more pages to export to!")
                    break

        if 12 <= file_len(file) and current_page != 1:
            stats = read_csv_file(file)

            try:
                export_to_csv(stats, f"game{current_page - 1}.csv")
            except IOError:
                print("CSV file is open, couldn't write!")
            if upload == True and spreadsheet_id:
                stuff_to_upload: list[list[str]] = []
                stuff_to_upload.append(stats.columns.to_list())
                stuff_to_upload.extend(stats.to_numpy().tolist())  # type: ignore
                update_sheet(stuff_to_upload, range_name, spreadsheet_id)
            print("Match Data Exported")

        else:
            print("Waiting for data")

        new_file: str = get_latest_file(workshop_file_path)

        if file != new_file:
            file = new_file

        sleep(2)
