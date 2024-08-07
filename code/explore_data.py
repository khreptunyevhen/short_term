import pandas as pd
from helpers import import_to_excel, merge_with_selected_columns, combine_excel_files, define_building, define_cross, calculate_cleaning
from variables import DATE_FOR_REPORT, BOOKING_RESERVATION_FILES, EXPEDIA_TRANSACTION_FILES

def create_ota_marketing_report(reservations_df, transactions_df):
    # Load data
    # cb_reservations = pd.read_excel(f"C:/projects/monthly_income/short_term/ota_marketing/Current reservations.xlsx")
    # cb_transactions = pd.read_excel(f"C:/projects/monthly_income/short_term/ota_marketing/Transactions.xlsx")


    expedia_df = pd.read_excel(EXPEDIA_TRANSACTION_FILES["expedia"])
    booking_df = combine_excel_files(BOOKING_RESERVATION_FILES)
    airbnb_df = pd.read_csv("C:/projects/monthly_income/short_term/sources/reservations/airbnb/airbnb.csv")

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
    merged_with_airbnb_df.rename(columns={"Commission amount" : "booking_marketing"}, inplace=True, errors="ignore")
    merged_with_airbnb_df.rename(columns={"Total Amount Due" : "expedia_marketing"}, inplace=True, errors="ignore")
    merged_with_airbnb_df.rename(columns={"Amount" : "airbnb_paid", "Service fee" : "airbnb_commission", "Gross earnings" : "airbnb_total"}, inplace=True, errors="ignore")

    merged_with_airbnb_df["notes"] = ""

    # Calculate taxes
    merged_with_airbnb_df["lod_tax"] = round(merged_with_airbnb_df.apply(lambda row: row["Accommodation Total"] * 0.035 if row["Source"] != "Airbnb (API)" else 0, axis=1), 2)
    merged_with_airbnb_df["gst"] = round(merged_with_airbnb_df.apply(lambda row: (row["lod_tax"] + row["Accommodation Total"]) * 0.05 if row["Source"] != "Airbnb (API)" else 0, axis=1), 2)
    merged_with_airbnb_df["qst"] = round(merged_with_airbnb_df.apply(lambda row: (row["lod_tax"] + row["Accommodation Total"]) * 0.09975 if row["Source"] != "Airbnb (API)" else 0, axis=1), 2)

    merged_with_airbnb_df["building"] = merged_with_airbnb_df.apply(define_building, axis=1)

    # Calculate balance due
    merged_with_airbnb_df["balance_due"] = round(merged_with_airbnb_df["Accommodation Total"] + merged_with_airbnb_df["lod_tax"] + merged_with_airbnb_df["gst"] + merged_with_airbnb_df["qst"] - merged_with_airbnb_df["Grand Total"], 2)

    merged_with_airbnb_df["cross"] = merged_with_airbnb_df.apply(define_cross, axis=1, args=(DATE_FOR_REPORT["month"],))

    merged_with_airbnb_df["Cleaning_+20%"] = merged_with_airbnb_df.apply(calculate_cleaning, axis=1)

    merged_with_airbnb_df = merged_with_airbnb_df.drop(columns=["Lodging Tax", "Good and Services Tax", "Quebec Sales Tax", "check_in_month", "check_out_month", "Status", "Cancelation fee"])
    merged_with_airbnb_df["Third Party Confirmation Number"] = merged_with_airbnb_df["Third Party Confirmation Number"].astype(str)

    # Desired column order
    desired_order = ["Accommodation Total", "Amount Paid", "balance_due", "lod_tax", "gst", "qst", "Grand Total", "Debit", "Check in Date", "Check out Date", "Nights", "Reservation_id", "Third Party Confirmation Number", "Name", "Room Number", "building", "Source", "Cleaning_+20%", "booking_marketing", "expedia_marketing", "airbnb_paid", "airbnb_commission", "airbnb_total", "cross", "notes"]

    merged_with_airbnb_df = merged_with_airbnb_df.reindex(columns=desired_order)

    merged_with_airbnb_df["Reservation_id"] = merged_with_airbnb_df["Reservation_id"].astype(int)

    # import_to_excel(merged_with_airbnb_df, "OTA with debit", "C:/projects/monthly_income/short_term/ota_marketing/")

    return merged_with_airbnb_df