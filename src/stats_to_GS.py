from glob import glob
from os.path import getctime, expanduser
from time import sleep
from google_sheets_push import update_sheet
from json import load
from sys import getwindowsversion
from os.path import exists
import pandas as pd

# List of pages for google sheets to write toP
pages_to_update: list = ["Placeholder1","Placeholder2"]
# Variable for switching pages when new file is detected
current_page: int = 0
# Range to update in sheets change infor after
range_name: str = f"{pages_to_update[current_page]}!A1:Z26"
# Name of the current map
cur_map: str = ""

    
def get_spreadsheet_id():
    with open("config.json", 'r') as file:
        data = load(file)
        return data.get("Spreadsheet ID", None)

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

def read_csv_file(file_to_read: str) -> pd.DataFrame:
    row_data: list[list] = []
    t1: list = []
    t2: list = []

    column_names = [
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
            "Team",]

    df = pd.read_csv(file_to_read, skiprows=range(1, file_len(file_to_read) - 9), header=0, names=column_names, encoding="utf-8")

    df['Hero Name'] = df['Hero Name'].replace({"LÃºcio": "Lucio", "TorbjÃ¶rn": "Torbjorn"})
    df = df.sort_values(by='Team', ascending=False)
    return df

def check_file_change(file_to_read: str) -> list[str]:
    fp = pd.read_csv(file_to_read, nrows=0, encoding="utf-8")
    return fp.columns.to_list()[0]

def file_len(file_to_read: str) -> int:
    fp = pd.read_csv(file_to_read, encoding="utf-8")
    return fp.shape[0]

def update_page(page_list: list, current_page: int) -> str:
    return f"{page_list[current_page]}!A1:Z26"

def export_to_csv(df: pd.DataFrame, file_name: str):
    df.to_csv(f'CSVs/{file_name}', index=False)

if __name__ == "__main__":
    credentials_exist = exists("credentials.json")
    spreadsheet_id_exists = False
    spreadsheet_pages_exists = False

    if credentials_exist:
        try:
            spreadsheet_id = get_spreadsheet_id()
            if spreadsheet_id == "" or spreadsheet_id == None:
                print("No spreadsheet ID found!")
            else:
                print(f"Uploading to spreadsheet ID: {spreadsheet_id}")
                spreadsheet_id_exists = True

        except:
            print("No spreadsheet ID found!")
        if spreadsheet_id_exists:
            try:
                pages_to_update_temp = get_spreadsheet_pages()
                if pages_to_update_temp ==  [] or pages_to_update_temp == None:
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

    file: str = get_latest_file()
    cur_map_temp: list[str] = check_file_change(file)

    while True:
        cur_map_temp: list[str] = check_file_change(file)

        if cur_map != cur_map_temp :
            cur_map = cur_map_temp
            current_page += 1
            if upload == True:
                range_name = update_page(pages_to_update, current_page)

        if 12 <= file_len(file) and current_page!=1:
            stats = read_csv_file(file)
            #print([stats.columns].extend(stats.values.tolist()))
            
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

        new_file: str = get_latest_file()

        if file != new_file:
            file = new_file

        sleep(2)
