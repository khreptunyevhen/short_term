import pandas as pd
from explore_cloudbeds_reservations import cloudbeds_reservations_df
from explore_temp_airbnb_reservations import temp_airbnb_reservations_df
from explore_airbnb_reservations import airbnb_columns_to_merge
from explore_booking_reservations import booking_columns_to_merge
from explore_expedia_reservations import expedia_columns_to_merge
from explore_vrbo_reservations import vrbo_columns_to_merge
from utils import import_to_excel
from settings.env import OUTPUT_FILE_PATH
from settings.constants import IDS

def merge_dfs(base_df, columns_to_merge_list, merge_key):
    """
    Merge multiple DataFrames with the base DataFrame using the specified merge key.

    Parameters:
    - base_df (pd.DataFrame): The base DataFrame to merge others into.
    - columns_to_merge_list (list of pd.DataFrame): List of DataFrames to merge with the base DataFrame.
    - merge_key (str): The column name on which to perform the merges.

    Returns:
    - pd.DataFrame: The merged DataFrame.
    """

    merged_df = base_df.copy()

    for df_to_merge in columns_to_merge_list:
        merged_df = pd.merge(merged_df, df_to_merge, on=merge_key, how="left")

    return merged_df

def combine_files():

    # Combine the initial dataframes
    combined_df = pd.concat([cloudbeds_reservations_df, temp_airbnb_reservations_df], axis=0, ignore_index=True)

    # List of dataframes to merge
    columns_to_merge_list = [airbnb_columns_to_merge, booking_columns_to_merge, expedia_columns_to_merge, vrbo_columns_to_merge]

    merged_df = merge_dfs(combined_df, columns_to_merge_list, IDS["third_party"])

    return merged_df

merged_reservations = combine_files()