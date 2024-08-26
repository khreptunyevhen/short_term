import pandas as pd
from helpers import filter_by_status, split_room_numbers

CB_RESERVATIONS = [f"C:/projects/monthly_income/short_term/sources/reservations/cloudbeds/montreal_vacation_rentals_reservations.xlsx", "C:/projects/monthly_income/short_term/sources/reservations/cloudbeds/werfy_luxury_apart_hotel_cloudbeds_reservations.xlsx"
]

CB_COLUMNS_TO_DROP = ["Email", "Phone Number", "Mobile", "Gender", "Date of Birth", "Type of Document", "Document Number", "Document Issue Date", "Document Issuing Country", "Document Expiration Date", "Street Address", "Apt, suite, floor etc.", "City", "State", "Postal / ZIP Code", "Adults", "Children", "Products", "Credit Card Type", "Country", "Guest Status", "Cancelation Date", "Estimated Arrival Time", "Origin", "Canceled By", "Company Name", "Company Tax ID Number", "Guest Tax ID Number", "Deposit", "Room Type", "Balance Due", "Reservation Date", "Cancelation fee", "Lodging Tax", "Good and Services Tax", "Quebec Sales Tax", "random"]

def combine_excel_files(files):
    """Combine multiple files into one by adding at the bottom"""

    data_frames = []

    for file in files:
        
        if file.endswith(".xlsx"):
            df = pd.read_excel(file)
        elif file.endswith(".csv"):
            df = pd.read_csv(file)
        else:
            raise ValueError(f"Unsupported file format for file: {file}")

        df.columns = df.columns.str.strip()
        data_frames.append(df)
    
    combined_df = pd.concat(data_frames, ignore_index=True)

    return combined_df

files = combine_excel_files(CB_RESERVATIONS)

files = files.drop(columns=CB_COLUMNS_TO_DROP, errors="ignore")

files["Check in Date"] = pd.to_datetime(files["Check in Date"], format='%d/%m/%Y')
files["Check out Date"] = pd.to_datetime(files["Check out Date"], format='%d/%m/%Y')

def filter_by_month(month, data):
    """Filter data by a specific month"""

    filtered_data = data[(data['Check out Date'].dt.month >= month) & (data['Check in Date'].dt.month <= month)]

    return filtered_data

filtered_files = filter_by_month(7, files)

filtered_status = filter_by_status(filtered_files, ["Checked Out", "In-House", "Confirmed"])

splitted = split_room_numbers(filtered_status)

def import_to_excel(data_frame, name, output_path):
    """Create an Excel file"""

    data_frame.to_excel(f"{output_path}/{name}.xlsx", engine='openpyxl', index=False)

import_to_excel(splitted, "combined cloudbeds", "C:/projects/monthly_income/short_term/ota_marketing")