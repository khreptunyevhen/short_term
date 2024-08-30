from utils import extract_columns
from settings.constants import COLUMNS_TO_RENAME, COLUMNS_TO_KEEP, IDS
from settings.env import SOURCE_FILE_PATH

booking_columns_to_merge = extract_columns(IDS["third_party"], COLUMNS_TO_KEEP["booking_invoice"], COLUMNS_TO_RENAME["booking_invoice"], SOURCE_FILE_PATH["booking_invoice"])