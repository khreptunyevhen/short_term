import pandas as pd
from helpers import calculate_cleaning, filter_by_month, define_cross, extract_month
from variables import COLUMN_ORDER, TEMPORARY_AIRBNB_ACCOUNT_COLUMNS_TO_DROP, DATE_FOR_REPORT

def load_temporary_aibnb_data():
    df = pd.read_csv("C:/projects/monthly_income/short_term/sources/reservations/airbnb/airbnb_stefan.csv")
    df_filtered = df[df["Type"] != "Payout"]

    df_filtered = df_filtered.drop(columns=TEMPORARY_AIRBNB_ACCOUNT_COLUMNS_TO_DROP)

    return df_filtered

def filtered_temporary_aibnb_data(data):
    # Rename columns to match with the main OTA marketing final file
    data.rename(columns={
        "Confirmation Code" : "Third Party Confirmation Number",
        "Start date" : "Check in Date",
        "End date" : "Check out Date",
        "Nights" : "Nights",
        "Guest" : "Name",
        "Listing" : "Room Number",
        "Details" : "notes",
        "Amount" : "airbnb_paid",
        "Service fee" : "airbnb_marketing",
        "Gross earnings" : "airbnb_total",
    }, inplace=True)

    # Add columns to match with the main OTA marketing final file
    data["Accommodation Total"] = data["airbnb_paid"]
    data["Amount Paid"] = data["airbnb_paid"]
    data["balance_due"] = 0
    data["lodging_tax"] = 0
    data["gst"] = 0
    data["qst"] = 0
    data["Grand Total"] = data["airbnb_total"]
    data["Debit"] = data["airbnb_total"]
    data["Reservation_id"] = "Stefan " + data["Third Party Confirmation Number"].astype(str)
    data["building"] = "Le Main"
    data["Source"] = "Airbnb (API) Stefan"
    data["Cleaning_+20%"] = data.apply(calculate_cleaning, axis=1)
    data["booking_marketing"] = 0
    data["expedia_marketing"] = 0
    data["cross"] = ""
    data["Check in Date"] = data["Check in Date"].str[3:5] + "/" + data["Check in Date"].str[:2] + "/" + data["Check in Date"].str[-4:]
    data["Check out Date"] = data["Check out Date"].str[3:5] + "/" + data["Check out Date"].str[:2] + "/" + data["Check out Date"].str[-4:]


    data["check_in_month"] = data["Check in Date"].apply(extract_month)
    data["check_out_month"] = data["Check out Date"].apply(extract_month)
    data["cross"] = data.apply(define_cross, axis=1, args=(DATE_FOR_REPORT["month"],))
    # Filter by the current month
    # df_filtered = data[(data["Check in Date"].str[:2].astype(int) <= 6) & (data["Check out Date"].str[:2].astype(int) >= 6)]

    filtered_by_month = filter_by_month(DATE_FOR_REPORT['month'], "Check in Date", "Check out Date", data)

    # Order columns to match with the main OTA marketing final file
    df_filtered = filtered_by_month.reindex(columns=COLUMN_ORDER)

    return df_filtered

def process_airbnb_reservations():
    data = load_temporary_aibnb_data()
    filtered_data = filtered_temporary_aibnb_data(data)
    
    return filtered_data