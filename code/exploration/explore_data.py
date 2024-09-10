from utils import define_building, define_cross, calculate_cleaning
from combined_reservations import merged_reservations
from settings.constants import TAXES, DATE_FOR_REPORT, COLUMN_ORDER

def add_additional_columns(data):
    """
    Add additional calculated columns to the DataFrame.

    This function calculates and adds the following columns to the DataFrame:
    - "Lodging Tax": Computed as a percentage of "Accommodation Total", except for rows where the source is "Airbnb (API)".
    - "GST": Calculated as a percentage of the sum of "Lodging Tax" and "Accommodation Total", except for rows where the source is "Airbnb (API)".
    - "QST": Calculated as a percentage of the sum of "Lodging Tax" and "Accommodation Total", except for rows where the source is "Airbnb (API)".
    - "Balance Due": The difference between the total amount due and the grand total.
    - "Building": Determined by the `define_building` function.
    - "Cross": Determined by the `define_cross` function, with the current month passed as an argument.
    - "Cleaning": Calculated by the `calculate_cleaning` function.
    - "Total marketing (no Airbnb)": The sum of marketing amounts from various sources excluding Airbnb.

    Parameters:
    - data (pd.DataFrame): The DataFrame containing the original reservation data.

    Returns:
    - pd.DataFrame: The DataFrame with additional columns added.
    """

    # Calculate taxes
    data["Lodging Tax"] = round(data.apply(lambda row: row["Accommodation Total"] * TAXES["lodging_tax"] if row["Source"] != "Airbnb (API)" else 0, axis=1), 2)
    data["GST"] = round(data.apply(lambda row: (row["Lodging Tax"] + row["Accommodation Total"]) * TAXES["gst"] if row["Source"] != "Airbnb (API)" else 0, axis=1), 2)
    data["QST"] = round(data.apply(lambda row: (row["Lodging Tax"] + row["Accommodation Total"]) * TAXES["qst"] if row["Source"] != "Airbnb (API)" else 0, axis=1), 2)

    # Add additional columns
    data["Balance Due"] = round(data["Accommodation Total"] + data["Lodging Tax"] + data["GST"] + data["QST"] - data["Grand Total"], 2)
    data["Building"] = data.apply(define_building, axis=1)
    data["Cross"] = data.apply(define_cross, axis=1, args=(DATE_FOR_REPORT["month"],))
    data["Cleaning"] = data.apply(calculate_cleaning, axis=1)

    return data

def reorder_columns(data, order):
    """
    Reorder columns in the DataFrame to match the desired order.

    This function rearranges the columns of the DataFrame according to the specified order list.

    Parameters:
    - data (pd.DataFrame): The DataFrame with columns to be reordered.
    - order (list of str): The desired column order.

    Returns:
    - pd.DataFrame: The DataFrame with columns reordered as specified.
    """

    return data.reindex(columns=order)

def create_final_reservations():
    """
    Create the final reservations DataFrame by adding additional columns and reordering columns.

    This function processes the reservations data by first adding calculated columns and then reordering the columns based on the predefined order.

    Returns:
    - pd.DataFrame: The final reservations DataFrame with additional and reordered columns.
    """

    reservations_df = add_additional_columns(merged_reservations)
    reservations_df = reorder_columns(reservations_df, COLUMN_ORDER)

    return reservations_df

co = "co"