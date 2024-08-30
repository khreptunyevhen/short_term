DATE_FOR_REPORT = {
    "year": 2024,
    "month": 7
}

COLUMNS_TO_DROP = {
    "cloudbeds_reservations": ["Email", "Phone Number", "Mobile", "Gender", "Date of Birth", "Type of Document", "Document Number", "Document Issue Date", "Document Issuing Country", "Document Expiration Date", "Street Address", "Apt, suite, floor etc.", "City", "State", "Postal / ZIP Code", "Adults", "Children", "Products", "Credit Card Type", "Country", "Guest Status", "Cancelation Date", "Estimated Arrival Time", "Origin", "Canceled By", "Company Name", "Company Tax ID Number", "Guest Tax ID Number", "Deposit", "Room Type", "Balance Due", "Reservation Date", "Cancelation fee", "Lodging Tax", "Good and Services Tax", "Quebec Sales Tax", "Status"],
    "temp_account_airbnb": ["Date", "Arriving by date", "Type", "Booking date", "Details", "Reference code", "Currency", "Paid out", "Fast Pay fee", "Cleaning fee", "Occupancy taxes", "Earnings year"]
}

COLUMNS_TO_RENAME = {
    "expedia_invoice": {
        "Reservation ID": "Third Party Confirmation Number",
        "Total Amount Due": "Expedia marketing"
    },
    "booking_invoice": {
        "Reservation number": "Third Party Confirmation Number",
        "Commission amount": "Booking marketing"
    },
    "airbnb_invoice": {
        "Service fee": "Airbnb marketing",
        "Confirmation Code": "Third Party Confirmation Number"
    },
    "temp_account_airbnb_invoice": {
        "Confirmation Code": "Third Party Confirmation Number",
        "End date": "Check out Date",
        "Start date": "Check in Date",
        "Nights": "Nights",
        "Guest": "Name",
        "Listing": "Room Number",
        "Amount": "Accommodation Total",
        "Service fee": "Airbnb marketing",
        "Gross earnings": "Grand Total",
    },
    "vrbo_invoice": {
        "Commission": "VRBO marketing",
        "Reservation External ID (Folio #)": "Third Party Confirmation Number"
    }
}

COLUMNS_TO_KEEP = {
    "expedia_invoice": ["Third Party Confirmation Number", "Expedia marketing"],
    "booking_invoice": ["Third Party Confirmation Number", "Booking marketing"],
    "airbnb_invoice": ["Third Party Confirmation Number", "Airbnb marketing", "Notes"],
    "vrbo_invoice": ["Third Party Confirmation Number", "VRBO marketing"],
}

IDS = {
    "cloudbeds": "Reservation Number",
    "third_party": "Third Party Confirmation Number"
}

TAXES = {
    "lodging_tax": 0.035,
    "gst": 0.05,
    "qst": 0.09975
}

COLUMN_ORDER = ["Accommodation Total", "Amount Paid", "Balance Due", "Lodging Tax", "GST", "QST", "Grand Total", "Check in Date", "Check out Date", "Nights", "Reservation Number", "Third Party Confirmation Number", "Name", "Room Number", "Building", "Source", "Cleaning", "Booking marketing", "Expedia marketing", "Airbnb marketing", "VRBO marketing", "Total marketing (no Airbnb)", "Cross", "Notes"]