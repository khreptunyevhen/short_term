from utils import define_building, define_cross, calculate_cleaning
from combined_reservations import merged_reservations
from settings.constants import TAXES, DATE_FOR_REPORT, COLUMN_ORDER

def add_additional_columns(data):

    # Calculate taxes
    data["Lodging Tax"] = round(data.apply(lambda row: row["Accommodation Total"] * TAXES["lodging_tax"] if row["Source"] != "Airbnb (API)" else 0, axis=1), 2)
    data["GST"] = round(data.apply(lambda row: (row["Lodging Tax"] + row["Accommodation Total"]) * TAXES["qst"] if row["Source"] != "Airbnb (API)" else 0, axis=1), 2)
    data["QST"] = round(data.apply(lambda row: (row["Lodging Tax"] + row["Accommodation Total"]) * TAXES["gst"] if row["Source"] != "Airbnb (API)" else 0, axis=1), 2)

    # Add additional columns
    data["Balance Due"] = round(data["Accommodation Total"] + data["Lodging Tax"] + data["GST"] + data["QST"] - data["Grand Total"], 2)
    data["Building"] = data.apply(define_building, axis=1)
    data["Cross"] = data.apply(define_cross, axis=1, args=(DATE_FOR_REPORT["month"],))
    data["Cleaning"] = data.apply(calculate_cleaning, axis=1)
    data["Total marketing (no Airbnb)"] = data["Booking marketing"] + data["Expedia marketing"] + data["VRBO marketing"]

    return data

def reorder_columns(data, order):
    """Reorder columns in the DataFrame to match the desired order."""
    return data.reindex(columns=order)

def create_final_reservations():
    reservations_df = add_additional_columns(merged_reservations)
    reservations_df = reorder_columns(reservations_df, COLUMN_ORDER)

    return reservations_df