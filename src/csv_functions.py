import pandas as pd

def read_csv_file(file_to_read: str) -> pd.DataFrame:
    row_data= []
    t1 = []
    t2 = []

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

def export_to_csv(df: pd.DataFrame, file_name: str):
    df.to_csv(f'CSVs/{file_name}', index=False)

def check_file_change(file_to_read: str) -> str:
    fp = pd.read_csv(file_to_read, nrows=0, encoding="utf-8")
    return fp.columns.to_list()[0]

def file_len(file_to_read: str) -> int:
    fp = pd.read_csv(file_to_read, encoding="utf-8")
    return fp.shape[0]

if __name__ == "__main__":
    import os
    import unittest

    dir_path = os.path.dirname(os.path.realpath(__file__))
    csv_path = os.path.join(dir_path, 'test_files/test.csv')
    log_path = os.path.join(dir_path, 'test_files/test_log.txt')

    test_frame = {'Player Name': {'[00:01:10] 70.10': 'Ana'}, 'Hero Name': {'[00:01:10] 70.10': 'Ana'}, 'Damage Dealt': {'[00:01:10] 70.10': 0}, 'Barrier Damage': {'[00:01:10] 70.10': 0}, 'Damage Blocked': {'[00:01:10] 70.10': 0}, 'Damage Taken': {'[00:01:10] 70.10': 0}, 'Deaths': {'[00:01:10] 70.10': 0}, 'Elims': {'[00:01:10] 70.10': 0}, 'Final Blows': {'[00:01:10] 70.10': 0}, 'Env Deaths': {'[00:01:10] 70.10': 0}, 'Env Kills': {'[00:01:10] 70.10': 0}, 'Healing': {'[00:01:10] 70.10': 0}, 'Obj Kills': {'[00:01:10] 70.10': 0}, 'solo kills': {'[00:01:10] 70.10': 0}, 'Ults Earned': {'[00:01:10] 70.10': 0}, 'Ults Used': {'[00:01:10] 70.10': 0}, 'Healing Recived': {'[00:01:10] 70.10': 0}, 'Team': {'[00:01:10] 70.10': 'Team 1'}}

    class TestStringMethods(unittest.TestCase):
        def test_file_len(self):
            self.assertEqual(file_len(csv_path), 5)

        def test_read_csv_file(self):
            self.assertEqual(read_csv_file(log_path).to_dict(), test_frame)

        def test_check_file_change(self):
            self.assertEqual(check_file_change(log_path),"[00:00:00] Antarctic Peninsula")

    unittest.main()