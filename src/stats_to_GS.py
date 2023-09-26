from glob import glob
from os.path import getctime, expanduser
from csv import reader
from time import sleep
from csv import writer
from google_sheets_push import update_sheet
from json import load
from sys import getwindowsversion

# List of pages for google sheets to write toP
pages_to_update: list = ["Placeholder1","Placeholder2"]
# Variable for switching pages when new file is detected
current_page: int = 0
# Range to update in sheets change infor after
range_name: str = f"{pages_to_update[current_page]}!A1:Z26"
# Name of the current map
cur_map: str = ""

def get_spreadsheet_pages():
    with open("config.json", 'r') as file:
        data = load(file)
        return data.get("Spreadsheet Pages", None)


def get_latest_file() -> str:
    win_version = getwindowsversion().build
    list_of_files = []

    if win_version <= 22000:
        list_of_files = glob(f"{expanduser('~/Documents')}/Overwatch/Workshop/*")
    else:
        list_of_files = glob(f"{expanduser('~/')}/OneDrive/Documents/Overwatch/Workshop/*")

    latest_file: str = max(list_of_files, key=getctime)
    return latest_file


def read_csv_file(file_to_read: str) -> list:
    row_data: list[list] = []
    t1: list = []
    t2: list = []
    file_length: int = file_len(file_to_read)

    with open(file_to_read) as csv_file:
        csv_reader = reader(csv_file, delimiter=",")
        for numbers in range(file_length - 9, file_length + 1):
            for rows in csv_reader:
                if csv_reader.line_num == numbers:
                    rows.pop(0)
                    if rows[1] == "LÃºcio":
                        rows[1] = "Lucio"
                    elif rows[1] == "TorbjÃ¶rn":
                        rows[1] = "Torbjorn"
                    if rows[len(rows) - 1] == "Team 1":
                        t1.insert(0, rows)
                    else:
                        t2.append(rows)
                    break

    row_data.insert(
        0,
        [
            "Player Name",
            "Hero Name",
            "Damage Dealt",
            "Barrier Damage",
            "Damage Blocked",
            "Damage Taken",
            "Deaths",
            "Elims",
            "Final Blows",
            "Env Deaths",
            "Env Kills",
            "Healing",
            "Obj Kills",
            "solo kills",
            "Ults Earned",
            "Ults Used",
            "Healing Recived",
            "Team",
        ],
    )
    for t1_rows in t1:
        row_data.append(t1_rows)
    for t2_rows in t2:
        row_data.append(t2_rows)
    return row_data


def check_file_change(file_to_read: str) -> list[str]:
    with open(file_to_read) as csv_file:
        csv_reader = reader(csv_file, delimiter=",")
        header: list[str] = next(csv_reader)
        return header


def file_len(file_to_read: str) -> int:
    with open(file_to_read) as fp:
        lines: int = len(fp.readlines())
        return lines


def update_page(page_list: list, current_page: int) -> str:
    return f"{page_list[current_page]}!A1:Z26"

def export_to_csv(rows,file_name):
    with open(f'CSVs/{file_name}', 'w') as f:
        write = writer(f, delimiter=',', lineterminator="\n")
        write.writerows(rows)

if __name__ == "__main__":
    pages_to_update.extend(get_spreadsheet_pages())
    file: str = get_latest_file()
    cur_map_temp: list[str] = check_file_change(file)

    while True:
        cur_map_temp: list[str] = check_file_change(file)

        if cur_map != cur_map_temp :
            cur_map = cur_map_temp
            current_page += 1
            range_name = update_page(pages_to_update, current_page)

        if 12 <= file_len(file) and current_page!=1:
            stats = read_csv_file(file)
            export_to_csv(stats, f"{current_page -1}.csv")
            update_sheet(stats, range_name)
            print("Match Data Exported")

        else:
            print("Waiting for data")

        new_file: str = get_latest_file()

        if file != new_file:
            file = new_file

        sleep(2)
