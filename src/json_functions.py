from json import load

def get_spreadsheet_id():
    with open("config.json", 'r') as file:
        data = load(file)
        return data.get("Spreadsheet ID", None)

def get_spreadsheet_pages():
    with open("config.json", 'r') as file:
        data = load(file)
        return data.get("Spreadsheet Pages", None)