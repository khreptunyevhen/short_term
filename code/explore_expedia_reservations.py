from utils import extract_columns
from settings.constants import COLUMNS_TO_RENAME, COLUMNS_TO_KEEP, IDS
from settings.env import SOURCE_FILE_PATH

expedia_columns_to_merge = extract_columns(IDS["third_party"], COLUMNS_TO_KEEP["expedia_invoice"], COLUMNS_TO_RENAME["expedia_invoice"], SOURCE_FILE_PATH["expedia_invoice"])