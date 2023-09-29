from sys import getwindowsversion
from glob import glob
from os.path import getctime, expanduser

def get_latest_file() -> str:
    win_version = getwindowsversion().build
    list_of_files = []

    if win_version <= 22000:
        list_of_files = glob(f"{expanduser('~/Documents')}/Overwatch/Workshop/*")
    else:
        list_of_files = glob(f"{expanduser('~/')}/OneDrive/Documents/Overwatch/Workshop/*")

    latest_file: str = max(list_of_files, key=getctime)
    return latest_file