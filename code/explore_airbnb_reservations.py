import numpy as np
from utils import combine_excel_files
from settings.env import SOURCE_FILE_PATH
from settings.constants import COLUMNS_TO_RENAME, COLUMNS_TO_KEEP, IDS
from utils import extract_columns

def process_files():
    combined_df = combine_excel_files(SOURCE_FILE_PATH["airbnb_reservations"])
    combined_df["Notes"] = np.where(combined_df['Type'] != "Reservation", combined_df['Type'].astype(str) + " - " + combined_df["Details"].astype(str), np.nan)
    combined_df = combined_df[combined_df["Type"] != "Payout"]

    return combined_df

combined_airbnb_df = process_files()

airbnb_columns_to_merge = extract_columns(IDS["third_party"], COLUMNS_TO_KEEP["airbnb_invoice"], COLUMNS_TO_RENAME["airbnb_invoice"], combined_airbnb_df)