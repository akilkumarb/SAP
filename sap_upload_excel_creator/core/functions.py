import datetime
import pickle
import numpy as np
import pandas as pd
from openpyxl.utils import get_column_letter

from ..paths import EMPTY_DF_DIR
# from sap_upload_excel_creator.paths import EMPTY_DF_DIR
from .mappers import (
    load_columnwise_mapping, 
    load_acquirer_n_device_model_to_item_no_n_item_desciption_mapping,
    load_spl_code_mapping,
    load_statenames_n_short_codes_mapping,
    load_bp_codes_n_names_mapping,
    load_deactivation_date_column_mapping,
    load_status_column_mapping,
)
from .validate import check_mandatory_columns_available

pd.options.display.max_columns = 1000


def do_basic_mapping(input_row:pd.Series, type_:str, selected_file:str):
    columnwise_mapping = load_columnwise_mapping()


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

def do_mapping_from_zone_to_spl_code(zone):  # changed from region to zone on Jan 23, 2023
    spl_code_mapping = load_spl_code_mapping()
    if zone is np.NaN:
        return np.NaN
    elif zone.upper() in spl_code_mapping:
        return str(spl_code_mapping[zone.upper()]['SPL Code'])   # ISSEUE AGAIN MAPPING(DELHI NCR) contains delhi. Can I map spl code for DELHI NCR to DELHI?
    else:
        print(f"Error while mapping zone to spl code: <ISSUE>{zone}</ISSUE>")
        return f"<ISSUE>{zone}</ISSUE>"

def do_mapping_from_acquirer_to_bp_code(acquirer):
    bp_codes_n_names = load_bp_codes_n_names_mapping()
    if acquirer in bp_codes_n_names.keys():
        return bp_codes_n_names[acquirer]["BP Code"]
    else:
        print(f"Error while mapping acquirer to bp code: <ISSUE>{acquirer}</ISSUE>")
        return f"<ISSUE>{acquirer}</ISSUE>"

def do_mapping_from_acquirer_to_bp_name(acquirer):  # or to customer
    bp_codes_n_names = load_bp_codes_n_names_mapping()
    if acquirer in bp_codes_n_names.keys():
        return bp_codes_n_names[acquirer]["BP Name"]
    else:
        print(f"Error while mapping acquirer to bp name: <ISSUE>{acquirer}</ISSUE>")
        return f"<ISSUE>{acquirer}</ISSUE>"


def do_mapping_for_item_number_n_name_n_description(input_row):
    acquirer_n_device_model_to_item_no_n_item_desciption = load_acquirer_n_device_model_to_item_no_n_item_desciption_mapping()
    # 'Item Code', 'Item Name', 'Item Description'
    output_row = pd.Series(dtype="object", index=['Item Code', 'Item Name', 'Item Description'])
    device_name, acquirer = input_row["Device Name__DERIVE"], input_row['Acquirer']

    # trying to break the code when excpetions other than KeyError occur - BEWARE
    try:
        output_row['Item Code'] = acquirer_n_device_model_to_item_no_n_item_desciption[device_name][acquirer]["Item No."]
    except KeyError as e:
        print(f"Error: unknown device_name or acquirer {e}")
        output_row['Item Code'] = f"<ISSUE>{device_name} == {acquirer}</ISSUE>"
    # except Exception as e:
        
    output_row['Item Name'] = output_row['Item Code']
    # import sys; sys.exit()
    # try:
    #     # if acquirer_n_device_model_to_item_no_n_item_desciption[device_name][acquirer]["Item No."] is np.NaN:
    #     #     output_row['Item Code'] = np.NaN
    #     # else:
    #     output_row['Item Code'] = acquirer_n_device_model_to_item_no_n_item_desciption[device_name][acquirer]["Item No."]
    #     output_row['Item Name'] = output_row['Item Code']
    # except Exception as e:
    #     print(f"Error in Generating Item Code and Item Name: [{device_name} -- {acquirer}] {e}")
    #     output_row['Item Code'] = f"<ISSUE>{acquirer + '===' + device_name}</ISSUE>"
    #     output_row['Item Name'] = f"<ISSUE>{acquirer + '===' + device_name}</ISSUE>"
    try:
        output_row['Item Description'] = acquirer_n_device_model_to_item_no_n_item_desciption[device_name][acquirer]["Item Description"]
    except Exception as e:
        print(f"Error in Generating Item Description: [{device_name} -- {acquirer}] {e}")
        output_row['Item Description'] = f"<ISSUE>{str(acquirer) + '===' + str(device_name)}</ISSUE>"

    return output_row


def generate(dfs, date_for_data_filter):
    status_column_mapping = load_status_column_mapping()
    # redoing validation again -- later remove repetition
    _, _,  not_found_columns_data = check_mandatory_columns_available(dfs)
    deactivation_date_column_mapping = load_deactivation_date_column_mapping()
    columnwise_mapping = load_columnwise_mapping()
    statenames_n_short_codes = load_statenames_n_short_codes_mapping()
    acquirers = ["KOTAK", "AXIS", "SBI", "HDFC", "IDFC", "ICICI", "YBL"]  
    types = ['installation', 'deinstallation', 'service']
    all_acquirers = ["KOTAK", "AXIS", "SBI", "HDFC", "HDFC AGGR", "IDFC", "ICICI", "YBL"]

    '''
    ====================== uploaded_acquirer vs selcted_acquirer ==========================
    uploaded_acquirer is used to name dataframes and this is the main vairable
    but selected_acquier is just for routing functions. For Example: the
    uploaded_acquirer HDFC AGGR will be routed to use HDFC (selected_acquirer) functions
    ---------------------------------------------------------------------------------------
    '''


    # SETTING DATE COLUMN DATATYPE:
    for file_id, raw_df in dfs.items():
        received_date_column_name = columnwise_mapping["Recvd Date__DERIVE"][file_id if file_id != "HDFC AGGR" else "HDFC"]
        try:
            raw_df[received_date_column_name] = pd.to_datetime(raw_df[received_date_column_name], unit='D', origin='1899-12-30')  # origin='1899-12-30',unit='D
        except Exception as e:
            try:
                print(f"Converting pd.to_datetime Error [{e}], trying with no extra params in pd.to_datetime")
                raw_df[received_date_column_name] = pd.to_datetime(raw_df[received_date_column_name])
            except Exception as e:
                print(f"Retry conversion pd.to_datetime Error [{e}], It seems Recvd Date in current dataframe is in correct format. so continuing")
        dfs[file_id] = raw_df

    # # pickling for debugging purpose
    # import pickle
    # with open("assets/dummy_dfs/empty_dfs.pkl", 'wb') as f:
    #     pickle.dump(dfs, f)
    
    with open(EMPTY_DF_DIR / "empty_dfs.pkl", 'rb') as f:  # functions.py 139 line
        empty_dfs = pickle.load(f)

    # FIXING ISSUE if COMPLAINTS excel file is only uploaded
    # adding empty dataframes if dataframe is not found or file-id is not found in keys. 
    # beware that later checks if isinstance(df, pd.DataFrame) will not work ============= DANGER
    for file_id, empty_df in empty_dfs.items():
        if file_id in dfs.keys():  # change this to dfs instead of dfs
            if dfs[file_id] is None:
                dfs[file_id] = empty_df
            else:
                dfs[file_id] = dfs[file_id]  # this else block is not needed but for clarify purpose we use

        else:
            dfs[file_id] = empty_df
    
    # MAIN PROCESS =======================================================================
    print("Aggregating the excels sheets....")

    identified_error_found_files = list(not_found_columns_data.keys())
    selected_keys_in_dfs = set(dfs.keys()).difference(set(identified_error_found_files+["COMPLAINTS"]))
    
    if "COMPLAINTS" in dfs.keys():
        complaints_df = dfs["COMPLAINTS"]
    else:
        complaints_df = None

    output_dfs = dict()
    # LOOP START FOR different sheets
    for uploaded_sheet in dfs.keys():
        if uploaded_sheet in selected_keys_in_dfs:
            
            print(f"selected uploaded_sheet = {uploaded_sheet}")
            # to avoid master complaints from here:
            if uploaded_sheet in all_acquirers:
                uploaded_acquirer = uploaded_sheet
                # checking if the acquirer is not in ["HDFC AGGR"]
                if uploaded_acquirer in acquirers:
                    selected_acquirer = uploaded_acquirer
                    if dfs[uploaded_acquirer] is None:
                        print(f"Skipping {uploaded_acquirer} processing since sheet is not found")
                        continue
                    else:
                        # assigning dataframe for further processing
                        df = dfs[uploaded_acquirer]

                elif uploaded_acquirer == "HDFC AGGR":
                    selected_acquirer = "HDFC"
                    if dfs[uploaded_acquirer] is None:
                        print(f"Skipping {uploaded_acquirer} processing since sheet is not found")
                        continue
                    else:

                        # assigning dataframe for further processing
                        df = dfs[uploaded_acquirer]
                else:
                    raise Exception(f"The uploaded acquirer [{uploaded_acquirer}] is not identified")


            output_dfs[uploaded_acquirer] = dict()  # it can never be selected acquirer if so one will be replaced by next since selected acquirer is not unique   -- VVERY IMPORTANT

            # LOOP START FOR TYPES HERE
            for type_ in types:
                print(f"Processing for {type_.upper()} Data of {uploaded_acquirer}")

                # # setting_up column datatype and formatting  ---------- NOT GOOD APPROACH -- PLEASE CHANGE LATER
                received_date_column_name = columnwise_mapping["Recvd Date__DERIVE"][selected_acquirer]
                # try:
                #     df[received_date_column_name] = pd.to_datetime(df[received_date_column_name], unit='D', origin='1899-12-30')  # origin='1899-12-30',unit='D
                # except Exception as e:
                #     print(f"Converting pd.to_datetime Error [{e}], trying with no extra params in pd.to_datetime")
                #     try:
                #         df[received_date_column_name] = pd.to_datetime(df[received_date_column_name])
                #     except Exception as e:
                #         print(f"Retry conversion pd.to_datetime Error [{e}], It seems Recvd Date in current dataframe is in correct format. so continuing")



                # IMPORTANT: filtering data is different for installation-deinstallation data and breakfix data

                if type_ == "installation":
                    status_column_name = status_column_mapping[uploaded_acquirer]

                    
                    received_date_column_name = columnwise_mapping["Recvd Date__DERIVE"][selected_acquirer]
                    # installation: Recvd Date == selected date ans Status == Pending

                    pending_ones = df[df[status_column_name] == 'Pending']

                    pending_on_date = pending_ones[pending_ones[received_date_column_name].dt.date == date_for_data_filter]  # filtering by selected date
                    # print("DEBUGGING....\n", pending_on_date); import sys; sys.exit()
                    filtered_data = pending_on_date

                elif type_ == "deinstallation":
                    status_column_name = status_column_mapping[uploaded_acquirer]
                    # received_date_column_name = columnwise_mapping["Recvd Date__DERIVE"][selected_acquirer]

                    # deactivation_date_column_mapping -- has to be added here -- add the column to mandatory columns set
                    deactivation_date_column_name = deactivation_date_column_mapping[selected_acquirer]



                    # de-installation: received_date_column_name == selected date ans Status == Deactive Pending
                    deactive_pending_ones = df[df[status_column_name] == 'Deactive Pending']     # until deactivation date ??


                    # import pickle
                    # with open("test.pkl", 'wb') as f:
                    #     pickle.dump(df, f)

                    # dealing with '--' in col which is meant to be datetime
                    deactive_pending_ones[deactivation_date_column_name]= deactive_pending_ones[deactivation_date_column_name].apply(lambda x: np.NaN if str(x) == "--" else x)

                    # converting the above date col to pandas datatime fmt
                    try:
                        deactive_pending_ones[deactivation_date_column_name] = pd.to_datetime(deactive_pending_ones[deactivation_date_column_name], unit='D', origin='1899-12-30')  # origin='1899-12-30',unit='D
                    except Exception as e:
                        deactive_pending_ones[deactivation_date_column_name] = pd.to_datetime(deactive_pending_ones[deactivation_date_column_name])
                        # try:
                        # except: 
                        #     # debugging purpose
                        #     import pickle
                        #     print(f"|||||||||||||| - [{deactivation_date_column_name}][{selected_acquirer}][{type_}]")
                        #     with open(f'temp_df_deactive_col_{deactivation_date_column_name}.pkl', "wb") as f:
                        #         pickle.dump(deactive_pending_ones, f)

                            

                    deactive_pending_on_date = deactive_pending_ones[deactive_pending_ones[deactivation_date_column_name].dt.date <= date_for_data_filter]  # filtering by selected date
                    filtered_data = deactive_pending_on_date

                elif type_ == "service":  # aservice = breakfix = complaint
                    status_column_name = status_column_mapping["COMPLAINTS"]
                    if complaints_df is None:
                        continue
                    received_date_column_name = columnwise_mapping["Recvd Date__DERIVE"]["COMPLAINTS"]
                    print(f"Fetching Complaints.. for {uploaded_acquirer}\
                        {'where selected_acquirer is '+selected_acquirer if uploaded_acquirer != selected_acquirer else ''}")
                    # breakfix: received_date_column_name <= selected date ans Status == Open
                    acquirer_specific = complaints_df[complaints_df["Acquirer"].str.upper() == selected_acquirer]  # DANGER ????????????  $%$%%$$%%$^%$^$^%$^$^$^$^$ SEE BELOW COMMENT
                    # or selected_acquirer - HDFC AGGR in not found anywhere in complaint master unique values. 
                    # .UPPER MAY NOT WORK FOR HDFC AGGR. if so we might need to map like AXIS: [Axis, AXIS, axis] etc.
                    open_ones = acquirer_specific[acquirer_specific[status_column_name] == 'Open']
                    # open_ones.to_excel("ISSUE_BEFORE_DATE_FILTER_SERVICE.xlsx", engine="xlsxwriter")

                    # deactivation_date_column_mapping -- has to be added here -- add the column to mandatory columns set
                    open_ones_till_date = open_ones[open_ones[received_date_column_name].dt.date <= date_for_data_filter]

                    # open_ones_till_date.to_excel("ISSUE_AFTER_DATE_SERVICE.xlsx", engine="xlsxwriter")
                    filtered_data = open_ones_till_date

                    # print(selected_acquirer, "COMPLAINTS___FILTERED", open_ones_till_date.shape)

                else:
                    raise Exception("the type_ is not identified.")


                # this should happen on every types on every acquier so idented inside the types loop

                # Basic mapping  -- Above ticket type should be checked in internal function do basic mapping
                if type_ in ['installation', "deinstallation"]:
                    data_after_basic_mapping = filtered_data.apply(lambda input_row: do_basic_mapping(input_row, type_, selected_acquirer,), axis=1)
                    there_is_difference_between_map_fn_out_and_columnwise_mapping_keys = bool(list(set(data_after_basic_mapping.columns) - set(columnwise_mapping.keys())))

                    # checking if empty dataframe is used to apply function, if so, the source df columns will be coming out again. we need to fix it
                    if there_is_difference_between_map_fn_out_and_columnwise_mapping_keys:
                        data_after_basic_mapping = pd.DataFrame(columns=columnwise_mapping.keys())
                    else:
                        data_after_basic_mapping = data_after_basic_mapping

                elif type_ == 'service':
                    if complaints_df is None:
                        data_after_basic_mapping= None
                        continue
                    data_after_basic_mapping = filtered_data.apply(lambda input_row: do_basic_mapping(input_row, type_, "COMPLAINTS",), axis=1)
                    there_is_difference_between_map_fn_out_and_columnwise_mapping_keys = bool(list(set(data_after_basic_mapping.columns) - set(columnwise_mapping.keys())))
                    # if type_ == "service": print(selected_acquirer, "COMPLAINTS___FILTERED", filtered_data.shape)
                    # if type_ == "service": print(selected_acquirer, "COMPLAINTS___BASEMAPPED", data_after_basic_mapping.shape)
                    # print(selected_acquirer, "COMPLAINTS___BASEMAPPED", data_after_basic_mapping.shape)
                    # checking if empty dataframe is used to apply function, if so, the source df columns will be coming out again. we need to fix it
                    if there_is_difference_between_map_fn_out_and_columnwise_mapping_keys:
                        data_after_basic_mapping = pd.DataFrame(columns=columnwise_mapping.keys())
                    else:
                        data_after_basic_mapping = data_after_basic_mapping
                    # if type_ == "service": print(selected_acquirer, "COMPLAINTS___FILTERED", filtered_data.shape)
                    # if type_ == "service": print(selected_acquirer, "COMPLAINTS___BASEMAPPED", data_after_basic_mapping.shape)
                    
                else:
                    raise Exception("type_ is not recognized in basic mapping section")
                
                if data_after_basic_mapping is None:  # this complaint df is not provided.. this will help not to break the app
                    continue
                else:
                    # 'Ticket Type' # Call Type','Subject'
                    data_after_basic_mapping['Ticket Type'] = type_.title()  # Final Remarks for ICICI and IDFC
                    data_after_basic_mapping["Call Type"] = data_after_basic_mapping['Ticket Type']  
                    data_after_basic_mapping["Subject"] = data_after_basic_mapping['Ticket Type']

                    # Sub Type -- Subject Type
                    data_after_basic_mapping['Sub Type'] = data_after_basic_mapping['Sub Type'].apply(
                        lambda x: "New Installation" if type_ == 'installation' else 'Terminal Pickup' if type_ == "deinstallation" else x )
                    
                    # Acquirer
                    data_after_basic_mapping['Acquirer'] = selected_acquirer  # DANGER or selected_acquier for HDFC_AGGR  -------------------> 


                    # spl_code_mapping  #  # changed from Region to Zone on jan 23, 2023
                    data_after_basic_mapping['SPL Code'] = data_after_basic_mapping["Zone"].apply(lambda x: do_mapping_from_zone_to_spl_code(x))
                    # if type_ in ['installation', "deinstallation"]:  # changed from Region to Zone on jan 23, 2023
                    #     data_after_basic_mapping['SPL Code'] = data_after_basic_mapping["Zone"].apply(lambda x: do_mapping_from_zone_to_spl_code(x))
                    # elif type_ in ['service']: ?????????????????????????????????? 

                    # BP Code, Customer 
                    data_after_basic_mapping["BP Code"] = data_after_basic_mapping['Acquirer'].apply(lambda x: do_mapping_from_acquirer_to_bp_code(x))
                    data_after_basic_mapping["Customer"] = data_after_basic_mapping['Acquirer'].apply(lambda x: do_mapping_from_acquirer_to_bp_name(x))
                    
                    # Status
                    data_after_basic_mapping['Status'] = "Open"         # ALL Open
                    
                    #  'Item Code', 'Item Name', 'Item Description'
                    # if type_ in ['installation', "deinstallation"]:
                    item_info_df = data_after_basic_mapping.apply(
                        lambda input_row: do_mapping_for_item_number_n_name_n_description(input_row), 
                        axis=1
                    )
                    #=== POSSIBLE ERRROR of dataframe is empyt which is used to apply function if so Item Code not foudn issue might come
                    data_after_basic_mapping["Item Code"] = item_info_df["Item Code"] 
                    data_after_basic_mapping["Item Name"] = item_info_df["Item Name"]
                    data_after_basic_mapping["Item Description"] = item_info_df["Item Description"]
                    
                    # POA Date
                    data_after_basic_mapping['POA Date'] = date_for_data_filter

                    # mappign state short names to state names
                    data_after_basic_mapping['State'] = data_after_basic_mapping['State'].apply(
                        lambda x: statenames_n_short_codes[x.upper()] \
                            if x.upper() in statenames_n_short_codes.keys() \
                                else statenames_n_short_codes[x.upper().replace("&", "AND")] \
                                    if x.upper().replace("&", "AND") in statenames_n_short_codes.keys()\
                                        else f"<ISSUE>{x}</ISSUE>"
                    )

                    data_after_basic_mapping["Store id"] = data_after_basic_mapping["Store id"].astype(str)
                    data_after_basic_mapping["Store id"] = data_after_basic_mapping["Store id"].apply(lambda x: np.NaN if x== "nan" else x )
                    final_df = data_after_basic_mapping  # change this later as process progress

                    # finally adding them to output_dict
                    output_dfs[uploaded_acquirer][type_] = final_df.reset_index(drop=True)
        else:
            print(f"Excluding {uploaded_sheet}")

    # print(output_dfs)
    print(100*"*")

    # ======================================================================= MAIN PROCESS 


    print("Combining all sheets...")
    # Removing __DERIVE columns and adding filter columns and combining all of them to one sheet
    derive_columns = ['Recvd Date__DERIVE', 'Device Name__DERIVE']  # 'Recvd Date__DERIVE', 'Device Name__DERIVE'

    list_of_output_sheets = []

    for bank in output_dfs.keys():
        for type_ in output_dfs[bank].keys():  # to avoid complaints df empty issue. this is edited from 'for type_ in types'  to 'output_dfs[bank].keys()'
            value_of_output_dfs = output_dfs[bank][type_]
            print(type(value_of_output_dfs), "=============================================")
            if value_of_output_dfs is None:
                print(f"The data sheet for {bank} if not found. Therefore skipping it.")
            else:
                print(bank, type_)
                df:pd.DataFrame = value_of_output_dfs
                # print(100*"-")
                df.drop(derive_columns, axis=1, inplace=True)
                columns = ["BANK_FILTER", "TYPE_FILTER"] + list(df.columns)
                df["BANK_FILTER"] = bank
                df["TYPE_FILTER"] = type_.upper()
                df = df[columns]  # ordering columns
                list_of_output_sheets.append(df)


    master_df = pd.concat(list_of_output_sheets, axis=0)
    return master_df


# from sap_upload_excel_creator.functions import dataframe_export_to_excel
# dataframe_export_to_excel(master_df, ".temp/MASTER.xlsx", sheet_name="Data Aggregated", engine="xlsxwriter")

# print("DONE ................................................................")


def aggregate(input_row, type_):
    row = pd.Series(dtype="object")
    # ============== WHAT SHOULD BE THE NAN VALUE FOR SC ENTRY AND SERVICE TICKET NUMBER ETC. "--"? 
    row['SC Entry'] = "--"  # ? not filled by us
    row['Service Ticket Number'] = "--"  # bcz this is only for break fix
    row['Transaction Type'] = "A"  # is this only for installation only? if so, make an if statment here also
    row['Reporting Type'] = input_row['Segment']
    row['Priority'] = "M"  # is this for all? including instalation, deinstallation and breakfix?
    row['Acquirer'] = input_row["Sponsor Bank"]  # or ?? input_row["Billed By"]

    if type_ == "installation":  # ie. status == Pending
        row['Ticket Type'] = "Installation"
    elif type_ == "deinstallation": # ie. status == "Deactive Pending"
        row['Ticket Type'] = "Deinstallation"
    else:
        raise NotImplementedError("Not sure what ticket type to use for this type")

    row['Call Type'] = row['Ticket Type']
    row['Subject'] = row['Ticket Type']

    if type_ == "installation":
        row['Sub Type'] = "New Installation"
    elif type_ == "deinstallation":
        row['Sub Type'] = "Terminal Pickup"
    else:
        raise NotImplementedError(f"Not sure what Sub Type to use for this type '{type_}'")

    # row['BP Code'] = ?   ----- need mapping from SAP  - busines partner code
    row['Customer'] = input_row["Login"]
    row['Contact Person'] = input_row["Login"]

    row['Merchant Name'] = input_row['Merchant Name']
    row['DBA Name'] = input_row["Merchant DBA Name"]

    row['Address'] = input_row["Address"]
    row["City"] = input_row["City"]
    row['Location'] = input_row["City"]   # ? predefined fields  - double check is City has only been used...
    row['Pincode'] = input_row["Pincode"]
    row["State"] = input_row["State"]   # might need to change to two letter abbreviation from mapping - State Shortcoes.xlsx

    row["Zone"] = input_row["New Team"]
    row["Region"] = input_row["Region"]

    row["Phone No"] = input_row["Login"]
    row["Merchant Phone No"] = input_row["Login"]
    row["User ID"] = input_row["Login"]
    row["MID"] = input_row["MID"]
    row["TID"] = input_row["TID"]
    row["Old Device Serial"] = input_row["Old Serial Number"]
    row['New Serial Number'] = input_row['Serial Number']  # ????

    # 'Item Code','Item Name', 'Item Description' ---> these from SAP or aggregate it from bank and device name fields..
    row['Item Code'] = "NOT IMPLEMENTED YET"
    row['Item Name'] = "NOT IMPLEMENTED YET"
    row['Item Description'] = "NOT IMPLEMENTED YET"

    if type_ == "installation":
        row['Status'] = 'Open'
    else:
        raise NotImplementedError("Not done for de installation and de-installation")  #  ???

    row['Closure Remarks'] = "NOT IMPLEMENTED YET"  # ??
    row['NSTP Remarks'] = "NOT IMPLEMENTED YET"     # ??
    row['SPL Code'] = "NOT IMPLEMENTED YET"         # ??

    row['No Of Visits'] = 0  # int

    row['SIM Provider'] = "NOT IMPLEMENTED YET"
    row['SIM No'] = "NOT IMPLEMENTED YET"
    row['SIM No Old'] = "NOT IMPLEMENTED YET"

    if type_ == "installation":
        row['POA'] = "Planned"
    else:
        raise NotImplementedError("Not done for de installation and de-installation")  #  ???

    row['POA Date'] = pd.to_datetime(datetime.datetime.now().date())  # Today's Date or Date used to filter the data? 

    return row



def dataframe_export_to_excel(df, output_path, sheet_name, write_mode="w", engine='openpyxl'):

    if (write_mode == "a") and (engine == 'openpyxl'):
        writer = pd.ExcelWriter(
            output_path,
            engine=engine,  # openpyxl - no proper date fmt    xlsxwriter - no appen feature
            # datetime_format='dd-mm-yyyy',
            # date_format='dd-mm-yyyy',
            mode=write_mode
        )
    elif (write_mode == "a") and (engine == 'xlsxwriter'):
        print("Warning: append mode not supported in xlsx writer. so the file will be ovewritten")
        writer = pd.ExcelWriter(
            output_path,
            engine=engine,  # openpyxl  xlsxwriter
            datetime_format='dd-mm-yyyy',
            date_format='dd-mm-yyyy'
        )
    else:
        writer = pd.ExcelWriter(
            output_path,
            engine=engine,  # openpyxl  xlsxwriter
            datetime_format='dd-mm-yyyy',
            date_format='dd-mm-yyyy'
        )     

    # Convert the dataframe to an XlsxWriter Excel object.
    df.to_excel(writer, index=False, sheet_name=sheet_name)

    # Get the xlsxwriter workbook and worksheet objects. in order to set the column
    # widths, to make the dates clearer.
    # workbook  = writer.book
    worksheet = writer.sheets[sheet_name]

    # Get the dimensions of the dataframe.
    (max_row, max_col) = df.shape

    # Set the column widths, to make the dates clearer.

    if engine == 'openpyxl':
        for col_number in range(1, max_col):
            worksheet.column_dimensions[get_column_letter(col_number)].width = 20
    elif engine == "xlsxwriter":
        worksheet.set_column(1, max_col, 20)
    else:
        raise Exception("Excel writer Engine is not identifiable")


    # Close the Pandas Excel writer and output the Excel file.
    writer.close()

