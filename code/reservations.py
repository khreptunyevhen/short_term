# import functions
from helpers import combine_excel_files, filter_by_month, filter_by_status, import_to_excel, split_room_numbers

# import variables
from variables import DATE_FOR_REPORT, RESERVATION_STATUS, cb_reservations_columns_to_drop, links_cb_reservations

report_name = f"{DATE_FOR_REPORT['year']}{DATE_FOR_REPORT['month']} - Reservations with OTA marketing"
cb_reservations_output_path = "C:/projects/monthly_income/short_term/ota_marketing"

combined_cb_reservations = combine_excel_files(links_cb_reservations, cb_reservations_columns_to_drop)

filtered_by_month = filter_by_month(DATE_FOR_REPORT['month'], "Check in Date", "Check out Date", combined_cb_reservations)

no_show_reservations = filter_by_status(filtered_by_month, [RESERVATION_STATUS["no_show"]])
current_reservations = filter_by_status(filtered_by_month, [RESERVATION_STATUS["checked_out"], RESERVATION_STATUS["in_house"], RESERVATION_STATUS["confirmed"]])
canceled_reservations = filter_by_status(filtered_by_month, [RESERVATION_STATUS["cancelled"]])

# Split and copy rows with multiple room numbers
split_reservations = split_room_numbers(current_reservations)

import_to_excel(split_reservations, report_name, cb_reservations_output_path)
import_to_excel(canceled_reservations, "cancelled", cb_reservations_output_path)
