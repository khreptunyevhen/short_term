DATE_FOR_REPORT = {
    "year": 2024,
    "month": 6
}

month = DATE_FOR_REPORT['month']

if DATE_FOR_REPORT['month'] < 10:
    month = f"0{DATE_FOR_REPORT['month']}"

RESERVATION_STATUS = {
    "cancelled": "Cancelled",
    "checked_out": "Checked Out",
    "no_show": "No Show",
    "in_house": "In-House",
    "confirmed": "Confirmed"
}

SOURCE_FOLDER = "C:/projects/monthly_income/short_term/sources/"
FINAL_FOLDER_LINK = "C:/projects/monthly_income/short_term/ota_marketing"

SOURCE_FILES_NAME = {}
FINAL_FILES_NAME = {
    "canceled_reservations": f"{DATE_FOR_REPORT['year']}{month} - canceled reservations",
    "no_show_reservations": f"{DATE_FOR_REPORT['year']}{month} - no-show reservations",
    "cb_debit_summary": f"{DATE_FOR_REPORT['year']}{month} - debit summary",
    "current_reservations": f"{DATE_FOR_REPORT['year']}{month} - current reservations",
    "combined_for_analysis": f"{DATE_FOR_REPORT['year']}{month} - Reservations with OTA marketing"
}

CB_COLUMNS_TO_DROP = ["Email", "Phone Number", "Mobile", "Gender", "Date of Birth", "Type of Document", "Document Number", "Document Issue Date", "Document Issuing Country", "Document Expiration Date", "Street Address", "Apt, suite, floor etc.", "City", "State", "Postal / ZIP Code", "Adults", "Children", "Products", "Credit Card Type", "Country", "Guest Status", "Cancelation Date", "Estimated Arrival Time", "Origin", "Canceled By", "Company Name", "Company Tax ID Number", "Guest Tax ID Number", "Deposit", "Room Type", "Balance Due", "Reservation Date"]

CB_RESERVATION_FILES = { 
    "hotel": f"{SOURCE_FOLDER}reservations/cloudbeds/montreal_vacation_rentals_reservations.xlsx",
    "other": f"{SOURCE_FOLDER}reservations/cloudbeds/werfy_luxury_apart_hotel_cloudbeds_reservations.xlsx"
}

CB_TRANSACTION_FILES = { 
    "hotel": f"{SOURCE_FOLDER}transactions/cloudbeds/montreal_vacation_rentals_transactions.xlsx",
    "other": f"{SOURCE_FOLDER}transactions/cloudbeds/werfy_luxury_apart_hotel_cloudbeds_transactions.xlsx"
}

EXTERNAL_SOURCE_FILES = {
    "expedia": f"{SOURCE_FOLDER}transactions/expedia/expedia_commissions.xlsx",
    "booking": f"{SOURCE_FOLDER}reservations/booking/booking_current.xlsx",
    "airbnb": f"{SOURCE_FOLDER}reservations/airbnb/airbnb.csv",
}

TAXES = {
    "lodging_tax": 0.035,
    "gst": 0.05,
    "qst": 0.0975
}

COLUMN_ORDER = ["Accommodation Total", "Amount Paid", "balance_due", "lodging_tax", "gst", "qst", "Grand Total", "Debit", "Check in Date", "Check out Date", "Nights", "Reservation_id", "Third Party Confirmation Number", "Name", "Room Number", "building", "Source", "Cleaning_+20%", "booking_marketing", "expedia_marketing", "airbnb_marketing", "airbnb_paid", "airbnb_total", "cross", "notes"]

TEMPORARY_AIRBNB_ACCOUNT_COLUMNS_TO_DROP = ["Arriving by date", "Earnings year", "Booking date", "Reference code", "Currency", "Paid out", "Fast Pay fee", "Cleaning fee", "Date", "Occupancy taxes", "Type"]