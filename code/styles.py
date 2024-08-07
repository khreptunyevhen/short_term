import pandas as pd
from helpers import import_to_excel

df = pd.read_excel("C:/projects/monthly_income/short_term/ota_marketing/OTA with debit.xlsx")

def highlight_duplicates(s):
    is_duplicate = s.duplicated(keep=False)
    return ['background-color: lightcoral' if v else '' for v in is_duplicate]

def highlight_na_or_empty(s):
    return ['background-color: lightcoral' if pd.isna(v) or v == '' else '' for v in s]

styled_df = df.style.apply(highlight_duplicates, subset=['Reservation_id'])
styled_df = styled_df.apply(highlight_na_or_empty, subset=['Room Number'])

import_to_excel(styled_df, "styled", "C:/projects/monthly_income/short_term/ota_marketing/")