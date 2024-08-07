from reservations import current_reservations, no_show_reservations, canceled_reservations
from transactions import cb_sum_debit
from explore_data import create_ota_marketing_report
from helpers import import_to_excel

def main():
    import_to_excel(current_reservations, "Current reservations", "C:/projects/monthly_income/short_term/ota_marketing")
    import_to_excel(no_show_reservations, "No snow reservations", "C:/projects/monthly_income/short_term/ota_marketing")
    import_to_excel(canceled_reservations, "Canceled reservations", "C:/projects/monthly_income/short_term/ota_marketing")
    import_to_excel(cb_sum_debit, "Transactions", "C:/projects/monthly_income/short_term/ota_marketing")

    import_to_excel(create_ota_marketing_report(current_reservations, cb_sum_debit), "OTA with debit", "C:/projects/monthly_income/short_term/ota_marketing")

if __name__ == "__main__":
    main()