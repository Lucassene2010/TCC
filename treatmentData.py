"""
processing data from an industry that has two workstations. 
This script is intended to refine the data for process mining.
for the TCC1 discipline.

Creator: lucas.gomes
Email: lucassene2010@gmail.com 
"""

# Libraries
from libs import tk
from libs import filedialog
from libs import pd
from libs import log
import libs as DEF

##
# @brief Opens a file explorer for the user to select one or more spreadsheets.
# @return A list of selected file paths.
#
def __OpenFileExplorer():
    _root = tk.Tk()
    _root.withdraw()  # Hide the Tkinter root window

    # Let the user select multiple files
    _filesSelected = filedialog.askopenfilenames(
        title="Select Excel files",
        filetypes=[("Excel files", "*.xlsx *.xls")]
    )

    if _filesSelected:
        log.info(f"Spreadsheets selected: {_filesSelected}")
    else:
        log.debug("No spreadsheets selected.")
    
    return _filesSelected  # Return a tuple of file paths

##
# @brief Prompts the user to select multiple spreadsheets and appends them to DataFrames.
# @param DataFrames A list to store the selected dataframes.
#
def __SelectedDataFrameFiles(DataFrames):
    # Call the file explorer to select multiple files
    _files = __OpenFileExplorer()
    
    if _files:
        for _file in _files:
            try:
                _df = pd.read_excel(_file)  # Read each selected spreadsheet
                DataFrames.append(_df)  # Append the dataframe to the list
                log.info(f"Spreadsheet '{_file}' loaded and added to DataFrames list.")
            except Exception as e:
                log.error(f"Failed to load spreadsheet '{_file}': {str(e)}")
    else:
        log.debug("No spreadsheets were selected.")


##
# @brief Converts date format from dd/mm/yyyy HH:MM:SS to mm/dd/yyyy HH:MM:SS.
# @param data The date string to convert.
# @return The converted date string.
#
def __data_format_converter(data):
    return pd.to_datetime(data, format='%d/%m/%Y %H:%M:%S').strftime('%m/%d/%Y %H:%M:%S')

##
# @brief Converts the spreadsheet to a .txt file with specific columns.
# @param txt_file_path The path where the .txt file will be saved.
#
def __ConvertExcelToTxt(txt_file_path):
    df = pd.read_excel(DEF.NEW_SPREADSHEET_NAME + '.xlsx')

    # Select necessary columns and save as .txt
    df[['ID da frequência', 'Timestamp', 'descrição Estado']].to_csv(
        txt_file_path, sep=',', index=False, header=['case_id', 'timestamp', 'activity']
    )
    log.info(f"Log saved as {txt_file_path}")

##
# @brief Concatenates and processes multiple dataframes, applying sorting, timestamp formatting, and filling missing case IDs.
# @param DataFrames A list of dataframes to concatenate.
#
def __AppendDataFrame(DataFrames):
    if DataFrames:
        try:
            # Concatenate all the dataframes selected by the user
            _df_concatenated = pd.concat(DataFrames)
            log.debug(f"DataFrames concatenated. Number of rows: {_df_concatenated.shape[0]}")
            
            # User input for the column name containing the timestamps
            _sort_filter_by_ = DEF.TIMESTAMP_COLUMM_NAME
            log.debug(f"Sorting dataframe by column: {_sort_filter_by_}")
            
            # Sort concatenated dataframe by the timestamp column
            _df_concatenated_order = _df_concatenated.sort_values(by=_sort_filter_by_)
            log.info("Spreadsheet ordered by timestamp and concatenated.")

            # Saving the new dataframe to a new spreadsheet
            _df_concatenated_order.to_excel(DEF.NEW_SPREADSHEET_NAME + '.xlsx', index=False)
            log.info(f"New spreadsheet '{DEF.NEW_SPREADSHEET_NAME}.xlsx' created successfully.")

            # Open the newly saved spreadsheet for further processing
            df = pd.read_excel(DEF.NEW_SPREADSHEET_NAME + '.xlsx')  
            
            # Apply the date format conversion to the 'Horário do servidor' column and create a new 'Timestamp' column
            df['Timestamp'] = df['Horário do servidor'].apply(__data_format_converter)
            log.debug("Timestamp column created with correct format.")

            # Fill blank cells in the 'ID da frequência' column with the value from the next valid cell
            df['ID da frequência'] = df['ID da frequência'].bfill()
            log.debug("'ID da frequência' column backfilled.")

            # Save the spreadsheet with the updated data
            df.to_excel(DEF.NEW_SPREADSHEET_NAME + '.xlsx', index=False)
            log.info(f"Spreadsheet '{DEF.NEW_SPREADSHEET_NAME}.xlsx' saved with updated data.")
        
        except Exception as _e:
            log.error(f"Error during dataframe processing: {str(_e)}")

    else:
        log.error("No dataframes were provided for processing.")

# Public functions

##
# @brief Main function to process and treat data from selected spreadsheets.
# @param DataFrames A list to store the dataframes from selected files.
#
def TreatmentDataFromSheets(DataFrames):
    log.info("Starting the process of treating data from spreadsheets.")
    __SelectedDataFrameFiles(DataFrames)  # Let the user select multiple spreadsheets
    log.debug(f"{len(DataFrames)} dataframes selected by the user.")
    __AppendDataFrame(DataFrames)  # Process and concatenate the selected dataframes
    log.info("Data treatment process completed.")
