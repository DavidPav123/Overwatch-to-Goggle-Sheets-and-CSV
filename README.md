# Overwatch matches data to Google Sheets and CSV

## Usage:

1. Download the latest release of this project and unzip it.
2. In the ***config.json*** file, change the ***Spreadsheet ID*** parameter to your spreadsheet's ID.
3. In the ***config.json*** file, change the ***Spreadsheet Pages*** parameter to the pages where the data should be uploaded.
4. Place a ***credentials.json*** file containing the Google Sheets API key in the same directory as the ***stats_to_GS.exe*** file. The first time the program is run, it will prompt for a login.
5. To run the program, double-click on ***overwatch-to-gs-csv.exe. The program will wait until a new log file appears in your Overwatch Workshop folder. A log file of your game will be automatically created once you start a custom game with workshop logging enabled. Once a new log file is detected, the data from the game will be uploaded to the provided Google spreadsheet and exported to a CSV file. When a new game starts, the program will automatically switch to uploading the data from that game to the next spreadsheet page. Once the program runs out of spreadsheet pages, it will automatically exit.

## Notes:
- If the program accidentally closes or crashes mid-series, once it is reopened, it will not upload again until the next match starts. Once it's reopened, it will overwrite the previous data, so be sure to move the previous data to a safe place before the next match starts.
- CSV files will automatically be named ***game1.csv, game2.csv, ect*** and will appear in the CSVs folder. If you open a CSV file mid-game, data will not be uploaded to the CSV file until it is closed.
- If matches end before spreadsheet pages run out, close the program to stop it, all data is automatically uploaded and exported to CSV files.
- If the prvious match was played on the same map, the code will not switch over.
