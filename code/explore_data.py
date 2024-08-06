import pandas as pd
from helpers import import_to_excel, merge_with_selected_columns, combine_excel_files
from variables import DATE_FOR_REPORT

cb_reservations = pd.read_excel(f"C:/projects/monthly_income/short_term/ota_marketing/{DATE_FOR_REPORT["year"]}{DATE_FOR_REPORT["month"]} - Reservations with OTA marketing.xlsx")

cb_transactions = pd.read_excel(f"C:/projects/monthly_income/short_term/ota_marketing/{DATE_FOR_REPORT["year"]}{DATE_FOR_REPORT["month"]} - Transaction summary.xlsx")

merge_col = "Reservation_id"

merged_df = merge_with_selected_columns(cb_reservations, cb_transactions, merge_col, "Reservation Number", "Res #")

merged_df["lod_tax"] = round(merged_df.apply(lambda row: row["Accommodation Total"] * 0.035 if row["Source"] != "Airbnb (API)" else 0, axis=1), 2)
merged_df["gst"] = round(merged_df.apply(lambda row: (row["lod_tax"] + row["Accommodation Total"]) * 0.05 if row["Source"] != "Airbnb (API)" else 0, axis=1), 2)
merged_df["qst"] = round(merged_df.apply(lambda row: (row["lod_tax"] + row["Accommodation Total"]) * 0.09975 if row["Source"] != "Airbnb (API)" else 0, axis=1), 2)

def define_building(row):
    room = row["Room Number"]

    if(room == "Le Clock"):
        return "Le Clock"
    elif(room == "Le Majestic"):
        return "Le Majestic"
    elif(pd.isna(room) or room == ""):
        return "Error"
    elif(room in ["2-4131", "1-4131", "2-4133"]):
        return "Les Vues de Mont Royal"
    else:
        return "Luxury Apart-Hotel"

merged_df["building"] = merged_df.apply(define_building, axis=1)

merged_df["balance_due"] = round(merged_df["Accommodation Total"] + merged_df["lod_tax"] + merged_df["gst"] + merged_df["qst"] - merged_df["Grand Total"], 2)

def define_cross(row, month):
    check_in = row["check_in_month"]
    check_out = row["check_out_month"]

    cross = ""

    if check_in < month:
        cross = "crossover"
    elif check_out > month:
        cross = "crossinto"
    else:
        cross = ""

    return cross

merged_df["cross"] = merged_df.apply(define_cross, axis=1, args=(DATE_FOR_REPORT["month"],))

def calculate_cleaning(row):  
    cleaning_flag = 1
    cleaning_sum = 0

    room_name = str(row["Room Number"])
    nights_count = row["Nights"]

    if(nights_count >= 14):
        cleaning_flag = 2

    if(room_name[-2:] in ["08", "05"]):
        cleaning = 90
    elif(room_name[-2:] in ["01", "02", "03", "04", "06", "07", "09"]):
        cleaning = 50
    elif(room_name in ["2-4131", "1-4131", "2-4133"]):
        cleaning = 60
    elif(room_name == "Le Majestic"):
        cleaning = 110
    elif(room_name == "Le Clock"):
        cleaning = 100
    else:
        cleaning = 0

    cleaning_sum = cleaning * cleaning_flag * 1.2
    
    return cleaning_sum 

merged_df["Cleaning_+20%"] = merged_df.apply(calculate_cleaning, axis=1)

merged_df["Additional_fees"] = ""

def calculate_fee(row, fee):
    additional_fee = float(row["balance_due"])

    fees = 0

    if(pd.isna(additional_fee)):
        return 0

    if(additional_fee > 1 or additional_fee < -1):
        fees = round(additional_fee / 1.14975 * fee, 2)
    
    return fees

merged_df["ad_gst"] = merged_df.apply(calculate_fee, axis=1, args=(0.05,))
merged_df["ad_qst"] = merged_df.apply(calculate_fee, axis=1, args=(0.09975,))

def calculate_final_fee(row):
    additional_fee = float(row["balance_due"])

    if(additional_fee > 1 or additional_fee < -1):
        return row["balance_due"] - row["ad_gst"] - row["ad_qst"]
    
    return 0

merged_df["ad_fee"] = merged_df.apply(calculate_final_fee, axis=1)

merged_df["notes"] = ""
merged_df["track"] = ""

merged_df = merged_df.drop(columns=["Lodging Tax", "Good and Services Tax", "Quebec Sales Tax", "check_in_month", "check_out_month", "Status", "Cancelation fee"])

merged_df["Third Party Confirmation Number"] = merged_df["Third Party Confirmation Number"].astype(str)

# merge with booking

booking_reservations = { 
    "past": "C:/projects/monthly_income/short_term/sources/reservations/booking/booking_current.xlsx",
    # "current": "C:/projects/monthly_income/short_term/sources/reservations/cloudbeds/werfy_luxury_apart_hotel_cloudbeds_reservations.xlsx"
}

booking_reservations_df = combine_excel_files(booking_reservations)
booking_reservations_df["Reservation number"] = booking_reservations_df["Reservation number"].astype(str)

merged_with_booking_df = merge_with_selected_columns(merged_df, booking_reservations_df, "Third Party Confirmation Number", "Third Party Confirmation Number", "Reservation number", ["Commission amount"])

import_to_excel(merged_with_booking_df, "OTA with debit", "C:/projects/monthly_income/short_term/ota_marketing/")