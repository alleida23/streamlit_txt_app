# Trial Balance Data Converter
Albert Lleida Estival, August 2023.

This is a straightforward Streamlit application that converts a specific format TXT file into an Excel (xlsx) file.

## How the App Works

1. Launch the app.
2. Utilize the provided file uploader to upload a TXT file.
3. Click the "Convert" button to initiate the processing of the uploaded file.
4. If the TXT file adheres to the required pattern, it will be processed and transformed into an Excel (xlsx) file.
5. You can then download the resulting Excel (xlsx) file, which will be named based on the date information extracted from the TXT file.

## App Workflow
The app begins with a title and a file uploader designed for uploading TXT files.

After selecting a file, simply click the "Convert" button to set the processing in motion.

When the file follows the recognized pattern, its data is transformed into a DataFrame and subsequently subjected to further processing.

During this processing, new columns are generated, populated, and formatted within the DataFrame.

The processed data is eventually saved as an Excel (xlsx) file. You can access this file using the "Download Excel (xlsx)" button.

## Code Details
Noteworthy code adjustments include:

- Integration of the function cleanup_temp_file() to handle the removal of temporary Excel (xlsx) files once they are no longer required.
- Clearing the memory of the uploaded TXT file's content via del content, a step that helps conserve system resources.
- Dynamic generation of Excel (xlsx) file names, using the date pattern extracted from the TXT content, when the user opts to download the file.

## Requirements
The app relies on the following Python libraries:

  - Streamlit
  - Pandas
  - re
  - tempfile
  - os

## Limitations
It's vital that any TXT files you intend to convert adhere to the specified format. Please ensure your files conform to this required pattern.

The app's file processing hinges on regular expressions. Incorrect detection of the pattern might lead to failed conversions.

Be certain you have sufficient available disk space and memory to accommodate the processing and creation of Excel (xlsx) files.

Remember that while the app takes care of temporary file management during conversion, it's important to have the necessary permissions and resources in place.

For additional help or troubleshooting, refer to the Streamlit documentation or reach out to the app's developer.
