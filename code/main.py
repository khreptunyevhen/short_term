from reservations import current_reservations, no_show_reservations, canceled_reservations
from transactions import cb_sum_debit
from explore_data import process_reservations
from helpers import import_to_excel
from variables import FINAL_FOLDER_LINK, FINAL_FILES_NAME

def main():
    final_reservations = process_reservations(current_reservations, cb_sum_debit)
    
    import_to_excel(current_reservations, FINAL_FILES_NAME["current_reservations"], FINAL_FOLDER_LINK)
    import_to_excel(no_show_reservations, FINAL_FILES_NAME["no_show_reservations"], FINAL_FOLDER_LINK)
    import_to_excel(canceled_reservations, FINAL_FILES_NAME["canceled_reservations"], FINAL_FOLDER_LINK)
    import_to_excel(cb_sum_debit, FINAL_FILES_NAME["cb_debit_summary"], FINAL_FOLDER_LINK)

    import_to_excel(final_reservations, FINAL_FILES_NAME["combined_for_analysis"], FINAL_FOLDER_LINK)

if __name__ == "__main__":
    main()