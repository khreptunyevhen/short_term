import pandas as pd

def get_combine_excel_file(input_files, columns_to_drop=None):
    """Combine multiple files into one by adding at the bottom"""

    files = []

    for source, file_path in input_files.items():
        
        if file_path.endswith(".xlsx"):
            read_file = pd.read_excel(file_path)
        elif file_path.endswith(".csv"):
            read_file = pd.read_csv(file_path)
        else:
            raise ValueError(f"Unsupported file format for file: {file_path}")

        read_file.columns = read_file.columns.str.strip()
        files.append(read_file)
    
    combined_df = pd.concat(files, ignore_index=True)
    
    if columns_to_drop:
        combined_df.drop(columns=columns_to_drop, inplace=True, errors="ignore")

    return combined_df

def import_file(input_file, name, output_path):
    """Create an Excel file"""

    input_file.to_excel(f"{output_path}/{name}.xlsx", engine='openpyxl', index=False)

def get_month(date):
    """Convert text data format to month number “28/06/2024” -> 6"""

    month = int(date[3:5])
    return month

def get_month_data(month, check_in_col_name, check_out_col_name, data):
    """Filter data by a specific month"""

    # create the helpers columns to get the month
    data["check_in_month"] = data[check_in_col_name].apply(get_month)
    data["check_out_month"] = data[check_out_col_name].apply(get_month)

    filtered_data = data[(data['check_out_month'] >= month) & (data['check_in_month'] <= month)]

    # remove the helpers columns
    # filtered_data = filtered_data.drop(columns = ["check_in_month", "check_out_month"])

    return filtered_data

def filter_by_status(status, data):
    """Filter data by the reservation status"""

    if "Cancelled" in status:
        return data[(data["Status"].isin(status)) & (data["Amount Paid"] > 0)]
    else:
        return data[data["Status"].isin(status)]

def split_rows(data):
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

def merge_left(data_1, data_2, merge_col_name, data_1_col_name="Reservation Number", data_2_col_name="Res #"):
    data_1.rename(columns={data_1_col_name : merge_col_name}, inplace=True)
    data_2.rename(columns={data_2_col_name : merge_col_name}, inplace=True)

    merged_df = pd.merge(data_1, data_2, on=merge_col_name, how="left")
    return merged_df