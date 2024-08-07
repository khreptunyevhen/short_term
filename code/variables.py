DATE_FOR_REPORT = {
    "year": 2024,
    "month": 6
}

RESERVATION_STATUS = {
    "cancelled": "Cancelled",
    "checked_out": "Checked Out",
    "no_show": "No Show",
    "in_house": "In-House",
    "confirmed": "Confirmed"
}

CB_COLUMNS_TO_DROP = ["Email", "Phone Number", "Mobile", "Gender", "Date of Birth", "Type of Document", "Document Number", "Document Issue Date", "Document Issuing Country", "Document Expiration Date", "Street Address", "Apt, suite, floor etc.", "City", "State", "Postal / ZIP Code", "Adults", "Children", "Products", "Credit Card Type", "Country", "Guest Status", "Cancelation Date", "Estimated Arrival Time", "Origin", "Canceled By", "Company Name", "Company Tax ID Number", "Guest Tax ID Number", "Deposit", "Room Type", "Balance Due", "Reservation Date"]

CB_RESERVATION_FILES = { 
    "hotel": "C:/projects/monthly_income/short_term/sources/reservations/cloudbeds/montreal_vacation_rentals_reservations.xlsx",
    "other": "C:/projects/monthly_income/short_term/sources/reservations/cloudbeds/werfy_luxury_apart_hotel_cloudbeds_reservations.xlsx"
}

BOOKING_RESERVATION_FILES = { 
    "past": "C:/projects/monthly_income/short_term/sources/reservations/booking/booking_current.xlsx",
}

CB_TRANSACTION_FILES = { 
    "hotel": "C:/projects/monthly_income/short_term/sources/transactions/cloudbeds/montreal_vacation_rentals_transactions.xlsx",
    "other": "C:/projects/monthly_income/short_term/sources/transactions/cloudbeds/werfy_luxury_apart_hotel_cloudbeds_transactions.xlsx"
}

EXPEDIA_TRANSACTION_FILES = { 
    "expedia": "C:/projects/monthly_income/short_term/sources/transactions/expedia/expedia_commissions.xlsx",
}