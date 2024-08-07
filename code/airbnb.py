import pandas as pd

df = pd.read_csv("C:/projects/monthly_income/short_term/sources/reservations/airbnb/airbnb.csv")

df_filtered = df[df["Type"] != "Payout"]

print(df_filtered.head())

