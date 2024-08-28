from utils import combine_excel_files, filter_by_month, filter_by_status, duplicate_rows_by_split, convert_to_datetime, format_to_text, import_to_excel, drop_columns
from settings.env import SOURCE_FILE_PATH
from settings.constants import COLUMNS_TO_DROP, DATE_FOR_REPORT, IDS

def process_files(files, statuses, columns_to_drop, month):
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

    combined_df["Check in Date"] = combined_df.apply(convert_to_datetime, axis=1, column_name="Check in Date", format='%d/%m/%Y')
    combined_df["Check out Date"] = combined_df.apply(convert_to_datetime, axis=1, column_name="Check out Date", format='%d/%m/%Y')

    filtered_status_df = filter_by_status(combined_df, statuses)
    filtered_month_df = filter_by_month(filtered_status_df, month)

    splitted_df = duplicate_rows_by_split(filtered_month_df, "Room Number", ", ")

    splitted_df = drop_columns(splitted_df, columns_to_drop)

    # Format to text
    splitted_df = format_to_text(splitted_df, IDS["cloudbeds"])

    return splitted_df

cloudbeds_reservations_df = process_files(SOURCE_FILE_PATH["cloudbeds_reservations"], ["Checked Out", "In-House", "Confirmed"], COLUMNS_TO_DROP["cloudbeds_reservations"], DATE_FOR_REPORT["month"])