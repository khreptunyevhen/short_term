from explore_data import create_final_reservations
from utils import import_to_excel
from settings.env import BASE_OUTPUT_PATH
from settings.constants import DATE_FOR_REPORT

def main(month):

    if month < 10:
        month = f"0{month}"

    reservations = create_final_reservations()
    import_to_excel(reservations, f"{DATE_FOR_REPORT["year"]}{month} - Reservations with OTA marketing for analysis", BASE_OUTPUT_PATH, DATE_FOR_REPORT["year"], month)

if __name__ == "__main__":
    main(DATE_FOR_REPORT["month"])