import os
from typing import Any
import unittest
from json_functions import get_spreadsheet_id, get_spreadsheet_pages
from get_latest_workshop_file import get_latest_file, get_windows_version
from csv_functions import read_csv_file, export_to_csv, check_file_change, file_len
from pandas import DataFrame

if __name__ == "__main__":
    dir_path = os.path.dirname(os.path.realpath(__file__))
    config_path = os.path.join(dir_path, "test_files/config.json")
    temp_txt_path = os.path.join(dir_path, "test_files/test.txt")
    directory_test_path = os.path.join(dir_path, "test_files/*")
    csv_path = os.path.join(dir_path, "test_files/test.csv")
    log_path = os.path.join(dir_path, "test_files/test_log.txt")
    temp_csv_path = os.path.join(dir_path, "test_files/temp_test.csv")
    test_frame: dict[str,dict[str, Any]] = {
        "Player Name": {"[00:01:10] 70.10": "Ana"},
        "Hero Name": {"[00:01:10] 70.10": "Ana"},
        "Damage Dealt": {"[00:01:10] 70.10": 0},
        "Barrier Damage": {"[00:01:10] 70.10": 0},
        "Damage Blocked": {"[00:01:10] 70.10": 0},
        "Damage Taken": {"[00:01:10] 70.10": 0},
        "Deaths": {"[00:01:10] 70.10": 0},
        "Elims": {"[00:01:10] 70.10": 0},
        "Final Blows": {"[00:01:10] 70.10": 0},
        "Env Deaths": {"[00:01:10] 70.10": 0},
        "Env Kills": {"[00:01:10] 70.10": 0},
        "Healing": {"[00:01:10] 70.10": 0},
        "Obj Kills": {"[00:01:10] 70.10": 0},
        "solo kills": {"[00:01:10] 70.10": 0},
        "Ults Earned": {"[00:01:10] 70.10": 0},
        "Ults Used": {"[00:01:10] 70.10": 0},
        "Healing Recived": {"[00:01:10] 70.10": 0},
        "Team": {"[00:01:10] 70.10": "Team 2"},
    }

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

        def test_windows_version(self):
            self.assertEqual(get_windows_version(), 11)

        def test_get_latest_file(self):
            with open(temp_txt_path, "w") as file:
                file.write("Hello, World!")
            print(get_latest_file(directory_test_path))
            self.assertEqual(
                get_latest_file(directory_test_path),
                r"F:\programming\OW-to-gs-CSV\src\test_files\test.txt",
            )
            os.remove(temp_txt_path)

        def test_file_len(self):
            self.assertEqual(file_len(csv_path), 5)

        def test_read_csv_file(self):
            self.assertEqual(read_csv_file(log_path).to_dict(), test_frame)

        def test_check_file_change(self):
            self.assertEqual(
                check_file_change(log_path), "[00:00:00] Antarctic Peninsula"
            )

        def test_export_to_csv(self):
            export_to_csv(DataFrame(test_frame), temp_csv_path)
            self.assertEqual(os.path.exists(temp_csv_path), True)
            os.remove(temp_csv_path)

    unittest.main()
