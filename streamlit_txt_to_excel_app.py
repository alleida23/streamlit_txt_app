import streamlit as st
import pandas as pd
import re
import tempfile
import os

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
        df['Saldo Inicial'] = df['Saldo Inicial'].str.replace(',', '').astype(float)
        df['Actividad Período'] = df['Actividad Período'].str.replace(',', '').astype(float)
        df['Saldo Final'] = df['Saldo Final'].str.replace(',', '').astype(float)

        # Extract sub-components of Cuenta_Total and add as columns
        df['Compañía'] = ''
        df['Num Centro'] = ''
        df['Cuenta'] = ''
        df['Subcuenta'] = ''
        for row in range(len(df)):
            df.loc[row, 'Compañía'] = df.loc[row, 'Cuenta_Total'][:4]
            df.loc[row, 'Num Centro'] = df.loc[row, 'Cuenta_Total'][5:12]
            df.loc[row, 'Cuenta'] = df.loc[row, 'Cuenta_Total'][13:17]
            df.loc[row, 'Subcuenta'] = df.loc[row, 'Cuenta_Total'][18:24]

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
            base_file_name = f"FORMATED_Trial_Balance_Detail_{month}_{year}"

            # Generate EXCEL content
            excel_content = df.to_csv(index=False)

            # Generate CSV content
            csv_content = df.to_csv(index=False)

            # Create temporary files to store EXCEL and CSV content
            with tempfile.NamedTemporaryFile(delete=False, mode="w", suffix=".xlsx") as temp_xlsx_file, \
                 tempfile.NamedTemporaryFile(delete=False, mode="w", suffix=".csv") as temp_csv_file:
                temp_xlsx_file.write(excel_content)
                temp_csv_file.write(csv_content)
                temp_xlsx_file_path = temp_xlsx_file.name
                temp_csv_file_path = temp_csv_file.name

            # Clean up uploaded file content from memory
            del content

            # Function to clean up temporary files
            def cleanup_temp_files():
                os.remove(temp_xlsx_file_path)
                os.remove(temp_csv_file_path)

            cleanup_temp_files()

            # Provide download buttons for the EXCEL and CSV files
            st.download_button("Download Excel", data=excel_content, file_name=f"{base_file_name}.xlsx")
            st.download_button("Download CSV", data=csv_content, file_name=f"{base_file_name}.csv")
        else:
            st.write("Pattern not found.")
    else:
        st.write("Upload a TXT file to convert.")
