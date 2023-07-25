# import os
# import pickle
# import numpy as np
# import pandas as pd
# import datetime
# from pathlib import Path
# import json

# pd.options.display.max_columns = 1000


# # data filtering
# date_for_data_filter = datetime.date(2023, 1, 21)
# # uploaded_acquirer = "KOTAK" 
# # selected_type = "installation"


# xl_dir = Path("assets/excel_files/original")

# files = {
#     "KOTAK": "kotak_master12.xlsb",
#     # "AXIS": "Axis Master Installation.xlsb",
#     # "SBI": "sbi_master (6).xlsx",
#     # "HDFC": "hdfc_master.xlsx",
#     # "HDFC AGGR": None,
#     # "IDFC": "IDFC Open Call - 23.01.2023_EDITED_BY_ASIF.xlsx",
#     # "ICICI": "ICICI Open Call 23.01.2023_EDITED_BY_ASIF.xlsx",
#     # "YBL": "YBL Master File.xlsx",
#     "COMPLAINTS": "Master Compliants (12).xlsx"
# }

# # READ SHEET NAMES DATA MAPPER
# from sap_upload_excel_creator.paths import MAPPINGS_DIR

# print("Loading Mapping Jsons...")

# with open(MAPPINGS_DIR / "sheet_names.json", 'r') as f:
#     relevant_sheet_names = json.load(f)

# with open(MAPPINGS_DIR / 'region_to_spl_codes.json', "r") as f:
#     spl_code_mapping = json.load(f)

# with open(MAPPINGS_DIR / 'bp_codes_n_names.json', "r") as f:
#     bp_codes_n_names = json.load(f)

# with open(MAPPINGS_DIR / 'acquirer_n_device_model_to_item_no_n_item_desciption.json', "r") as f:
#     acquirer_n_device_model_to_item_no_n_item_desciption = json.load(f)

# with open(MAPPINGS_DIR / "columnwise_mapping.json", 'r') as f:
#     columnwise_mapping:dict = json.load(f)

# # getting column validation mapper from json file
# with open(MAPPINGS_DIR / "column_validation_mapper.json", 'r') as f:
#     column_validation_mapper = json.load(f)

# with open(MAPPINGS_DIR/ "statenames_n_short_codes.json", "r") as f:
#     statenames_n_short_codes = json.load(f)



# # excluding if dataframe is not avalable (value is None)
# selected_files = {key: value for key, value in files.items() if value is not None}

# print("Loading the excel files to memory for further processing. This might take many minutes...")

# # # loading all dataframes
# # dfs = dict()
# # for file_id, filename in selected_files.items():
# #     print(f"{'Reading file:':<20} {file_id:>20}")
# #     dfs[file_id] = pd.read_excel(xl_dir / filename, sheet_name=relevant_sheet_names[file_id])
# #     print(f"Done".rjust(40, " "))
# #     print(40*"-")

# # -------TEMP ----------- for above loading of files -------
# # import pickle
# # with open(".temp/dfs.pkl", "wb") as f:
# #     pickle.dump(dfs, f)

# with open(".temp/dfs.pkl", "rb") as f:
#     dfs = pickle.load(f)



# # MAPPING FUNCTIONS =======================================
# print("Loading Mapping functions...")


# def do_basic_mapping(input_row:pd.Series, type_:str, selected_file:str):

#     output_columns = columnwise_mapping.keys()
#     output_row = pd.Series(dtype="object", index=output_columns)
#     for field in output_columns:
#         # if type_ in ['installation', 'deinstallation']:
#         if isinstance(columnwise_mapping[field], dict):
#             if selected_file in columnwise_mapping[field].keys():
#                 corresponding_col_in_selected_file = columnwise_mapping[field][selected_file]
#                 output_row[field] = input_row[corresponding_col_in_selected_file]
#         elif type(columnwise_mapping[field]) in [str, int]:
#             output_row[field] = columnwise_mapping[field]
#         elif columnwise_mapping[field] is None:
#             output_row[field] = np.NaN
#         else:
#             raise Exception("value type of columnwise mapping.json is neither dict, int nor str")
#         # elif type_ in ['service',]:
#         #     raise NotImplementedError("Not implemented breakfix")

#     return output_row

# def do_mapping_from_zone_to_spl_code(zone):  # changed from region to zone on Jan 23, 2023
#     global spl_code_mapping
#     if zone is np.NaN:
#         return np.NaN
#     elif zone.upper() in spl_code_mapping:
#         return str(spl_code_mapping[zone.upper()]['SPL Code'])   # ISSEUE AGAIN MAPPING(DELHI NCR) contains delhi. Can I map spl code for DELHI NCR to DELHI?
#     else:
#         print(f"Error while mapping zone to spl code: <ISSUE>{zone}</ISSUE>")
#         return f"<ISSUE>{zone}</ISSUE>"

# def do_mapping_from_acquirer_to_bp_code(acquirer):
#     global bp_codes_n_names
#     if acquirer in bp_codes_n_names.keys():
#         return bp_codes_n_names[acquirer]["BP Code"]
#     else:
#         print(f"Error while mapping acquirer to bp code: <ISSUE>{acquirer}</ISSUE>")
#         return f"<ISSUE>{acquirer}</ISSUE>"

# def do_mapping_from_acquirer_to_bp_name(acquirer):  # or to customer
#     global bp_codes_n_names
#     if acquirer in bp_codes_n_names.keys():
#         return bp_codes_n_names[acquirer]["BP Name"]
#     else:
#         print(f"Error while mapping acquirer to bp name: <ISSUE>{acquirer}</ISSUE>")
#         return f"<ISSUE>{acquirer}</ISSUE>"


# def do_mapping_for_item_number_n_name_n_description(input_row):
#     # 'Item Code', 'Item Name', 'Item Description'
#     output_row = pd.Series(dtype="object", index=['Item Code', 'Item Name', 'Item Description'])
#     device_name, acquirer = input_row["Device Name__DERIVE"], input_row['Acquirer']

#     # trying to break the code when excpetions other than KeyError occur - BEWARE
#     try:
#         output_row['Item Code'] = acquirer_n_device_model_to_item_no_n_item_desciption[device_name][acquirer]["Item No."]
#     except KeyError as e:
#         print(f"Error: unknown device_name or acquirer {e}")
#         output_row['Item Code'] = f"<ISSUE>{device_name} == {acquirer}</ISSUE>"
#     # except Exception as e:
        
#     output_row['Item Name'] = output_row['Item Code']
#     # import sys; sys.exit()
#     # try:
#     #     # if acquirer_n_device_model_to_item_no_n_item_desciption[device_name][acquirer]["Item No."] is np.NaN:
#     #     #     output_row['Item Code'] = np.NaN
#     #     # else:
#     #     output_row['Item Code'] = acquirer_n_device_model_to_item_no_n_item_desciption[device_name][acquirer]["Item No."]
#     #     output_row['Item Name'] = output_row['Item Code']
#     # except Exception as e:
#     #     print(f"Error in Generating Item Code and Item Name: [{device_name} -- {acquirer}] {e}")
#     #     output_row['Item Code'] = f"<ISSUE>{acquirer + '===' + device_name}</ISSUE>"
#     #     output_row['Item Name'] = f"<ISSUE>{acquirer + '===' + device_name}</ISSUE>"
#     try:
#         output_row['Item Description'] = acquirer_n_device_model_to_item_no_n_item_desciption[device_name][acquirer]["Item Description"]
#     except Exception as e:
#         print(f"Error in Generating Item Description: [{device_name} -- {acquirer}] {e}")
#         output_row['Item Description'] = f"<ISSUE>{acquirer + '===' + device_name}</ISSUE>"

#     return output_row


# # =========================================MAPPING FUNCTIONS

# # check columns in each files - validation
# # read data with defined datatype validations
# # while pd.read happens --- itself this info has to be read - also read only columns that are need for processing - This wil avoid RAM exhausting issue



# acquirers = ["KOTAK", "AXIS", "SBI", "HDFC", "IDFC", "ICICI", "YBL"]  
# types = ['installation', 'deinstallation', 'service']
# all_acquirers = ["KOTAK", "AXIS", "SBI", "HDFC", "HDFC AGGR", "IDFC", "ICICI", "YBL"]

# '''
# ====================== uploaded_acquirer vs selcted_acquirer ==========================
# uploaded_acquirer is used to name dataframes and this is the main vairable
# but selected_acquier is just for routing functions. For Example: the
# uploaded_acquirer HDFC AGGR will be routed to use HDFC (selected_acquirer) functions
# ---------------------------------------------------------------------------------------
# '''


# print("Validating if all mandatory columns exist in sheets...")
# # VALIDATION OF COLUMNS IF EXISTS OR NOT
# not_found_columns_data = dict()
# for file_id, file_data in dfs.items():
#     if isinstance(file_data, pd.DataFrame):
#         mandatory_columns = column_validation_mapper[file_id]
#         not_found_mandatory_columns = list(set(mandatory_columns) - set(file_data.columns))
#         if not_found_mandatory_columns:
#             not_found_columns_data[file_id] = not_found_mandatory_columns

# if not_found_columns_data:
#     raise Exception(f"The following mandatory fields are not found: {not_found_columns_data}")


# # SETTING DATE COLUMN DATATYPE:
# for file_id, raw_df in dfs.items():
#     received_date_column_name = columnwise_mapping["Recvd Date__DERIVE"][file_id]
#     try:
#         raw_df[received_date_column_name] = pd.to_datetime(raw_df[received_date_column_name], unit='D', origin='1899-12-30')  # origin='1899-12-30',unit='D
#     except Exception as e:
#         try:
#             print(f"Converting pd.to_datetime Error [{e}], trying with no extra params in pd.to_datetime")
#             raw_df[received_date_column_name] = pd.to_datetime(raw_df[received_date_column_name])
#         except Exception as e:
#             print(f"Retry conversion pd.to_datetime Error [{e}], It seems Recvd Date in current dataframe is in correct format. so continuing")


# # MAIN PROCESS =======================================================================
# print("Aggregating the excels sheets....")

# identified_error_found_files = list(not_found_columns_data.keys())
# selected_keys_in_dfs = set(dfs.keys()).difference(set(identified_error_found_files+["COMPLAINTS"]))

# complaints_df = dfs["COMPLAINTS"]

# output_dfs = dict()
# # LOOP START FOR different sheets
# for uploaded_sheet in dfs.keys():
#     if uploaded_sheet in selected_keys_in_dfs:
        
#         print(f"selected uploaded_sheet = {uploaded_sheet}")
#         # to avoid master complaints from here:
#         if uploaded_sheet in all_acquirers:
#             uploaded_acquirer = uploaded_sheet
#             # checking if the acquirer is not in ["HDFC AGGR"]
#             if uploaded_acquirer in acquirers:
#                 selected_acquirer = uploaded_acquirer
#                 if dfs[uploaded_acquirer] is None:
#                     print(f"Skipping {uploaded_acquirer} processing since sheet is not found")
#                     continue
#                 else:
#                     # assigning dataframe for further processing
#                     df = dfs[uploaded_acquirer]

#             elif uploaded_acquirer == "HDFC AGGR":
#                 selected_acquirer = "HDFC"
#                 if dfs[uploaded_acquirer] is None:
#                     print(f"Skipping {uploaded_acquirer} processing since sheet is not found")
#                     continue
#                 else:

#                     # assigning dataframe for further processing
#                     df = dfs[uploaded_acquirer]
#             else:
#                 raise Exception(f"The uploaded acquirer [{uploaded_acquirer}] is not identified")


#         output_dfs[uploaded_acquirer] = dict()  # it can never be selected acquirer if so one will be replaced by next since selected acquirer is not unique   -- VVERY IMPORTANT

#         # LOOP START FOR TYPES HERE
#         for type_ in types:
#             print(f"Processing for {type_.upper()} Data of {uploaded_acquirer}")

#             # # setting_up column datatype and formatting  ---------- NOT GOOD APPROACH -- PLEASE CHANGE LATER
#             received_date_column_name = columnwise_mapping["Recvd Date__DERIVE"][selected_acquirer]
#             # try:
#             #     df[received_date_column_name] = pd.to_datetime(df[received_date_column_name], unit='D', origin='1899-12-30')  # origin='1899-12-30',unit='D
#             # except Exception as e:
#             #     print(f"Converting pd.to_datetime Error [{e}], trying with no extra params in pd.to_datetime")
#             #     try:
#             #         df[received_date_column_name] = pd.to_datetime(df[received_date_column_name])
#             #     except Exception as e:
#             #         print(f"Retry conversion pd.to_datetime Error [{e}], It seems Recvd Date in current dataframe is in correct format. so continuing")



#             # IMPORTANT: filtering data is different for installation-deinstallation data and breakfix data

#             if type_ == "installation":
                
#                 received_date_column_name = columnwise_mapping["Recvd Date__DERIVE"][selected_acquirer]
#                 # installation: Recvd Date == selected date ans Status == Pending
#                 pending_ones = df[df['Status'] == 'Pending']
#                 pending_on_date = pending_ones[pending_ones[received_date_column_name].dt.date == date_for_data_filter]  # filtering by selected date
#                 # print("DEBUGGING....\n", pending_on_date); import sys; sys.exit()
#                 filtered_data = pending_on_date

#             elif type_ == "deinstallation":
#                 received_date_column_name = columnwise_mapping["Recvd Date__DERIVE"][selected_acquirer]
#                 # de-installation: received_date_column_name == selected date ans Status == Deactive Pending
#                 deactive_pending_ones = df[df['Status'] == 'Deactive Pending']
#                 deactive_pending_on_date = deactive_pending_ones[deactive_pending_ones[received_date_column_name].dt.date == date_for_data_filter]  # filtering by selected date
#                 filtered_data = deactive_pending_on_date

#             elif type_ == "service":  # aservice = breakfix = complaint
#                 received_date_column_name = columnwise_mapping["Recvd Date__DERIVE"]["COMPLAINTS"]
#                 print(f"Fetching Complaints.. for {uploaded_acquirer}\
#                     {'where selected_acquirer is '+selected_acquirer if uploaded_acquirer != selected_acquirer else ''}")
#                 # breakfix: received_date_column_name <= selected date ans Status == Open
#                 acquirer_specific = complaints_df[complaints_df["Acquirer"].str.upper() == selected_acquirer]  # DANGER ????????????  $%$%%$$%%$^%$^$^%$^$^$^$^$ SEE BELOW COMMENT
#                 # or selected_acquirer - HDFC AGGR in not found anywhere in complaint master unique values. 
#                 # .UPPER MAY NOT WORK FOR HDFC AGGR. if so we might need to map like AXIS: [Axis, AXIS, axis] etc.
#                 open_ones = acquirer_specific[acquirer_specific["Ticket Status"] == 'Open']
#                 open_ones_till_date = open_ones[open_ones[received_date_column_name].dt.date <= date_for_data_filter]
#                 filtered_data = open_ones_till_date

#                 # print(selected_acquirer, "COMPLAINTS___FILTERED", open_ones_till_date.shape)

#             else:
#                 raise Exception("the type_ is not identified.")




#             # this should happen on every types on every acquier so idented inside the types loop

#             # Basic mapping  -- Above ticket type should be checked in internal function do basic mapping
#             if type_ in ['installation', "deinstallation"]:
#                 data_after_basic_mapping = filtered_data.apply(lambda input_row: do_basic_mapping(input_row, type_, selected_acquirer,), axis=1)
#                 there_is_difference_between_map_fn_out_and_columnwise_mapping_keys = bool(list(set(data_after_basic_mapping.columns) - set(columnwise_mapping.keys())))

#                 # checking if empty dataframe is used to apply function, if so, the source df columns will be coming out again. we need to fix it
#                 if there_is_difference_between_map_fn_out_and_columnwise_mapping_keys:
#                     data_after_basic_mapping = pd.DataFrame(columns=columnwise_mapping.keys())
#                 else:
#                     data_after_basic_mapping = data_after_basic_mapping

#             elif type_ == 'service':
#                 data_after_basic_mapping = filtered_data.apply(lambda input_row: do_basic_mapping(input_row, type_, "COMPLAINTS",), axis=1)
#                 there_is_difference_between_map_fn_out_and_columnwise_mapping_keys = bool(list(set(data_after_basic_mapping.columns) - set(columnwise_mapping.keys())))
#                 # if type_ == "service": print(selected_acquirer, "COMPLAINTS___FILTERED", filtered_data.shape)
#                 # if type_ == "service": print(selected_acquirer, "COMPLAINTS___BASEMAPPED", data_after_basic_mapping.shape)
#                 # print(selected_acquirer, "COMPLAINTS___BASEMAPPED", data_after_basic_mapping.shape)
#                 # checking if empty dataframe is used to apply function, if so, the source df columns will be coming out again. we need to fix it
#                 if there_is_difference_between_map_fn_out_and_columnwise_mapping_keys:
#                     data_after_basic_mapping = pd.DataFrame(columns=columnwise_mapping.keys())
#                 else:
#                     data_after_basic_mapping = data_after_basic_mapping
#                 # if type_ == "service": print(selected_acquirer, "COMPLAINTS___FILTERED", filtered_data.shape)
#                 # if type_ == "service": print(selected_acquirer, "COMPLAINTS___BASEMAPPED", data_after_basic_mapping.shape)
#             else:
#                 raise Exception("type_ is not recognized in basic mapping section")
            
#             # 'Ticket Type' # Call Type','Subject'
#             data_after_basic_mapping['Ticket Type'] = type_.title()
#             data_after_basic_mapping["Call Type"] = data_after_basic_mapping['Ticket Type']
#             data_after_basic_mapping["Subject"] = data_after_basic_mapping['Ticket Type']
            
#             # Acquirer
#             data_after_basic_mapping['Acquirer'] = selected_acquirer  # DANGER or selected_acquier for HDFC_AGGR  -------------------> 


#             # spl_code_mapping  #  # changed from Region to Zone on jan 23, 2023
#             data_after_basic_mapping['SPL Code'] = data_after_basic_mapping["Zone"].apply(lambda x: do_mapping_from_zone_to_spl_code(x))
#             # if type_ in ['installation', "deinstallation"]:  # changed from Region to Zone on jan 23, 2023
#             #     data_after_basic_mapping['SPL Code'] = data_after_basic_mapping["Zone"].apply(lambda x: do_mapping_from_zone_to_spl_code(x))
#             # elif type_ in ['service']: ?????????????????????????????????? 

#             # BP Code, Customer 
#             data_after_basic_mapping["BP Code"] = data_after_basic_mapping['Acquirer'].apply(lambda x: do_mapping_from_acquirer_to_bp_code(x))
#             data_after_basic_mapping["Customer"] = data_after_basic_mapping['Acquirer'].apply(lambda x: do_mapping_from_acquirer_to_bp_name(x))
            
#             # Status
#             data_after_basic_mapping['Status'] = "Open"         # ALL open?
            
#             #  'Item Code', 'Item Name', 'Item Description'
#             # if type_ in ['installation', "deinstallation"]:
#             item_info_df = data_after_basic_mapping.apply(
#                 lambda input_row: do_mapping_for_item_number_n_name_n_description(input_row), 
#                 axis=1
#             )
#             #=== POSSIBLE ERRROR of dataframe is empyt which is used to apply function if so Item Code not foudn issue might come
#             data_after_basic_mapping["Item Code"] = item_info_df["Item Code"]
#             data_after_basic_mapping["Item Name"] = item_info_df["Item Name"]
#             data_after_basic_mapping["Item Description"] = item_info_df["Item Description"]
            
#             # POA Date
#             data_after_basic_mapping['POA Date'] = date_for_data_filter

#             # mappign state short names to state names
#             data_after_basic_mapping['State'] = data_after_basic_mapping['State'].apply(
#                 lambda x: statenames_n_short_codes[x.upper()] \
#                     if x.upper() in statenames_n_short_codes.keys() \
#                         else statenames_n_short_codes[x.upper().replace("&", "AND")] \
#                             if x.upper().replace("&", "AND") in statenames_n_short_codes.keys()\
#                                 else f"<ISSUE>{x}</ISSUE>"
#             )

#             final_df = data_after_basic_mapping  # change this later as process progress
#             # finally adding them to output_dict
#             output_dfs[uploaded_acquirer][type_] = final_df.reset_index(drop=True)
#     else:
#         print(f"Excluding {uploaded_sheet}")

# # print(output_dfs)
# print(100*"*")

# # ======================================================================= MAIN PROCESS 

# print("Combining all sheets...")
# # Removing __DERIVE columns and adding filter columns and combining all of them to one sheet
# derive_columns = ['Recvd Date__DERIVE', 'Device Name__DERIVE']  # 'Recvd Date__DERIVE', 'Device Name__DERIVE'

# list_of_output_sheets = []

# for bank in output_dfs.keys():
#     for type_ in types:
#         value_of_output_dfs = output_dfs[bank][type_]
#         print(type(value_of_output_dfs), "=============================================")
#         if value_of_output_dfs is None:
#             print(f"The data sheet for {bank} if not found. Therefore skipping it.")
#         else:
#             print(bank, type_)
#             df:pd.DataFrame = value_of_output_dfs
#             # print(100*"-")
#             df.drop(derive_columns, axis=1, inplace=True)
#             columns = ["BANK_FILTER", "TYPE_FILTER"] + list(df.columns)
#             df["BANK_FILTER"] = bank
#             df["TYPE_FILTER"] = type_.upper()
#             df = df[columns]  # ordering columns
#             list_of_output_sheets.append(df)


# master_df = pd.concat(list_of_output_sheets, axis=0)
# # print(list_of_output_sheets)
# # print(master_df)


# from sap_upload_excel_creator.functions import dataframe_export_to_excel
# dataframe_export_to_excel(master_df, ".temp/MASTER.xlsx", sheet_name="Data Aggregated", engine="xlsxwriter")

# print("DONE ................................................................")



from sap_upload_excel_creator.

import hashlib

def hash_password(password):
    # Use sha256 to hash the password
    password_hash = hashlib.sha256(password.encode()).hexdigest()
    return password_hash

def store_password(password_hash):
    # Write the hashed password to a file
    with open("hashed_password.txt", "w") as f:
        f.write(password_hash)

# Get the password from the user
password = input("Enter your password: ")

# Hash the password
password_hash = hash_password(password)

# Store the hashed password in a file
store_password(password_hash)




