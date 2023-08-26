import streamlit as st
import pandas as pd
import re

# Streamlit app title
st.title("Trial Balance Data Converter")

# File uploader
uploaded_file = st.file_uploader("Upload a TXT File", type=["txt"])

# Convert button
if st.button("Convert"):
    if uploaded_file is not None:
        content = uploaded_file.read().decode("utf-8")

        # Retrieve data from txt file to a new DataFrame
        data = []
        for line in content.splitlines():
            line = line.strip()
            if re.match(r"^\d{4}", line):
                parts = re.split(r"\s{2,}", line.strip(), maxsplit=1)
                account = parts[0].strip()
                rest_of_line = parts[1].strip()

                description = re.search(r"^(.*?)\s+18", rest_of_line).group(1)
                rest_of_line = rest_of_line[len(description):].strip()

                parts = rest_of_line.split()
                cuenta = parts[0]
                saldo_inicial = parts[1]
                actividad_periodo = parts[2]
                saldo_final = parts[3]

                data.append([account, description, cuenta, saldo_inicial, actividad_periodo, saldo_final])

        # Processed DataFrame
        column_names = ["Account", "Descripción", "Cuenta_Total", "Saldo Inicial", "Actividad Período", "Saldo Final"]
        df = pd.DataFrame(data, columns=column_names)
        df['Compañía'] = ''
        for row in range(len(df)):
            df['Compañía'][row] = df['Cuenta_Total'][row][:4]
            df['Num Centro'][row] = df['Cuenta_Total'][row][5:12]
            df['Cuenta'][row] = df['Cuenta_Total'][row][13:17]
            df['Subcuenta'][row] = df['Cuenta_Total'][row][18:24]
        df = df.drop('Cuenta_Total', axis=1)
        df = df[['Account', 'Descripción', 'Compañía', 'Num Centro', 'Cuenta', 'Subcuenta',
                 'Saldo Inicial', 'Actividad Período', 'Saldo Final']]
        df['Saldo Inicial'] = (df['Saldo Inicial'].str.replace('[,.]', '', regex=True).astype(float)) / 100
        df['Actividad Período'] = (df['Actividad Período'].str.replace('[,.]', '', regex=True).astype(float)) / 100
        df['Saldo Final'] = (df['Saldo Final'].str.replace('[,.]', '', regex=True).astype(float)) / 100

        # Search for date pattern in txt content using regular expression
        match = re.search(r'Fecha: \d{2}-([A-Z]+)-(\d{4}) \d{2}:\d{2}', content)

        if match:
            month = match.group(1)
            year = match.group(2)
            new_file_name = f"FORMATED_Trial_Balance_Detail_{month}_{year}.csv"
            st.write("New file name:", new_file_name)

            # Generate CSV content
            csv_content = df.to_csv(index=False)

            # Provide a download link for the CSV file
            st.download_button("Download CSV", data=csv_content, file_name=new_file_name)
        else:
            st.write("Pattern not found.")
    else:
        st.write("Upload a TXT file to convert.")
