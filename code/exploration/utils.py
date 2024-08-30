import pandas as pd
import os
from settings.params import CLEANING_COST

def combine_excel_files(files):
    """
    Combine multiple Excel and CSV files into a single DataFrame by appending the data.

    This function reads data from a list of file paths, which can be either Excel (`.xlsx`) or CSV (`.csv`) files.
    It strips whitespace from column names, concatenates the data from all files into a single DataFrame, 
    and returns the combined result. If a file format is unsupported, the function raises a ValueError.

    Parameters:
    - files (list of str): A list of file paths to be combined. The files can be in Excel (`.xlsx`) or CSV (`.csv`) format.

    Returns:
    - pd.DataFrame: A DataFrame containing the combined data from all specified files.

    Raises:
    - ValueError: If a file format other than `.xlsx` or `.csv` is provided.
    """

    data_frames = []

    for file in files:
        
        if file.endswith(".xlsx"):
            df = pd.read_excel(file)
        elif file.endswith(".csv"):
            df = pd.read_csv(file)
        else:
            raise ValueError(f"Unsupported file format for file: {file}")

        df.columns = df.columns.str.strip()
        data_frames.append(df)
    
    combined_df = pd.concat(data_frames, ignore_index=True)

    return combined_df

def filter_by_month(data, month):
    """
    Filter a DataFrame to include only rows where the reservation overlaps with a specific month.

    This function filters the input DataFrame to include only those rows where the 'Check out Date' is in the specified month or later, and the 'Check in Date' is in the specified month or earlier.
    It is useful for identifying reservations that are active or overlap within a given month.

    Parameters:
    - data (pd.DataFrame): The DataFrame containing reservation data. It must include 'Check out Date' and 'Check in Date' columns with datetime data type.
    - month (int): The month to filter by, represented as an integer (e.g., 1 for January, 12 for December).

    Returns:
    - pd.DataFrame: A filtered DataFrame containing only the rows that meet the month overlap criteria.
    """

    filtered_data = data[(data['Check out Date'].dt.month >= month) & (data['Check in Date'].dt.month <= month)]

    return filtered_data

def filter_by_status(data, statuses):
    """
    Filter the DataFrame based on specified reservation statuses.

    This function filters rows of the input DataFrame based on the values in the "Status" column.
    If the "Cancelled" status is included in the list of statuses, it will further filter those
    rows to include only those where the "Amount Paid" is greater than zero.

    Parameters:
    - data (pd.DataFrame): The DataFrame containing reservation data, including "Status" and "Amount Paid" columns.
    - statuses (list of str): A list of status values to filter by. If "Cancelled" is included, only rows with 
    "Amount Paid" greater than zero will be considered for "Cancelled" reservations.

    Returns:
    - pd.DataFrame: A DataFrame filtered by the specified statuses and conditions for "Cancelled" reservations.
    """

    if "Cancelled" in statuses:
        return data[(data["Status"].isin(statuses)) & (data["Amount Paid"] > 0)]
    else:
        return data[data["Status"].isin(statuses)]
    
def duplicate_rows_by_split(data, column_name, separator):
    """
    Split the values in the specified column using a separator and duplicate rows accordingly.

    Parameters:
    - data (pd.DataFrame): The DataFrame containing the data.
    - column_name (str): The name of the column to split.
    - separator (str): The separator used to split the column values.

    Returns:
    - pd.DataFrame: A new DataFrame with rows duplicated and the specified column split.
    """

    rows = []

    for _, row in data.iterrows():
        values = str(row[column_name]).split(separator)

        for value in values:
            new_row = row.copy()
            new_row[column_name] = value.strip()
            rows.append(new_row)

    return pd.DataFrame(rows)

def import_to_excel(data_frame, name, output_path, year, month):
    """
    Export a DataFrame to an Excel file.

    This function takes a pandas DataFrame and exports it to an Excel file using the specified file name and output path.
    The file is saved with a `.xlsx` extension, and the index is not included in the exported file.

    Parameters:
    - data_frame (pd.DataFrame): The pandas DataFrame to be exported to Excel.
    - name (str): The name of the Excel file (without the extension). This name will be used as the filename.
    - output_path (str): The directory path where the Excel file will be saved. The file will be saved at the specified location with the given name.

    Returns:
    - None: The function saves the DataFrame to an Excel file but does not return any value.

    Notes:
    - The function uses the `openpyxl` engine to write the Excel file, which must be installed for this function to work.
    - If the specified output path does not exist, an error will be raised. Ensure that the output path is valid and accessible.
    - The resulting Excel file will not include the DataFrame's index unless explicitly modified in the function call.
    """

    path = os.path.join(output_path, str(year), month)

    if not os.path.exists(path):
        os.makedirs(path)

    file_path = os.path.join(path, f"{name}.xlsx")
    data_frame.to_excel(file_path, engine='openpyxl', index=False)

def convert_to_datetime(row, column_name, format):
    """
    Convert a column in a row to datetime format, handling multiple date formats.

    Parameters:
    - row (pd.Series): The row of the DataFrame.
    - column_name (str): The name of the column to convert.

    Returns:
    - pd.Timestamp: The converted datetime.
    """

    return pd.to_datetime(row[column_name], format=format)

def drop_columns(df, columns_to_drop):
    """
    Drop specified columns from the DataFrame.

    This function removes columns from the DataFrame based on the list provided. If a column specified in the list does not exist in the DataFrame, it will be ignored without raising an error.

    Parameters:
    - df (pd.DataFrame): The DataFrame from which columns need to be removed.
    - columns_to_drop (list of str): A list of column names to be dropped from the DataFrame.

    Returns:
    - pd.DataFrame: A DataFrame with the specified columns removed.
    """

    df = df.drop(columns=columns_to_drop, errors="ignore")

    return df

def extract_columns(source_id, extract_columns, rename_columns=None, data=None):
    """
    Extract specific columns from a DataFrame or an Excel file path, rename columns if specified, and convert a column to a string type.

    Parameters:
    - source_id (str): The name of the column to be converted to a string.
    - extract_columns (list of str): A list of column names to be extracted.
    - rename_columns (dict, optional): A dictionary for renaming columns in the format {'old_name': 'new_name'}.
    - data (pd.DataFrame or str): A DataFrame to extract columns from or a string path to an Excel file.

    Returns:
    - pd.DataFrame: A DataFrame containing the extracted columns with the specified source ID column converted to a string type.
    """

    # Check if `data` is a file path (str) or a DataFrame
    if isinstance(data, str):
        df = pd.read_excel(data)
    elif isinstance(data, pd.DataFrame):
        df = data
    else:
        raise ValueError("The 'data' parameter must be either a file path (str) or a DataFrame.")
    
    if rename_columns:
        df = df.rename(columns=rename_columns)

    columns_to_merge = df.loc[:, extract_columns]

    columns_to_merge[source_id] = columns_to_merge[source_id].astype(str)

    return columns_to_merge

def define_building(row):
    """
    Assign a building name based on the room number.

    This function takes a row from a DataFrame and checks the value in the "Room Number" column. It returns a specific building name based on predefined conditions. The building names are assigned as follows:

    - "Le Clock" if the room number is "Le Clock".
    - "Le Majestic" if the room number is "Le Majestic".
    - "No name" if the room number is missing (NaN) or an empty string.
    - "Les Vues de Mont Royal" for specific room numbers: "2-4131", "1-4131", "2-4133".
    - "Le Main" for specific descriptive room names related to the city center.
    - "Luxury Apart-Hotel" as a default category for all other room numbers.

    Parameters:
    - row (pd.Series): A row of the DataFrame containing the "Room Number" column.

    Returns:
    - str: The building name corresponding to the room number.
    """

    room = row["Room Number"]

    if room == "Le Clock":
        return "Le Clock"
    elif room == "Le Majestic":
        return "Le Majestic"
    elif pd.isna(room) or room == "":
        return "No name"
    elif room in ["2-4131", "1-4131", "2-4133"]:
        return "Les Vues de Mont Royal"
    elif room in ["Le Moderne Nouveau Studio Rénové Centre-ville", "Loft sur la Main-Cœur de Montréal Centre-ville", "Le Chic Nouveau Studio Rénové Centre-ville", "Le Loft Trendy centre-ville de Montréal", "Studio centre-ville Montreal"]:
        return "Le Main"
    else:
        return "Luxury Apart-Hotel"
    
def define_cross(row, month):
    """
    Check if a reservation crosses over into a new month or crosses out of a month.

    Parameters:
    - row (pd.Series): A row from a DataFrame containing 'Check in Date' and 'Check out Date'.
    - month (int): The month number to check against (1 for January, 12 for December).

    Returns:
    - str: Returns 'crossover' if the reservation starts in a previous month, 'crossinto' if the reservation ends in a later month, otherwise returns an empty string.
    """

    check_in_month = row["Check in Date"].month
    check_out_month = row["Check out Date"].month

    if check_in_month < month:
        return "crossover"
    elif check_out_month > month:
        return "crossinto"
    else:
        return ""
    
def calculate_cleaning(row):
    """
    Calculate the cleaning cost based on the room number and the length of stay.

    This function calculates the cleaning cost for a room based on the room number, the number of nights stayed, and the building category. The calculation follows these rules:

    - The cleaning flag is set to 2 if the building is "Luxury Apart-Hotel" and the stay is 14 nights or more; otherwise, it is set to 1.
    - Cleaning costs are determined based on the room number suffix or specific room names:
        - For room numbers ending in "08" or "05", the cost is based on "hotel_2br".
        - For room numbers ending in "01", "02", "03", "04", "06", "07", or "09", the cost is based on "hotel_1br".
        - Specific room numbers ("2-4131", "1-4131", "2-4133") use the cost for "mont_royal".
        - Specific room names ("Le Majestic", "Le Clock", etc.) use their respective costs.
        - All other room numbers are set to a cleaning cost of 0.

    Parameters:
    - row (pd.Series): A row of the DataFrame containing "Room Number", "Nights", and "building" columns.

    Returns:
    - float: The total cleaning cost, adjusted by the cleaning flag.
    """

    room_name = str(row["Room Number"])
    nights_count = row["Nights"]
    if row["Building"] == "Luxury Apart-Hotel":
        cleaning_flag = 2 if nights_count >= 14 else 1
    else:
        cleaning_flag = 1

    if(room_name[-2:] in ["08", "05"]):
        cleaning = CLEANING_COST["hotel_2br"]
    elif(room_name[-2:] in ["01", "02", "03", "04", "06", "07", "09"]):
        cleaning = CLEANING_COST["hotel_1br"]
    elif(room_name in ["2-4131", "1-4131", "2-4133"]):
        cleaning = CLEANING_COST["mont_royal"]
    elif(room_name == "Le Majestic"):
        cleaning = CLEANING_COST["le_majestic"]
    elif(room_name == "Le Clock"):
        cleaning = CLEANING_COST["le_clock"]
    elif room_name in ["Studio centre-ville Montreal", "Le Moderne Nouveau Studio Rénové Centre-ville", "Loft sur la Main-Cœur de Montréal Centre-ville", "Le Loft Trendy centre-ville de Montréal", "Le Petit Penthouse centre-ville Montreal", "Le Chic Nouveau Studio Rénové Centre-ville"]:
        cleaning = CLEANING_COST["le_main"]
    else:
        cleaning = 0
    
    return cleaning * cleaning_flag

# Functions for columns formatting
def format_to_text(df, column_name):
    """
    Standardize text in a column (e.g., trim whitespace, convert to uppercase).

    Parameters:
    - df (pd.DataFrame): The DataFrame containing the column to format.
    - column_name (str): The name of the column to standardize.

    Returns:
    - pd.DataFrame: The DataFrame with the specified column standardized.
    """
    df[column_name] = df[column_name].astype(str).str.strip()

    return df