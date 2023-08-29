import streamlit as st
import pandas as pd
import re
import tempfile
import os
import xlsxwriter

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

        # Search for date pattern in TXT content
        match = re.search(r'Fecha: \d{2}-([A-Z]+)-(\d{4}) \d{2}:\d{2}', content)

        if match:
            month = match.group(1)
            year = match.group(2)
            new_file_name = f"FORMATED_Trial_Balance_Detail_{month}_{year}.xlsx"

            # Generate EXCEL content
            with tempfile.NamedTemporaryFile(delete=False, mode="wb", suffix=".xlsx") as temp_file:
                excel_writer = pd.ExcelWriter(temp_file, engine='xlsxwriter')
                df.to_excel(excel_writer, sheet_name='Sheet1', index=False)

                # Get the xlsxwriter workbook and worksheet objects
                workbook = excel_writer.book
                worksheet = excel_writer.sheets['Sheet1']

                # Set the column format to text for specified columns
                text_format = workbook.add_format({'num_format': '@'})
                for col_num, column_title in enumerate(df.columns):
                    if column_title in ['Account', 'Compañía', 'Num Centro', 'Cuenta', 'Subcuenta']:
                        worksheet.set_column(col_num, col_num, None, text_format)

                excel_writer.save()

                temp_file_path = temp_file.name

            # Clean up uploaded file content from memory
            del content 

            # Function to clean up temporary file
            def cleanup_temp_file():
                os.remove(temp_file_path)

            cleanup_temp_file()

            # Provide download button for the EXCEL file
            st.download_button("Download Excel", data=open(temp_file_path, 'rb').read(), file_name=new_file_name)
        else:
            st.write("Pattern not found.")
    else:
        st.write("Upload a TXT file to convert.")
