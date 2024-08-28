import pandas as pd
from utils import filter_by_month, convert_to_datetime, drop_columns
from settings.env import SOURCE_FILE_PATH
from settings.constants import COLUMNS_TO_RENAME, COLUMNS_TO_DROP, DATE_FOR_REPORT, IDS

df = pd.read_csv(SOURCE_FILE_PATH["airbnb_reservations"][1])

def process_files(df, rename_columns, columns_to_drop, month):
    """
    Process the Airbnb reservations data by renaming columns, filtering out specific types, and formatting the dates.

    Parameters:
    - df (pd.DataFrame): The DataFrame containing Airbnb reservations data.
    - rename_columns (dict): A dictionary mapping old column names to new column names.
    - columns_to_drop (list of str): A list of column names to drop from the DataFrame.
    - month (int): The month number to filter the data by.

    Returns:
    - pd.DataFrame: The processed DataFrame.
    """

    # Convert 'Start date' and 'End date' to datetime
    df["Start date"] = df.apply(convert_to_datetime, axis=1, column_name="Start date", format='%m/%d/%Y')
    df["End date"] = df.apply(convert_to_datetime, axis=1, column_name="End date", format='%m/%d/%Y')

    # Rename columns
    df = df.rename(columns=rename_columns)

    # Filter out rows where 'Type' is 'Payout' and by specified month
    df_filtered = df[df["Type"] != "Payout"]
    df_filtered = filter_by_month(df, month)

    # Drop specified columns
    df_filtered = drop_columns(df_filtered, columns_to_drop)

    # Add extra columns
    df_filtered["Source"] = "Airbnb (API)"
    df_filtered["Amount Paid"] = df_filtered["Grand Total"] - df_filtered["Airbnb marketing"]
    df_filtered[IDS["cloudbeds"]] = "Airbnb (API) Stefan" + " " + df_filtered[IDS["third_party"]]

    df_filtered = df_filtered.drop(columns=["Airbnb marketing"], errors="ignore")

    return df_filtered

temp_airbnb_reservations_df = process_files(df, COLUMNS_TO_RENAME["temp_account_airbnb_invoice"], COLUMNS_TO_DROP["temp_account_airbnb"], DATE_FOR_REPORT["month"])
