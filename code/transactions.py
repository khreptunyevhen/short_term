# import functions
from helpers import get_combine_excel_file, import_file, get_month_data, filter_by_status, group_and_sum

# import variables
from variables import DATE_FOR_REPORT, RESERVATION_STATUS, links_cb_transactions

report_name = f"{DATE_FOR_REPORT['year']}{DATE_FOR_REPORT['month']} - Transaction summary"
cb_reservations_output_path = "C:/projects/monthly_income/short_term/ota_marketing"

combined_cb_transactions = get_combine_excel_file(links_cb_transactions)

filtered_by_month = get_month_data(DATE_FOR_REPORT['month'], "Check-In", "Check-Out", combined_cb_transactions)

current_transactions = filter_by_status([RESERVATION_STATUS["checked_out"], RESERVATION_STATUS["in_house"], RESERVATION_STATUS["confirmed"]], filtered_by_month)

sum_debit = group_and_sum(current_transactions, "Res #", "Debit")

import_file(sum_debit, report_name, cb_reservations_output_path)