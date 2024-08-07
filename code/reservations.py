from helpers import combine_excel_files, filter_by_month, filter_by_status, split_room_numbers
from variables import DATE_FOR_REPORT, RESERVATION_STATUS, CB_COLUMNS_TO_DROP, CB_RESERVATION_FILES

def create_reservations(statuses):
    combined_cb_reservations = combine_excel_files(CB_RESERVATION_FILES, CB_COLUMNS_TO_DROP)

    filtered_by_month = filter_by_month(DATE_FOR_REPORT['month'], "Check in Date", "Check out Date", combined_cb_reservations)

    # Filter by reservation status
    reservations = filter_by_status(filtered_by_month, statuses)

    # Split and copy rows with multiple room numbers
    split_reservations = split_room_numbers(reservations)

    return split_reservations

current_reservations = create_reservations([RESERVATION_STATUS["checked_out"], RESERVATION_STATUS["in_house"], RESERVATION_STATUS["confirmed"]])
no_show_reservations = create_reservations([RESERVATION_STATUS["no_show"]])
canceled_reservations = create_reservations([RESERVATION_STATUS["cancelled"]])
