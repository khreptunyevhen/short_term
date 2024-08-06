# import functions
from helpers import combine_excel_files, import_to_excel, filter_by_month, filter_by_status, group_and_sum

# import variables
from variables import DATE_FOR_REPORT, RESERVATION_STATUS, links_cb_transactions

report_name = f"{DATE_FOR_REPORT['year']}{DATE_FOR_REPORT['month']} - Transaction summary"
cb_reservations_output_path = "C:/projects/monthly_income/short_term/ota_marketing"

combined_cb_transactions = combine_excel_files(links_cb_transactions)

filtered_by_month = filter_by_month(DATE_FOR_REPORT['month'], "Check-In", "Check-Out", combined_cb_transactions)

current_transactions = filter_by_status(filtered_by_month, [RESERVATION_STATUS["checked_out"], RESERVATION_STATUS["in_house"], RESERVATION_STATUS["confirmed"]])

sum_debit = group_and_sum(current_transactions, "Res #", "Debit")

import_to_excel(sum_debit, report_name, cb_reservations_output_path)