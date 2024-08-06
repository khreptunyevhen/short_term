from helpers import combine_excel_files, import_to_excel
from variables import BOOKING_RESERVATION_FILES

booking_df = combine_excel_files(BOOKING_RESERVATION_FILES)

import_to_excel(booking_df, "booking", "C:/projects/monthly_income/short_term/ota_marketing")