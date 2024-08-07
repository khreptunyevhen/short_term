import pandas as pd
from helpers import merge_with_selected_columns, define_building, define_cross, calculate_cleaning
from variables import DATE_FOR_REPORT, EXTERNAL_SOURCE_FILES

def create_ota_marketing_report(reservations_df, transactions_df):
    # Load data
    expedia_df = pd.read_excel(EXTERNAL_SOURCE_FILES["expedia"])
    booking_df = pd.read_excel(EXTERNAL_SOURCE_FILES["booking"])
    airbnb_df = pd.read_csv(EXTERNAL_SOURCE_FILES["airbnb"])

    airbnb_df_filtered = airbnb_df[airbnb_df["Type"] != "Payout"]

    merge_col = "Reservation_id"

    # Change type for the reservations ID
    booking_df["Reservation number"] = booking_df["Reservation number"].astype(str)
    expedia_df["Reservation ID"] = expedia_df["Reservation ID"].astype(str)

    # Merge data
    df_with_debit = merge_with_selected_columns(reservations_df, transactions_df, merge_col, "Reservation Number", "Res #")
    merged_with_booking_df = merge_with_selected_columns(df_with_debit, booking_df, "Third Party Confirmation Number", "Third Party Confirmation Number", "Reservation number", ["Commission amount"])
    merged_with_expedia_df = merge_with_selected_columns(merged_with_booking_df, expedia_df, "Third Party Confirmation Number", "Third Party Confirmation Number", "Reservation ID", ["Total Amount Due"])
    merged_with_airbnb_df = merge_with_selected_columns(merged_with_expedia_df, airbnb_df_filtered, "Third Party Confirmation Number", "Third Party Confirmation Number", "Confirmation Code", ["Amount", "Service fee", "Gross earnings"])

    # Rename columns
    merged_with_airbnb_df.rename(columns={"Amount" : "airbnb_paid", "Service fee" : "airbnb_commission", "Gross earnings" : "airbnb_total", "Total Amount Due" : "expedia_marketing", "Commission amount" : "booking_marketing"}, inplace=True, errors="ignore")

    merged_with_airbnb_df["notes"] = ""

    # Calculate taxes
    merged_with_airbnb_df["lodging_tax"] = round(merged_with_airbnb_df.apply(lambda row: row["Accommodation Total"] * 0.035 if row["Source"] != "Airbnb (API)" else 0, axis=1), 2)
    merged_with_airbnb_df["gst"] = round(merged_with_airbnb_df.apply(lambda row: (row["lodging_tax"] + row["Accommodation Total"]) * 0.05 if row["Source"] != "Airbnb (API)" else 0, axis=1), 2)
    merged_with_airbnb_df["qst"] = round(merged_with_airbnb_df.apply(lambda row: (row["lodging_tax"] + row["Accommodation Total"]) * 0.09975 if row["Source"] != "Airbnb (API)" else 0, axis=1), 2)

    merged_with_airbnb_df["building"] = merged_with_airbnb_df.apply(define_building, axis=1)

    # Calculate balance due
    merged_with_airbnb_df["balance_due"] = round(merged_with_airbnb_df["Accommodation Total"] + merged_with_airbnb_df["lodging_tax"] + merged_with_airbnb_df["gst"] + merged_with_airbnb_df["qst"] - merged_with_airbnb_df["Grand Total"], 2)

    merged_with_airbnb_df["cross"] = merged_with_airbnb_df.apply(define_cross, axis=1, args=(DATE_FOR_REPORT["month"],))

    merged_with_airbnb_df["Cleaning_+20%"] = merged_with_airbnb_df.apply(calculate_cleaning, axis=1)

    merged_with_airbnb_df = merged_with_airbnb_df.drop(columns=["Lodging Tax", "Good and Services Tax", "Quebec Sales Tax", "check_in_month", "check_out_month", "Status", "Cancelation fee"])
    merged_with_airbnb_df["Third Party Confirmation Number"] = merged_with_airbnb_df["Third Party Confirmation Number"].astype(str)

    # Desired column order
    desired_order = ["Accommodation Total", "Amount Paid", "balance_due", "lodging_tax", "gst", "qst", "Grand Total", "Debit", "Check in Date", "Check out Date", "Nights", "Reservation_id", "Third Party Confirmation Number", "Name", "Room Number", "building", "Source", "Cleaning_+20%", "booking_marketing", "expedia_marketing", "airbnb_paid", "airbnb_commission", "airbnb_total", "cross", "notes"]

    merged_with_airbnb_df = merged_with_airbnb_df.reindex(columns=desired_order)

    merged_with_airbnb_df["Reservation_id"] = merged_with_airbnb_df["Reservation_id"].astype(int)

    return merged_with_airbnb_df