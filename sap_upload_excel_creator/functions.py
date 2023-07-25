import datetime
import pandas as pd
from openpyxl.utils import get_column_letter

pd.options.display.max_columns = 1000



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
    workbook  = writer.book
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

