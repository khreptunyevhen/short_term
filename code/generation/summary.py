import pandas as pd
from settings.params import COMMISSION, ADDITIONAL_EXPENSES, PROPERTIES

try:
    source = pd.read_excel("C:/tasks/1. unit reports/2024/07/202407 - Reservations with OTA marketing for analysis.xlsx")
except:
    raise ValueError("The specified Excel file was not found.")

def get_reservations_by_building(data: pd.DataFrame) -> tuple:
    """
    Splits the given DataFrame into two based on the building type.

    Parameters:
    - data (pd.DataFrame): The DataFrame containing reservation data.

    Returns:
    - tuple: A tuple containing two DataFrames, one for 'Luxury Apart-Hotel' and another for other buildings.
    """

    hotel_reservations = data[data["Building"] == "Luxury Apart-Hotel"]
    other_reservations = data[data["Building"] != "Luxury Apart-Hotel"]

    return (hotel_reservations, other_reservations)

hotel_reservations, other_reservations = list(get_reservations_by_building(source))

def get_summary(data: pd.DataFrame) -> dict:
    """
    Generate a summary of monthly financial metrics from reservation data.

    This function calculates various financial metrics for a given set of reservation data.
    It computes the total revenue, OTA (Online Travel Agency) charges, commission fees, cleaning costs, and additional 
    expenses related to salaries and hotel expenses. The calculations are based on both the reservation data and predefined
    constants for commission rates and additional expenses.

    Parameters:
    - data (pd.DataFrame): A pandas DataFrame containing reservation data. The DataFrame is expected to include columns such as 
      "Accommodation Total", "Total marketing (no Airbnb)", and "Cleaning".

    Returns:
    - dict: A dictionary containing the following keys and their corresponding calculated values:
        - "total_revenue": Total revenue from accommodations.
        - "ota_charges": Total OTA charges, including additional expenses.
        - "commission": Commission calculated as a percentage of total revenue.
        - "cleaning": Total cleaning costs, adjusted for commission.
        - "salaries": Additional salary expenses from predefined constants.
        - "hotel_expenses": A nested dictionary containing:
            - "recurrent": Recurrent hotel expenses from predefined constants.
            - "one_time": One-time hotel expenses from predefined constants.
    """

    MONTHLY_SUMMARY = {
        "total_revenue": 0,
        "ota_charges": 0,
        "commission": 0,
        "cleaning": 0,
        "salaries": ADDITIONAL_EXPENSES.get("salaries", 0),
        "nights": 0,
        "hotel_expenses": {
            "recurrent": ADDITIONAL_EXPENSES["hotel_expenses"].get("recurrent", 0),
            "one_time": ADDITIONAL_EXPENSES["hotel_expenses"].get("one_time", 0)
        }
    }

    if "Accommodation Total" in data.columns:
        MONTHLY_SUMMARY["total_revenue"] = round(float(data["Accommodation Total"].sum(skipna=True)), 2)
    else:
        raise ValueError("Accommodation Total column missing in data")
    
    if "Total marketing (no Airbnb)" in data.columns:
        MONTHLY_SUMMARY["ota_charges"] = round(float(data["Total marketing (no Airbnb)"].sum(skipna=True)) + ADDITIONAL_EXPENSES["ota_charges"], 2)
    else:
        raise ValueError("Total marketing (no Airbnb) column missing in data")
    
    if "Cleaning" in data.columns:
        MONTHLY_SUMMARY["cleaning"] = round(float(data["Cleaning"].sum(skipna=True)) * (1 + COMMISSION["hotel"]), 2)
    else:
        raise ValueError("Cleaning column missing in data")
    
    if "Nights" in data.columns:
        MONTHLY_SUMMARY["nights"] = float(data["Nights"].sum(skipna=True))
    else:
        raise ValueError("Cleaning column missing in data")

    MONTHLY_SUMMARY["commission"] = round(MONTHLY_SUMMARY["total_revenue"] * COMMISSION["hotel"], 2)

    return MONTHLY_SUMMARY

hotel_summary = get_summary(hotel_reservations)

def calculate_portion(row, amount, properties_info):
    unit_type = row["Unit"][-2:]
    total_area = 0

    for property in properties_info:
        total_area += property["area"] * len(property["units"])

    unit_by_type = next((p for p in properties_info if p["type"] == unit_type), None)

    if unit_by_type is None:
        return 0

    units_by_type = len(unit_by_type["units"])
    area_by_type = round(units_by_type * unit_by_type["area"], 4)

    portion = round(amount * (area_by_type / total_area) / units_by_type, 2)

    return portion

def create_summary_table(units, summary, properties_info):
    table = pd.DataFrame(units, columns=["Unit number"])

    table["Unit"] = "Unit " + table["Unit number"]
    table["Accommodation Total"] = table.apply(lambda row: calculate_portion(row, summary["total_revenue"], properties_info), axis=1)
    table["Sum Marketing"] = table.apply(lambda row: calculate_portion(row, summary["ota_charges"], properties_info), axis=1)
    table["Cleaning Fee"] = table.apply(lambda row: calculate_portion(row, summary["cleaning"], properties_info), axis=1)
    table["Salaries attributions"] = table.apply(lambda row: calculate_portion(row, summary["salaries"], properties_info), axis=1)
    table["WERFY commission"] = table["Accommodation Total"] * COMMISSION["hotel"]
    table["Per Unit Bill Attribution"] = 0
    table["Total Nights"] = 0
    table["Parking"] = 0
    table["Amount Remitted"] = table["Accommodation Total"] + table["Parking"] - table["Sum Marketing"] - ((table["Salaries attributions"] + table["Cleaning Fee"] + table["Per Unit Bill Attribution"]) * (1 + 0.05 + 0.09975) + table["WERFY commission"] * (1 + 0.05 + 0.09975))

    return table

summary_table = create_summary_table(hotel_reservations["Room Number"].unique(), hotel_summary, PROPERTIES["hotel"])

print(summary_table)



