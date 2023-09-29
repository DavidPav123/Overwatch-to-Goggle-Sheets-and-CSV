from json import load

def get_spreadsheet_id(file_name:str):
    with open(file_name, 'r') as file:
        data = load(file)
        return data.get("Spreadsheet ID", None)

def get_spreadsheet_pages(file_name):
    with open(file_name, 'r') as file:
        data = load(file)
        return data.get("Spreadsheet Pages", None)
    
if __name__ == "__main__":
    import os
    import unittest

    dir_path = os.path.dirname(os.path.realpath(__file__))
    config_path = os.path.join(dir_path, 'test_files/config.json')

    class TestStringMethods(unittest.TestCase):

        def test_get_spreadsheet_pages(self):
            self.assertEqual(get_spreadsheet_pages(config_path), ["Sheet1", "Sheet2", "Sheet3", "Sheet4", "Sheet5"])

        def test_get_spreadsheet_id(self):
            self.assertEqual(get_spreadsheet_id(config_path), "1_s8kTUCKG7wWY43Fa24knmBPAW-iV0uoNBLLUXUxLA0")

    unittest.main()