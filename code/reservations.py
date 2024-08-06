from helpers import combine_excel_files, filter_by_month, filter_by_status, import_to_excel, split_room_numbers
from variables import DATE_FOR_REPORT, RESERVATION_STATUS, CB_COLUMNS_TO_DROP, CB_RESERVATION_FILES

report_name = f"{DATE_FOR_REPORT['year']}{DATE_FOR_REPORT['month']} - Reservations with OTA marketing"
cb_reservations_output_path = "C:/projects/monthly_income/short_term/ota_marketing"

combined_cb_reservations = combine_excel_files(CB_RESERVATION_FILES, CB_COLUMNS_TO_DROP)

filtered_by_month = filter_by_month(DATE_FOR_REPORT['month'], "Check in Date", "Check out Date", combined_cb_reservations)

# Filter by reservation status
no_show_reservations = filter_by_status(filtered_by_month, [RESERVATION_STATUS["no_show"]])
current_reservations = filter_by_status(filtered_by_month, [RESERVATION_STATUS["checked_out"], RESERVATION_STATUS["in_house"], RESERVATION_STATUS["confirmed"]])
canceled_reservations = filter_by_status(filtered_by_month, [RESERVATION_STATUS["cancelled"]])

# Split and copy rows with multiple room numbers
split_reservations = split_room_numbers(current_reservations)

import_to_excel(split_reservations, report_name, cb_reservations_output_path)
import_to_excel(canceled_reservations, "cancelled", cb_reservations_output_path)
