from pandas import read_csv, DataFrame, notnull


def read_csv_file(file_to_read: str) -> DataFrame:
    """
    Reads a specific CSV file and processes it into a DataFrame.

    This function reads the provided CSV file, skips certain rows, and assigns custom column names.
    It also replaces specific values in the "Hero Name" column and sorts the DataFrame based on the "Team" column.

    Args:
        file_to_read (str): Path to the CSV file to be read.

    Returns:
        pd.DataFrame: Processed DataFrame with the relevant data.
    """
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
        "Team",
    ]

    df = read_csv(
        file_to_read,
        skiprows=range(1, file_len(file_to_read) - 9),
        header=0,
        names=column_names,
        encoding="utf-8",
    )

    df["Hero Name"] = df["Hero Name"].replace(
        {"LÃºcio": "Lucio", "TorbjÃ¶rn": "Torbjorn"}
    )
    df = df.where(notnull(df), "Not Selected")
    df = df.sort_values(by="Team", ascending=True)
    return df


def export_to_csv(df: DataFrame, file_name: str):
    """
    Exports a given DataFrame to a CSV file in a specified directory.

    Args:
        df (pd.DataFrame): The DataFrame to be exported.
        file_name (str): The name of the output CSV file. The file will be saved in the "CSVs" directory.

    Returns:
        None
    """
    df.to_csv(file_name, index=False)


def check_file_change(file_to_read: str) -> str:
    """
    Checks the first column name of the given CSV file.

    Args:
        file_to_read (str): Path to the CSV file to be checked.

    Returns:
        str: The name of the first column in the CSV file.
    """
    fp = read_csv(file_to_read, nrows=0, encoding="utf-8")
    return fp.columns.to_list()[0]


def file_len(file_to_read: str) -> int:
    """
    Calculates the number of rows in the given CSV file.

    Args:
        file_to_read (str): Path to the CSV file whose length is to be determined.

    Returns:
        int: The number of rows in the CSV file.
    """
    fp = read_csv(file_to_read, encoding="utf-8")
    return fp.shape[0]
