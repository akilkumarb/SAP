import datetime
import pandas as pd

from paths import ASSETS_DIR
from functions import aggregate, dataframe_export_to_excel


pd.options.display.max_columns = 1000

output_columns = [
    'SC Entry', 'Service Ticket Number', 'Transaction Type',
    'Reporting Type', 'Priority', 'Acquirer', 'Ticket Type', 'Call Type',
    'Subject', 'Sub Type', 'BP Code', 'Customer', 'Contact Person',
    'Merchant Name', 'DBA Name', 'Address', 'City', 'Location', 'Pincode',
    'State', 'Zone', 'Region', 'Phone No', 'Merchant Phone No', 'User ID',
    'MID', 'TID', 'Old Device Serial', 'New Serial Number', 'Item Code',
    'Item Name', 'Item Description', 'Status', 'Closure Remarks',
    'NSTP Remarks', 'SPL Code', 'No Of Visits', 'SIM Provider', 'SIM No',
    'SIM No Old', 'POA', 'POA Date'
]


master_29_file = ASSETS_DIR / "kotak_master (29).xlsb"

df = pd.read_excel(master_29_file, sheet_name="Data")

# checking columns if exists to avoid later issues
columns_to_check_if_exists = ['Status', "Recvd Date"]
for col in columns_to_check_if_exists: assert "Status" in list(df.columns)


# setting date columns
df["Recvd Date"] = pd.to_datetime(df["Recvd Date"], unit='D', origin='1899-12-30')


date_for_data_filter = datetime.date(2023, 1, 9)  # this could be today's date



# Data filtering


pending_onces = df[df['Status'] == 'Pending']  # taking pending only for installation
pending_on_date = pending_onces[pending_onces["Recvd Date"].dt.date == date_for_data_filter]  # filtering by selected date
installation_data = pending_on_date.apply(lambda input_row: aggregate(input_row, type_="installation"), axis=1)

# converting dates back to excel date formats
installation_data["POA Date"] = installation_data["POA Date"].dt.date.astype('<M8[ns]')  # <M8[ns]  datetime64[ns]

# exporting
dataframe_export_to_excel(installation_data, ".temp/test.xlsx", sheet_name="INSTALLATION", engine="xlsxwriter")



