DATE_FOR_REPORT = {
    "year": 2024,
    "month": 7
}

CB_COLUMNS_TO_DROP = ["Email", "Phone Number", "Mobile", "Gender", "Date of Birth", "Type of Document", "Document Number", "Document Issue Date", "Document Issuing Country", "Document Expiration Date", "Street Address", "Apt, suite, floor etc.", "City", "State", "Postal / ZIP Code", "Adults", "Children", "Products", "Credit Card Type", "Country", "Guest Status", "Cancelation Date", "Estimated Arrival Time", "Origin", "Canceled By", "Company Name", "Company Tax ID Number", "Guest Tax ID Number", "Deposit", "Room Type", "Balance Due", "Reservation Date", "Cancelation fee", "Lodging Tax", "Good and Services Tax", "Quebec Sales Tax", "Status"]

TEMP_AIRBNB_COLUMNS_TO_DROP = ["Date", "Arriving by date", "Type", "Booking date", "Details", "Reference code", "Currency", "Paid out", "Fast Pay fee", "Cleaning fee", "Occupancy taxes", "Earnings year"]

RENAME_AIRBNB_COLUMNS = {
    "Confirmation Code": "Third Party Confirmation Number",
    "End date": "Check out Date",
    "Start date": "Check in Date",
    "Nights": "Nights",
    "Guest": "Name",
    "Listing": "Room Number",
    "Amount": "Accommodation Total",
    "Service fee": "Airbnb marketing",
    "Gross earnings": "Grand Total",
}