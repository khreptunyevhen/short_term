import pandas as pd

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