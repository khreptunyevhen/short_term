import pandas as pd
from helpers import import_to_excel, merge_with_selected_columns, combine_excel_files
from variables import DATE_FOR_REPORT, BOOKING_RESERVATION_FILES

# Load data
cb_reservations = pd.read_excel(f"C:/projects/monthly_income/short_term/ota_marketing/{DATE_FOR_REPORT["year"]}{DATE_FOR_REPORT["month"]} - Reservations with OTA marketing.xlsx")
cb_transactions = pd.read_excel(f"C:/projects/monthly_income/short_term/ota_marketing/{DATE_FOR_REPORT["year"]}{DATE_FOR_REPORT["month"]} - Transaction summary.xlsx")

# Merge data
merge_col = "Reservation_id"
merged_df = merge_with_selected_columns(cb_reservations, cb_transactions, merge_col, "Reservation Number", "Res #")

# Calculate taxes
merged_df["lod_tax"] = round(merged_df.apply(lambda row: row["Accommodation Total"] * 0.035 if row["Source"] != "Airbnb (API)" else 0, axis=1), 2)
merged_df["gst"] = round(merged_df.apply(lambda row: (row["lod_tax"] + row["Accommodation Total"]) * 0.05 if row["Source"] != "Airbnb (API)" else 0, axis=1), 2)
merged_df["qst"] = round(merged_df.apply(lambda row: (row["lod_tax"] + row["Accommodation Total"]) * 0.09975 if row["Source"] != "Airbnb (API)" else 0, axis=1), 2)

# Define building
def define_building(row):
    room = row["Room Number"]

    if room == "Le Clock":
        return "Le Clock"
    elif room == "Le Majestic":
        return "Le Majestic"
    elif pd.isna(room) or room == "":
        return "Error"
    elif room in ["2-4131", "1-4131", "2-4133"]:
        return "Les Vues de Mont Royal"
    else:
        return "Luxury Apart-Hotel"

merged_df["building"] = merged_df.apply(define_building, axis=1)

# Calculate balance due
merged_df["balance_due"] = round(merged_df["Accommodation Total"] + merged_df["lod_tax"] + merged_df["gst"] + merged_df["qst"] - merged_df["Grand Total"], 2)

# Define crosses
def define_cross(row, month):
    check_in = row["check_in_month"]
    check_out = row["check_out_month"]

    if check_in < month:
        return "crossover"
    elif check_out > month:
        return "crossinto"
    else:
        return ""

merged_df["cross"] = merged_df.apply(define_cross, axis=1, args=(DATE_FOR_REPORT["month"],))

# Calculate cleaning fee
def calculate_cleaning(row):  
    room_name = str(row["Room Number"])
    nights_count = row["Nights"]
    cleaning_flag = 2 if nights_count >= 14 else 1

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
    
    return cleaning * cleaning_flag * 1.2 

merged_df["Cleaning_+20%"] = merged_df.apply(calculate_cleaning, axis=1)


# FIXME:
# merged_df["Additional_fee_description"] = ""

# # Calculate additional fees
# def calculate_fee(row, fee):
#     additional_fee = float(row["balance_due"])

#     if(pd.isna(additional_fee)):
#         return 0

#     if(additional_fee > 1 or additional_fee < -1):
#         return round(additional_fee / 1.14975 * fee, 2)
    
#     return 0

# merged_df["additional_fee_gst"] = merged_df.apply(calculate_fee, axis=1, args=(0.05,))
# merged_df["additional_fee_qst"] = merged_df.apply(calculate_fee, axis=1, args=(0.09975,))

# def calculate_final_fee(row):
#     additional_fee = float(row["balance_due"])

#     if(additional_fee > 1 or additional_fee < -1):
#         return row["balance_due"] - row["additional_fee_gst"] - row["additional_fee_qst"]
    
#     return 0

# merged_df["ad_fee"] = merged_df.apply(calculate_final_fee, axis=1)

merged_df = merged_df.drop(columns=["Lodging Tax", "Good and Services Tax", "Quebec Sales Tax", "check_in_month", "check_out_month", "Status", "Cancelation fee"])
merged_df["Third Party Confirmation Number"] = merged_df["Third Party Confirmation Number"].astype(str)

# merge with booking
booking_reservations_df = combine_excel_files(BOOKING_RESERVATION_FILES)
booking_reservations_df["Reservation number"] = booking_reservations_df["Reservation number"].astype(str)

merged_with_booking_df = merge_with_selected_columns(merged_df, booking_reservations_df, "Third Party Confirmation Number", "Third Party Confirmation Number", "Reservation number", ["Commission amount"])
merged_with_booking_df.rename(columns={"Commission amount" : "booking_marketing"}, inplace=True, errors='ignore')
import_to_excel(merged_with_booking_df, "OTA with debit", "C:/projects/monthly_income/short_term/ota_marketing/")