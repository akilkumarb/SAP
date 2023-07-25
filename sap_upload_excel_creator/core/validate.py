import pandas as pd

from .mappers import load_column_validation_mapping



def check_mandatory_columns_available(dfs):
    column_validation_mapper = load_column_validation_mapping()
    print("Validating if all mandatory columns exist in sheets...")
    # VALIDATION OF COLUMNS IF EXISTS OR NOT
    not_found_columns_data = dict()
    for file_id, file_data in dfs.items():
        if isinstance(file_data, pd.DataFrame):  # to avoid None when file is not present
            mandatory_columns = column_validation_mapper[file_id]
            not_found_mandatory_columns = list(set(mandatory_columns) - set(file_data.columns))
            if not_found_mandatory_columns:
                not_found_columns_data[file_id] = not_found_mandatory_columns

    if not_found_columns_data:
        # raise Exception(f"The following mandatory fields are not found: {not_found_columns_data}")
        return False, "Mandatory fields are not found in excel input sheets", not_found_columns_data
    else:
        return True, "Mandatory columns are available in excel input sheets", not_found_columns_data


