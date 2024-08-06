import pandas as pd

def combine_excel_files(file_paths, columns_to_drop=None):
    """Combine multiple files into one by adding at the bottom"""

    data_frames = []

    for source, file_path in file_paths.items():
        
        if file_path.endswith(".xlsx"):
            df = pd.read_excel(file_path)
        elif file_path.endswith(".csv"):
            df = pd.read_csv(file_path)
        else:
            raise ValueError(f"Unsupported file format for file: {file_path}")

        df.columns = df.columns.str.strip()
        data_frames.append(df)
    
    combined_df = pd.concat(data_frames, ignore_index=True)
    
    if columns_to_drop:
        combined_df.drop(columns=columns_to_drop, inplace=True, errors="ignore")

    return combined_df

def import_to_excel(data_frame, name, output_path):
    """Create an Excel file"""

    data_frame.to_excel(f"{output_path}/{name}.xlsx", engine='openpyxl', index=False)

def extract_month(date_str):
    """Convert text data format to month number “28/06/2024” -> 6"""

    return int(date_str[3:5])

def filter_by_month(month, check_in_col_name, check_out_col_name, data):
    """Filter data by a specific month"""

    # create the helpers columns to get the month
    data["check_in_month"] = data[check_in_col_name].apply(extract_month)
    data["check_out_month"] = data[check_out_col_name].apply(extract_month)

    filtered_data = data[(data['check_out_month'] >= month) & (data['check_in_month'] <= month)]

    # remove the helpers columns
    # filtered_data = filtered_data.drop(columns = ["check_in_month", "check_out_month"])

    return filtered_data

def filter_by_status(data, statuses):
    """Filter data by the reservation status"""

    if "Cancelled" in statuses:
        return data[(data["Status"].isin(statuses)) & (data["Amount Paid"] > 0)]
    else:
        return data[data["Status"].isin(statuses)]

def split_room_numbers(data):
    """Split and copy rows with multiple room numbers"""

    rows = []

    for _, row in data.iterrows():
        room_numbers = str(row["Room Number"]).split(", ")

        for room in room_numbers:
            new_row = row.copy()
            new_row["Room Number"] = room
            rows.append(new_row)
    return pd.DataFrame(rows)

def group_and_sum(data, group_col, sum_col):
    """Group the DataFrame by a specific column and sum another column"""
    
    sum = data.groupby(group_col, as_index=False)[sum_col].sum()
    return sum

def merge_with_selected_columns(left_df, right_df, merge_col_name, left_col_name, right_col_name, right_cols_to_keep=None):
    """
    Merge two DataFrames on a specified column, retaining only selected columns from the right DataFrame.

    Parameters:
    left_df (pd.DataFrame): The left DataFrame to merge.
    right_df (pd.DataFrame): The right DataFrame to merge.
    merge_col_name (str): The name of the column to merge on.
    left_col_name (str): The name of the merge column in the left DataFrame.
    right_col_name (str): The name of the merge column in the right DataFrame.
    right_cols_to_keep (list): List of columns to retain from the right DataFrame (including the merge column).

    Returns:
    pd.DataFrame: The merged DataFrame.
    """

    # Rename the columns in both DataFrames to the merge column name
    left_df.rename(columns={left_col_name: merge_col_name}, inplace=True)
    right_df.rename(columns={right_col_name: merge_col_name}, inplace=True)

    # If specific columns to keep from the right DataFrame are provided, select only those columns
    if right_cols_to_keep:
        right_df = right_df[[merge_col_name] + right_cols_to_keep]

    # Perform the left merge
    merged_df = pd.merge(left_df, right_df, on=merge_col_name, how="left")

    return merged_df