import streamlit as st
import pandas as pd
import re
import tempfile
import os

# Streamlit app title
st.title("Trial Balance Data Converter")

# File uploader for TXT file
uploaded_file = st.file_uploader("Upload a TXT File", type=["txt"])

# Initialize a session state variable to track if conversion has been done
if "conversion_done" not in st.session_state:
    st.session_state.conversion_done = False

# Convert button
if st.button("Convert") or st.session_state.conversion_done:
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

        # Drop unnecessary column and reorder columns
        df = df.drop('Cuenta_Total', axis=1)
        df = df[['Account', 'Descripción', 'Compañía', 'Num Centro', 'Cuenta', 'Subcuenta',
                 'Saldo Inicial', 'Actividad Período', 'Saldo Final']]

        # Prepare filtered dataframe (second file to download)
        df_filtered = df.copy()

        # Original df length
        original_length = len(df_filtered)

        # Drop rows from 'Account' column with values <= 5000
        initial_rows_account = df_filtered.shape[0]
        df_filtered = df_filtered[df_filtered['Account'].astype(int) > 5000]
        dropped_rows_account = initial_rows_account - df_filtered.shape[0]

        # Drop rows from 'Subcuenta' column with specific values
        specific_values_to_drop = ['184812', '184650', '184902', '184716', '184760', '184761']
        initial_rows_subcuenta = df_filtered.shape[0]
        df_filtered = df_filtered[~df_filtered['Subcuenta'].isin(specific_values_to_drop)]
        dropped_rows_subcuenta = initial_rows_subcuenta - df_filtered.shape[0]

        # Final df length after dropping rows
        final_length = len(df_filtered)

        # Convert 'Account', 'Compañía', 'Num Centro', 'Cuenta', and 'Subcuenta' columns to string/object
        df['Account'] = df['Account'].astype(str)
        df['Compañía'] = df['Compañía'].astype(str)
        df['Num Centro'] = df['Num Centro'].astype(str)
        df['Cuenta'] = df['Cuenta'].astype(str)
        df['Subcuenta'] = df['Subcuenta'].astype(str)

        # Search for date pattern in TXT content
        match = re.search(r'Fecha: \d{2}-([A-Z]+)-(\d{4}) \d{2}:\d{2}', content)

        if match:
            month = match.group(1)
            year = match.group(2)
            base_file_name = f"FORMATED_Trial_Balance_Detail_{month}_{year}"
            provisiones_file_name = f"Filtered_Cuentas_Provisiones_{month}_{year}"

            # Generate EXCEL content
            excel_content = df.to_csv(index=False)
            filtered_excel_content = df_filtered.to_csv(index=False)

            # Generate CSV content
            csv_content = df.to_csv(index=False)
            filtered_csv_content = df_filtered.to_csv(index=False)

            # Create temporary files to store EXCEL and CSV content
            with tempfile.NamedTemporaryFile(delete=False, mode="w", suffix=".xlsx") as temp_xlsx_file, \
                 tempfile.NamedTemporaryFile(delete=False, mode="w", suffix=".csv") as temp_csv_file:
                temp_xlsx_file.write(excel_content)
                temp_csv_file.write(csv_content)
                temp_xlsx_file_path = temp_xlsx_file.name
                temp_csv_file_path = temp_csv_file.name

            with tempfile.NamedTemporaryFile(delete=False, mode="w", suffix=".xlsx") as temp_xlsx_file_filtered, \
                 tempfile.NamedTemporaryFile(delete=False, mode="w", suffix=".csv") as temp_csv_file_filtered:
                temp_xlsx_file_filtered.write(filtered_excel_content)
                temp_csv_file_filtered.write(filtered_csv_content)
                temp_xlsx_file_path_filtered = temp_xlsx_file_filtered.name
                temp_csv_file_path_filtered = temp_csv_file_filtered.name

            # Clean up uploaded file content from memory
            del content

            # Function to clean up temporary files
            def cleanup_temp_files():
                os.remove(temp_xlsx_file_path)
                os.remove(temp_csv_file_path)
                os.remove(temp_xlsx_file_path_filtered)
                os.remove(temp_csv_file_path_filtered)

            cleanup_temp_files()

            # Filtered TBD
            st.write(f" ")
            st.write(f"**Full TBD file**")

            # Provide download buttons for the EXCEL and CSV files
            st.download_button("Download Full TBD (Excel)", data=excel_content, file_name=f"{base_file_name}.xlsx")
            st.download_button("Download Full TBD (CSV)", data=csv_content, file_name=f"{base_file_name}.csv")
            st.write(f"Total number of accounting entries: {len(df)}")
            st.write(f" ")

            st.write(f" ")
            st.write(f"**Filtered TBD file**")

            # Provide download buttons for the EXCEL and CSV files (filtered_df)
            st.download_button("Download Cuentas Provisiones (Excel)", data=filtered_excel_content, file_name=f"{provisiones_file_name}.xlsx")
            st.download_button("Download Cuentas Provisiones (CSV)", data=filtered_csv_content, file_name=f"{provisiones_file_name}.csv")
            st.write(f"Final number of accounting entries: {final_length}")
            st.write(f" ")

            # Print Eliminated Entries
            st.write(f"Eliminated entries: 'Account': **{dropped_rows_account}** / 'Subcuenta': **{dropped_rows_subcuenta}**")

            # Set the conversion_done session state variable to True
            st.session_state.conversion_done = True

        else:
            st.write("Pattern not found.")
    else:
        st.write("Upload a TXT file to convert.")

# Clean button to remove temporary files
if st.button("Clean"):
    if hasattr(st.session_state, 'temp_files'):
        temp_files = st.session_state.temp_files
        for file_path in temp_files.values():
            os.remove(file_path)
        st.write("Temporary files cleaned.")
    else:
        st.write("No temporary files to clean.")
