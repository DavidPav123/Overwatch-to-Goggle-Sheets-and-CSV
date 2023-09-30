from time import sleep
from src.google_sheets_push import update_sheet
from os.path import exists, expanduser
from src.json_functions import get_spreadsheet_id, get_spreadsheet_pages
from src.get_latest_workship_file import get_latest_file, get_windows_version
from src.csv_functions import read_csv_file, export_to_csv, check_file_change, file_len

# List of pages for google sheets to write toP
pages_to_update: list = ["Placeholder1", "Placeholder2"]
# Variable for switching pages when new file is detected
current_page: int = 0
# Range to update in sheets change infor after
range_name: str = f"{pages_to_update[current_page]}!A1:Z26"
# Name of the current map
cur_map: str = ""


def update_page(page_list: list, current_page: int) -> str:
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
    spreadsheet_id_exists = False
    spreadsheet_pages_exists = False
    windows_version = get_windows_version()

    if windows_version == 10:
        workshop_file_path = f"{expanduser('~/Documents')}/Overwatch/Workshop/*"
    else:
        workshop_file_path = (
            f"{expanduser('~/')}/OneDrive/Documents/Overwatch/Workshop/*"
        )

    if credentials_exist:
        try:
            spreadsheet_id = get_spreadsheet_id("config.json")
            if spreadsheet_id == "" or spreadsheet_id == None:
                print("No spreadsheet ID found!")
            else:
                print(f"Uploading to spreadsheet ID: {spreadsheet_id}")
                spreadsheet_id_exists = True

        except:
            print("No spreadsheet ID found!")
        if spreadsheet_id_exists:
            try:
                pages_to_update_temp = get_spreadsheet_pages("config.json")
                if pages_to_update_temp == [] or pages_to_update_temp == None:
                    print("No spreadsheet pages found!")
                else:
                    print(f"Uploading to spreadsheet pages: {pages_to_update_temp}")
                    pages_to_update.extend(pages_to_update_temp)
                    spreadsheet_pages_exists = True
            except:
                print("No spreadsheet pages found!")
    else:
        print("No credentials.json found!")

    if credentials_exist and spreadsheet_id_exists and spreadsheet_pages_exists:
        upload = True
    else:
        upload = False
        print("Not uploading to Google Sheets!")

    file = get_latest_file(workshop_file_path)
    cur_map_temp = check_file_change(file)

    while True:
        cur_map_temp = check_file_change(file)

        if cur_map != cur_map_temp:
            cur_map = cur_map_temp
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
                export_to_csv(stats, f"game{current_page -1}.csv")
            except IOError:
                print("CSV file is open, couldn't write!")
            if upload == True:
                stuff_to_upload = []
                stuff_to_upload.append(stats.columns.to_list())
                stuff_to_upload.extend(stats.values.tolist())
                update_sheet(stuff_to_upload, range_name)
            print("Match Data Exported")

        else:
            print("Waiting for data")

        new_file: str = get_latest_file(workshop_file_path)

        if file != new_file:
            file = new_file

        sleep(2)
