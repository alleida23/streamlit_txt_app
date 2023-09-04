# Trial Balance Data Converter
Albert Lleida Estival, August 2023.

This is a Streamlit application designed to convert a specific format TXT file into CSV files. Additionally, it now includes a feature to filter the data based on specific account and subcuenta values.

## How the App Works
1. Launch the app.
2. Utilize the provided file uploader to upload a TXT file.
3. Click the "Convert" button to initiate the processing of the uploaded file.
   - If the TXT file adheres to the required pattern, it will be processed and transformed into CSV files.
   - The original data will be processed into a DataFrame, and a filtered version of the data will also be generated based on specified account and subcuenta values.
4. You can then download the resulting CSV files:
   - One containing the full data, named based on date information extracted from the TXT file.
   - Another containing the filtered data, named accordingly.

## App Workflow
The app starts with a title and a file uploader for TXT files. When the "Convert" button is clicked:

- The uploaded TXT file is read, and its data is parsed and processed into a DataFrame.
- The data is transformed and cleaned.
- Two CSV files are generated: one with the full data and another with filtered data.
- Temporary files are created to store the CSV files, which are available for download.

## Code Details
Noteworthy code adjustments and features include:

- Parsing and processing of TXT file data.
- Filtering data based on specific account and subcuenta values.
- Temporary file management for CSV file generation.

## Requirements
The app relies on the following Python libraries:

- Streamlit
- Pandas
- re
- tempfile
- os

## Limitations
Please keep in mind the following limitations:

- The app's file processing relies on regular expressions. Incorrect detection of the pattern might lead to failed conversions.
- Ensure you have sufficient available disk space and memory to accommodate the processing and creation of CSV files.
- The app provides the option to clean up temporary files, but ensure you have the necessary permissions and resources in place.

## Troubleshooting
For additional help or troubleshooting, refer to the Streamlit documentation or reach out to the app's developer.

Feel free to provide additional details or update the README further based on your specific needs.
