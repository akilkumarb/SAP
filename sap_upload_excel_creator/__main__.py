import streamlit as st
import datetime
import time

import pandas as pd
from io import StringIO

st.title('SAP Upload Data Creator')
st.subheader('An Ezetap Tool to aggregate excel files from sources to create output excel files for SAP')


# date_for_filter = st.date_input(
#     "Select the Date for filtering data",
#     datetime.datetime.now().date())
# st.write('Selected Date is:', date_for_filter.strftime("%d/%m/%Y"))

# bank_file_upload_cols = st.columns(6)

# with bank_file_upload_cols[0]:


# uploaded_file = st.file_uploader("Axis Bank Data Excel: ", type=['xlsx', 'xlsb'])
# if uploaded_file is not None:
#     # To read file as bytes:
#     bytes_data = uploaded_file.getvalue()
#     st.write(bytes_data)

#     # To convert to a string based IO:
#     # stringio = StringIO(uploaded_file.getvalue().decode("utf-8"))
#     # st.write(stringio)

#     # To read file as string:
#     # string_data = stringio.read()
#     # st.write(string_data)

#     # Can be used wherever a "file-like" object is accepted:
#     dataframe = pd.read_excel(uploaded_file, sheet_name="Data")
#     st.write(dataframe)

# kotak_uploaded_file = st.file_uploader("Kotak Master Excel: ", type=['xlsx', 'xlsb'], accept_multiple_files=False)
# axis_uploaded_file = st.file_uploader("Axis Master Excel: ", type=['xlsx', 'xlsb'], accept_multiple_files=False)
# sbi_uploaded_file = st.file_uploader("SBI Master Excel: ", type=['xlsx', 'xlsb'], accept_multiple_files=False)
# hdfc_uploaded_file = st.file_uploader("HDFC Master Excel: ", type=['xlsx', 'xlsb'], accept_multiple_files=False)
# icici_uploaded_file = st.file_uploader("ICICI Master Excel: ", type=['xlsx', 'xlsb'], accept_multiple_files=False)
# idfc_uploaded_file = st.file_uploader("IDFC Master Excel: ", type=['xlsx', 'xlsb'], accept_multiple_files=False)
# complaints_uploaded_file = st.file_uploader("Complaints Master Excel", type=['xlsx', 'xlsb'], accept_multiple_files=False)

# uploaded_files = [axis_uploaded_file, sbi_uploaded_file, hdfc_uploaded_file, icici_uploaded_file, idfc_uploaded_file, complaints_uploaded_file]
# if not all(uploaded_files):
#     st.info("No files uploaded so far")
# elif any(uploaded_files):
#     st.write("The following files were uploaded: ", ", ".join([file.name for file in uploaded_files if file is not None]))
#     st.warning("Please the other files as well")
# else:
#     st.write("The following files were uploaded: ", ", ".join([file.name for file in uploaded_files if file is not None]))
#     # # bytes_data = uploaded_file.read()
#     # st.write("filename:", file.name)

# ==========================================================================================

with st.form("Upload Section"):
    st.write("Please fill in the following input fields:")

    date_for_filter = st.date_input(
        "Select the Date for filtering data",
        datetime.datetime.now().date())
    st.write('Selected Date is:', date_for_filter.strftime("%d/%m/%Y"))

    kotak_uploaded_file = st.file_uploader("Kotak Master Excel: ", type=['xlsx', 'xlsb'], accept_multiple_files=False)
    axis_uploaded_file = st.file_uploader("Axis Master Excel: ", type=['xlsx', 'xlsb'], accept_multiple_files=False)
    sbi_uploaded_file = st.file_uploader("SBI Master Excel: ", type=['xlsx', 'xlsb'], accept_multiple_files=False)
    hdfc_uploaded_file = st.file_uploader("HDFC Master Excel: ", type=['xlsx', 'xlsb'], accept_multiple_files=False)
    icici_uploaded_file = st.file_uploader("ICICI Master Excel: ", type=['xlsx', 'xlsb'], accept_multiple_files=False)
    idfc_uploaded_file = st.file_uploader("IDFC Master Excel: ", type=['xlsx', 'xlsb'], accept_multiple_files=False)
    complaints_uploaded_file = st.file_uploader("Complaints Master Excel", type=['xlsx', 'xlsb'], accept_multiple_files=False)


#    slider_val = st.slider("Form slider")
#    checkbox_val = st.checkbox("Form checkbox")

    # Every form must have a submit button.
    submitted = st.form_submit_button("Upload, Validate & Aggregate")
    uploaded_files = [axis_uploaded_file, sbi_uploaded_file, hdfc_uploaded_file, icici_uploaded_file, idfc_uploaded_file, complaints_uploaded_file]
    if submitted:
        if not all(uploaded_files):  # any change to all
            st.warning('Please upload all files')
        else:
            with st.spinner('Processing...'):
                time.sleep(5)
            st.success('Done!')

st.button("Download the aggregated excel sheet", disabled=not all(uploaded_files))
        



# st.write(data)
