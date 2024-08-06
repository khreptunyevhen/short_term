# import functions
from helpers import get_combine_excel_file, get_month_data, filter_by_status, import_file, split_rows

# import variables
from variables import DATE_FOR_REPORT, RESERVATION_STATUS, cb_reservations_columns_to_drop, links_cb_reservations

report_name = f"{DATE_FOR_REPORT['year']}{DATE_FOR_REPORT['month']} - Reservations with OTA marketing"
cb_reservations_output_path = "C:/projects/monthly_income/short_term/ota_marketing"

combined_cb_reservations = get_combine_excel_file(links_cb_reservations, cb_reservations_columns_to_drop)

filtered_by_month = get_month_data(DATE_FOR_REPORT['month'], "Check in Date", "Check out Date", combined_cb_reservations)

no_show_reservations = filter_by_status([RESERVATION_STATUS["no_show"]], filtered_by_month)
current_reservations = filter_by_status([RESERVATION_STATUS["checked_out"], RESERVATION_STATUS["in_house"], RESERVATION_STATUS["confirmed"]], filtered_by_month)
canceled_reservations = filter_by_status([RESERVATION_STATUS["cancelled"]], filtered_by_month)

# Split and copy rows with multiple room numbers
split_reservations = split_rows(current_reservations)

import_file(split_reservations, report_name, cb_reservations_output_path)
import_file(canceled_reservations, "cancelled", cb_reservations_output_path)
