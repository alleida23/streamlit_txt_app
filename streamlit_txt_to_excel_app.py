import streamlit as st
import pandas as pd
import re
import tempfile
import os
import openpyxl

# Streamlit app title
st.title("Trial Balance Data Converter")

# File uploader for TXT file
uploaded_file = st.file_uploader("Upload a TXT File", type=["txt"])

# Convert button
if st.button("Convert"):
    if uploaded_file is not None:
        # Read the content of the uploaded TXT file
        content = uploaded_file.read().decode("utf-8")

        # Parse data from TXT content and process it
        data = []
        for line in content.splitlines():
            line = line.strip()
            if re.match(r"^\d{4}", line):
                parts = re.split(r"\s{2,}", line.strip(), maxsplit=1)
                account = parts[0].strip()
                rest_of_line = parts[1].strip()

                # Extract description
                description = re.search(r"^(.*?)\s+18", rest_of_line).group(1)
                rest_of_line = rest_of_line[len(description):].strip()

                # Parse account details
                parts = rest_of_line.split()
                cuenta = parts[0]
                saldo_inicial = parts[1]
                actividad_periodo = parts[2]
                saldo_final = parts[3]

                data.append([account, description, cuenta, saldo_inicial, actividad_periodo, saldo_final])

        # Create DataFrame from parsed data
        column_names = ["Account", "Descripción", "Cuenta_Total", "Saldo Inicial", "Actividad Período", "Saldo Final"]
        df = pd.DataFrame(data, columns=column_names)

        # Convert 'Saldo Inicial', 'Actividad Período', and 'Saldo Final' columns to float
        df['Saldo Inicial'] = df['Saldo Inicial'].astype(float)
        df['Actividad Período'] = df['Actividad Período'].astype(float)
        df['Saldo Final'] = df['Saldo Final'].astype(float)

        # Extract sub-components of Cuenta_Total and add as columns
        df['Compañía'] = df['Cuenta_Total'].str[:4]
        df['Num Centro'] = df['Cuenta_Total'].str[5:12]
        df['Cuenta'] = df['Cuenta_Total'].str[13:17]
        df['Subcuenta'] = df['Cuenta_Total'].str[18:24]

        # Convert 'Account', 'Compañía', 'Num Centro', 'Cuenta', and 'Subcuenta' columns to string/object
        df['Account'] = df['Account'].astype(str)
        df['Compañía'] = df['Compañía'].astype(str)
        df['Num Centro'] = df['Num Centro'].astype(str)
        df['Cuenta'] = df['Cuenta'].astype(str)
        df['Subcuenta'] = df['Subcuenta'].astype(str)

        # Drop unnecessary column and reorder columns
        df = df.drop('Cuenta_Total', axis=1)
        df = df[['Account', 'Descripción', 'Compañía', 'Num Centro', 'Cuenta', 'Subcuenta',
                 'Saldo Inicial', 'Actividad Período', 'Saldo Final']]

        # Generate EXCEL content
        with tempfile.NamedTemporaryFile(delete=False, mode="wb", suffix=".xlsx") as temp_file:
            excel_writer = pd.ExcelWriter(temp_file, engine='openpyxl')
            df.to_excel(excel_writer, sheet_name='Sheet1', index=False)
            excel_writer.save()

            temp_file_path = temp_file.name

            # Open the saved workbook and worksheet using openpyxl
            workbook = openpyxl.load_workbook(temp_file_path)
            worksheet = workbook.active

            # Set the column format to text for specified columns
            text_format = openpyxl.styles.NumFmtFormat('@')
            for col_num, column_title in enumerate(df.columns, start=1):
                if column_title in ['Account', 'Compañía', 'Num Centro', 'Cuenta', 'Subcuenta']:
                    column_letter = openpyxl.utils.get_column_letter(col_num)
                    for row_num in range(2, len(df) + 2):  # Start from row 2 (header is row 1)
                        worksheet[f'{column_letter}{row_num}'].number_format = text_format

            workbook.save(temp_file_path)

        # Clean up uploaded file content from memory
        del content

        # Provide download button for the EXCEL file
        st.download_button("Download Excel", data=open(temp_file_path, 'rb').read(), file_name=new_file_name)
    else:
        st.write("Upload a TXT file to convert.")
