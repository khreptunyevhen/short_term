from helpers import combine_excel_files, import_to_excel

booking_reservations = { 
    "past": "C:/projects/monthly_income/short_term/sources/reservations/booking/booking_current.xlsx",
    # "current": "C:/projects/monthly_income/short_term/sources/reservations/cloudbeds/werfy_luxury_apart_hotel_cloudbeds_reservations.xlsx"
}

reservations_df = combine_excel_files(booking_reservations)

import_to_excel(reservations_df, "booking", "C:/projects/monthly_income/short_term/ota_marketing")