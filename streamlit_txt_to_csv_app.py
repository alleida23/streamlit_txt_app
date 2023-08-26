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

        # Extract sub-components of Cuenta_Total and add as columns
        df['Compañía'] = ''
        df['Num Centro'] = ''
        df['Cuenta'] = ''
        df['Subcuenta'] = ''
        for row in range(len(df)):
            df['Compañía'][row] = df['Cuenta_Total'][row][:4]
            df['Num Centro'][row] = df['Cuenta_Total'][row][5:12]
            df['Cuenta'][row] = df['Cuenta_Total'][row][13:17]
            df['Subcuenta'][row] = df['Cuenta_Total'][row][18:24]

        # Drop unnecessary column and reorder columns
        df = df.drop('Cuenta_Total', axis=1)
        df = df[['Account', 'Descripción', 'Compañía', 'Num Centro', 'Cuenta', 'Subcuenta',
                 'Saldo Inicial', 'Actividad Período', 'Saldo Final']]

        # Search for date pattern in TXT content
        match = re.search(r'Fecha: \d{2}-([A-Z]+)-(\d{4}) \d{2}:\d{2}', content)

        if match:
            month = match.group(1)
            year = match.group(2)
            new_file_name = f"FORMATED_Trial_Balance_Detail_{month}_{year}.csv"

            # Generate CSV content
            csv_content = df.to_csv(index=False)

            # Create temporary file to store CSV content
            with tempfile.NamedTemporaryFile(delete=False, mode="w", suffix=".csv") as temp_file:
                temp_file.write(csv_content)
                temp_file_path = temp_file.name

            # Clean up uploaded file content from memory
            del content 

            # Function to clean up temporary file
            def cleanup_temp_file():
                os.remove(temp_file_path)

            cleanup_temp_file()

            # Provide download button for the CSV file
            st.download_button("Download CSV", data=csv_content, file_name=new_file_name)
        else:
            st.write("Pattern not found.")
    else:
        st.write("Upload a TXT file to convert.")
