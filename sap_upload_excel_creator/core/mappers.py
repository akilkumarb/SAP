import json
from ..paths import MAPPINGS_DIR


def load_column_validation_mapping():
    # getting column validation mapper from json file
    with open(MAPPINGS_DIR / "column_validation_mapper.json", 'r') as f:
        column_validation_mapper = json.load(f)
    return column_validation_mapper


def load_relevant_sheet_names_mapping():
    with open(MAPPINGS_DIR / "sheet_names.json", 'r') as f:
        relevant_sheet_names = json.load(f)
        return relevant_sheet_names


def load_spl_code_mapping():
    with open(MAPPINGS_DIR / 'region_to_spl_codes.json', "r") as f:
        spl_code_mapping = json.load(f)
        return spl_code_mapping


def load_bp_codes_n_names_mapping():
    with open(MAPPINGS_DIR / 'bp_codes_n_names.json', "r") as f:
        bp_codes_n_names = json.load(f)
        return bp_codes_n_names


def load_acquirer_n_device_model_to_item_no_n_item_desciption_mapping():
    with open(MAPPINGS_DIR / 'acquirer_n_device_model_to_item_no_n_item_desciption.json', "r") as f:
        acquirer_n_device_model_to_item_no_n_item_desciption = json.load(f)
        return acquirer_n_device_model_to_item_no_n_item_desciption


def load_columnwise_mapping():
    with open(MAPPINGS_DIR / "columnwise_mapping.json", 'r') as f:
        columnwise_mapping:dict = json.load(f)
        return columnwise_mapping


def load_statenames_n_short_codes_mapping():
    with open(MAPPINGS_DIR/ "statenames_n_short_codes.json", "r") as f:
        statenames_n_short_codes = json.load(f)
        return statenames_n_short_codes


def load_deactivation_date_column_mapping():
    with open(MAPPINGS_DIR/ "deactivation_date_column_mapping.json", "r") as f:
        deactivation_date_column_mapping = json.load(f)
        return deactivation_date_column_mapping


def load_status_column_mapping():
    with open(MAPPINGS_DIR/ "status_columns.json", "r") as f:
        status_column_mapping = json.load(f)
        return status_column_mapping
