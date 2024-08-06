from helpers import get_combine_excel_file, import_file, merge_left

booking_reservations = { 
    "past": "C:/projects/monthly_income/short_term/sources/reservations/booking/booking_current.xlsx",
    # "current": "C:/projects/monthly_income/short_term/sources/reservations/cloudbeds/werfy_luxury_apart_hotel_cloudbeds_reservations.xlsx"
}

reservations_df = get_combine_excel_file(booking_reservations)

import_file(reservations_df, "booking", "C:/projects/monthly_income/short_term/ota_marketing")