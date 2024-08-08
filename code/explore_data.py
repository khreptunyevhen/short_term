import pandas as pd
from helpers import merge_with_selected_columns, define_building, define_cross, calculate_cleaning
from variables import DATE_FOR_REPORT, EXTERNAL_SOURCE_FILES, TAXES, COLUMN_ORDER
from airbnb import process_airbnb_reservations

def load_ota_data():
    """Load data from external sources (Expedia, Booking, Airbnb)."""
    expedia_df = pd.read_excel(EXTERNAL_SOURCE_FILES["expedia"])
    booking_df = pd.read_excel(EXTERNAL_SOURCE_FILES["booking"])
    airbnb_df = pd.read_csv(EXTERNAL_SOURCE_FILES["airbnb"])

    return (expedia_df, booking_df, airbnb_df)

def merge_reservation_data(ota_reservations, cb_reservations, cb_transactions):
    """Merge OTA and Cloudbeds reservation data with relevant columns."""
    expedia_df, booking_df, airbnb_df = ota_reservations

    # Ensure reservation ID columns are strings
    booking_df["Reservation number"] = booking_df["Reservation number"].astype(str)
    expedia_df["Reservation ID"] = expedia_df["Reservation ID"].astype(str)
    cb_reservations["Third Party Confirmation Number"] = cb_reservations["Third Party Confirmation Number"].astype(str)

    airbnb_df_filtered = airbnb_df[airbnb_df["Type"] != "Payout"]

    # Merge dataframes
    reservations_with_debit = merge_with_selected_columns(cb_reservations, cb_transactions, "Reservation_id", "Reservation Number", "Res #")
    merged_with_booking = merge_with_selected_columns(reservations_with_debit, booking_df, "Third Party Confirmation Number", "Third Party Confirmation Number", "Reservation number", ["Commission amount"])
    merged_with_expedia = merge_with_selected_columns(merged_with_booking, expedia_df, "Third Party Confirmation Number", "Third Party Confirmation Number", "Reservation ID", ["Total Amount Due"])
    merged_with_airbnb = merge_with_selected_columns(merged_with_expedia, airbnb_df_filtered, "Third Party Confirmation Number", "Third Party Confirmation Number", "Confirmation Code", ["Amount", "Service fee", "Gross earnings"])

    return merged_with_airbnb

def add_additional_columns(data):
    """Add calculated columns to the merged reservation data."""
    # Rename columns
    data.rename(columns={"Amount" : "airbnb_paid", "Service fee" : "airbnb_marketing", "Gross earnings" : "airbnb_total", "Total Amount Due" : "expedia_marketing", "Commission amount" : "booking_marketing"}, inplace=True, errors="ignore")

    # Calculate taxes
    data["lodging_tax"] = round(data.apply(lambda row: row["Accommodation Total"] * TAXES["lodging_tax"] if row["Source"] != "Airbnb (API)" else 0, axis=1), 2)
    data["gst"] = round(data.apply(lambda row: (row["lodging_tax"] + row["Accommodation Total"]) * TAXES["gst"] if row["Source"] != "Airbnb (API)" else 0, axis=1), 2)
    data["qst"] = round(data.apply(lambda row: (row["lodging_tax"] + row["Accommodation Total"]) * TAXES["qst"] if row["Source"] != "Airbnb (API)" else 0, axis=1), 2)

    # Add additional columns
    data["balance_due"] = round(data["Accommodation Total"] + data["lodging_tax"] + data["gst"] + data["qst"] - data["Grand Total"], 2)
    data["building"] = data.apply(define_building, axis=1)
    data["cross"] = data.apply(define_cross, axis=1, args=(DATE_FOR_REPORT["month"],))
    data["Cleaning_+20%"] = data.apply(calculate_cleaning, axis=1)
    data["notes"] = ""

    return data

def reorder_columns(data, order):
    """Reorder columns in the DataFrame to match the desired order."""
    return data.reindex(columns=order)

def process_reservations(current_reservations, cb_sum_debit):
    reservations_dfs = list(load_ota_data())
    merged_reservations = merge_reservation_data(reservations_dfs, current_reservations, cb_sum_debit)
    reservations_with_calculations = add_additional_columns(merged_reservations)
    reservations = reorder_columns(reservations_with_calculations, COLUMN_ORDER)

    airbnb_temporary_data = process_airbnb_reservations()

    final_reservations = pd.concat([reservations, airbnb_temporary_data], ignore_index=True)

    return final_reservations