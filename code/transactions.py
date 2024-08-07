from helpers import combine_excel_files, filter_by_month, filter_by_status, group_and_sum
from variables import DATE_FOR_REPORT, RESERVATION_STATUS, CB_TRANSACTION_FILES

report_name = f"{DATE_FOR_REPORT['year']}{DATE_FOR_REPORT['month']} - Transaction summary"

def create_transactions():
    combined_cb_transactions = combine_excel_files(CB_TRANSACTION_FILES)
    filtered_by_month = filter_by_month(DATE_FOR_REPORT['month'], "Check-In", "Check-Out", combined_cb_transactions)
    current_transactions = filter_by_status(filtered_by_month, [RESERVATION_STATUS["checked_out"], RESERVATION_STATUS["in_house"], RESERVATION_STATUS["confirmed"]])

    sum_debit = group_and_sum(current_transactions, "Res #", "Debit")

    return sum_debit

cb_sum_debit = create_transactions()