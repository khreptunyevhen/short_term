import pandas as pd
from utils import combine_excel_files, filter_by_month, filter_by_status, duplicate_rows_by_split, convert_to_datetime
from settings.env import CB_RESERVATIONS
from settings.constants import CB_COLUMNS_TO_DROP, DATE_FOR_REPORT

def process_files(files, statuses, drop_columns, month):
    """
    Process multiple files by combining, cleaning, filtering, and formatting the data.

    Parameters:
    - files (list of str): List of file paths to combine.
    - statuses (list of str): List of reservation statuses to filter.
    - drop_columns (list of str): List of columns to drop from the DataFrame.
    - month (int): The month number to filter the data by.

    Returns:
    - pd.DataFrame: The processed DataFrame with combined, cleaned, filtered, and formatted data.
    """
    
    combined_df = combine_excel_files(files)

    combined_df["Check in Date"] = combined_df.apply(convert_to_datetime, axis=1, column_name="Check in Date")
    combined_df["Check out Date"] = combined_df.apply(convert_to_datetime, axis=1, column_name="Check out Date")

    filtered_status_df = filter_by_status(combined_df, statuses)
    filtered_month_df = filter_by_month(filtered_status_df, month)

    splitted_df = duplicate_rows_by_split(filtered_month_df, "Room Number", ", ")

    splitted_df = splitted_df.drop(columns=drop_columns, errors="ignore")

    return splitted_df

splitted = process_files(CB_RESERVATIONS, ["Checked Out", "In-House", "Confirmed"], CB_COLUMNS_TO_DROP, DATE_FOR_REPORT["month"])