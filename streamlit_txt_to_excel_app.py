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

        # Original df length
        original_length = len(df)
        st.write(f"Initial number of accounting entries: {original_length}.")
        
        # Drop rows from 'Account' column with values >= 5000
        initial_rows_account = df.shape[0]
        df = df[df['Account'].astype(int) < 5000]
        dropped_rows_account = initial_rows_account - df.shape[0]
        st.write(f"Eliminated {dropped_rows_account} accounting entries where 'Account' <= 5000.")

        # Drop rows from 'Subcuenta' column with specific values
        specific_values_to_drop = [184812, 184650, 184902, 184716, 184760, 184761]
        initial_rows_subcuenta = df.shape[0]
        df = df[~df['Subcuenta'].astype(int).isin(specific_values_to_drop)]
        dropped_rows_subcuenta = initial_rows_subcuenta - df.shape[0]
        st.write(f"Eliminated {dropped_rows_subcuenta} accounting entries for 'Subcuenta' values: {', '.join(map(str, specific_values_to_drop))}.")

        # Final df length after dropping rows
        final_length = len(df)
        st.write(f"Number of accounting entries after dropping rows: {final_length}.")
       
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

            # Generate CSV content
            csv_path = os.path.join(tempfile.gettempdir(), f"{base_file_name}.csv")
            df.to_csv(csv_path, index=False)

            # Clean up uploaded file content from memory
            del content

            # Function to clean up temporary files
            def cleanup_temp_files():
                os.remove(csv_path)

            cleanup_temp_files()

            # Provide download button for the CSV file
            st.download_button("Download CSV", data=csv_path, file_name=f"{base_file_name}.csv")
        else:
            st.write("Pattern not found.")
    else:
        st.write("Upload a TXT file to convert.")
