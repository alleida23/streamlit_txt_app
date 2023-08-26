# Trial Balance Data Converter
Albert Lleida Estival, August 2023. 

This is a simple Streamlit app that converts a specific format TXT file into a CSV file.

## How it Works

1. Run the app.
2. Upload a TXT file using the provided file uploader.
3. Click the "Convert" button to process the uploaded file.
4. If the TXT file has the correct pattern, it will be processed and converted into a CSV file.
5. The CSV file will be available for download with the name based on the date in the TXT file.

## Installation

To run the app locally, follow these steps:

1. Clone the repository:

   ```bash
   git clone https://github.com/your-username/your-repo.git

## App Workflow
The app begins with a title and a file uploader to upload the TXT file.

After uploading, click the "Convert" button to process the file.

If the file's pattern is recognized, the data is transformed into a DataFrame and then processed further.

New columns are created, filled, and formatted in the DataFrame.

The processed data is saved as a CSV file, which can be downloaded using the "Download CSV" button.

## Requirements
The app uses the following Python libraries:

Streamlit
Pandas
re

##Limitations
The app assumes that the uploaded TXT file follows a specific format. Make sure your file adheres to the required pattern.
The app processes files based on regular expressions. If the pattern is not detected correctly, the conversion might fail.
