from utils import extract_columns
from settings.constants import COLUMNS_TO_RENAME, COLUMNS_TO_KEEP, IDS
from settings.env import SOURCE_FILE_PATH

vrbo_columns_to_merge = extract_columns(IDS["third_party"], COLUMNS_TO_KEEP["vrbo_invoice"], COLUMNS_TO_RENAME["vrbo_invoice"], SOURCE_FILE_PATH["vrbo_invoice"])