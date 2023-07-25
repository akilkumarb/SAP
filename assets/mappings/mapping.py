import os
import json
import numpy as np
import pandas as pd
import datetime

pd.options.display.max_columns = 1000

# output_columns = [
#     'SC Entry', 'Service Ticket Number', 'Transaction Type',
#     'Reporting Type', 'Priority', 'Acquirer', 'Ticket Type', 'Call Type',
#     'Subject', 'Sub Type', 'BP Code', 'Customer', 'Contact Person',
#     'Merchant Name', 'DBA Name', 'Address', 'City', 'Location', 'Pincode',
#     'State', 'Zone', 'Region', 'Phone No', 'Merchant Phone No', 'User ID',
#     'MID', 'TID', 'Old Device Serial', 'New Serial Number', 'Item Code',
#     'Item Name', 'Item Description', 'Status', 'Closure Remarks',
#     'NSTP Remarks', 'SPL Code', 'No Of Visits', 'SIM Provider', 'SIM No',
#     'SIM No Old', 'POA', 'POA Date'
# ]

# [
#     'SC Entry',
#  'Service Ticket Number',
#  'Transaction Type',
#  'SPL Code',
#  'Reporting Type',
#  'Priority',
#  'Acquirer',
#  'Ticket Type',
#  'Call Type',
#  'Subject',
#  'Sub Type',
#  'BP Code',
#  'Customer',
#  'Contact Person',
#  'Merchant Name',
#  'DBA Name',
#  'Address',
#  'City',
#  'Location',
#  'Pincode',
#  'State',
#  'Zone',
#  'Region',
#  'Phone No',
#  'Merchant Phone No',
#  'User ID',
#  'MID',
#  'TID',
#  'Old Device Serial',
#  'New Serial Number',
#  'Item Code',
#  'Item Name',
#  'Item Description',
#  'Status',
#  'Closure Remarks',
#  'POA',
#  'No Of Visits',
#  'SIM Provider',
#  'SIM No',
#  'SIM No Old',
#  'POA',
#  'POA Date',
#  nan,
#  'Store ID']

columns_mapping_file = "assets/Column Header mapping.xlsx"
sheets = pd.read_excel(columns_mapping_file, sheet_name=None)
df = sheets['Common Fields Mapping']

mapped_section = df[[col for col in df.columns if "Unnamed:" not in col]].set_index("SAP Fornat").copy()
# mapped_section.loc["SC Entry"]['KOTAK'] is np.NAN

def get_mapping(input_sheet:str, mapped_section:pd.DataFrame):
    sheet_specific_map = mapped_section[input_sheet]
    return sheet_specific_map[sheet_specific_map.notnull()].to_dict()

sheetz = ['KOTAK', 'AXIS', 'SBI', 'HDFC', 'ICICI', 'IDFC', 'Complaints Master']
sheetz_n_mappings = {sheet: get_mapping(input_sheet=sheet, mapped_section=mapped_section)  for sheet in sheetz}
with open('./assets/mappings/sheetz_n_mappings.json', 'w') as f:
    json.dump(sheetz_n_mappings, f, indent=4, sort_keys=False)

columnwise_mapping = {col: {sht: sheetz_n_mappings[sht][col] for sht in sheetz if col in sheetz_n_mappings[sht].keys()} for col in output_columns}
with open('./assets/mappings/columnwise_mapping.json', 'w') as f:
    json.dump(columnwise_mapping, f, indent=4, sort_keys=False)



# # validation mapper creation  +++ RECEIVED DATE WHICH IS SET MANUALLY
# all_file_ids = ["KOTAK", "AXIS", "SBI", "HDFC", "HDFC AGGR", "IDFC", "ICICI", "YBL", "COMPLAINTS"]
# column_validation_mapper = dict()
# for file_id in all_file_ids:
#     column_validation_mapper[file_id] = []
#     for k, v in columnwise_mapping.items():
#         if isinstance(v, dict):
#             if file_id in v.keys():
#                 for kk, vv in v.items():
#                     if kk == file_id:
#                         column_validation_mapper[file_id].append(vv)

# with open(MAPPINGS_DIR / "column_validation_mapper.json", 'w') as f:
#     json.dump(column_validation_mapper, f, sort_keys=False, indent=4)

# # getting column validation mapper from json file
# with open(MAPPINGS_DIR / "column_validation_mapper.json", 'r') as f:
#     column_validation_mapper = json.load(f)



def do_basic_mapping(input_row:pd.Series, type_:str, selected_file:str):

    output_columns = columnwise_mapping.keys()
    output_row = pd.Series(dtype="object", index=output_columns)
    for field in output_columns:
        # if type_ in ['installation', 'deinstallation']:
        if isinstance(columnwise_mapping[field], dict):
            if selected_file in columnwise_mapping[field].keys():
                corresponding_col_in_selected_file = columnwise_mapping[field][selected_file]
                output_row[field] = input_row[corresponding_col_in_selected_file]
        elif type(columnwise_mapping[field]) in [str, int]:
            output_row[field] = columnwise_mapping[field]
        elif columnwise_mapping[field] is None:
            output_row[field] = np.NaN
        else:
            raise Exception("value type of columnwise mapping.json is neither dict, int nor str")
        # elif type_ in ['service',]:
        #     raise NotImplementedError("Not implemented breakfix")

    return output_row



