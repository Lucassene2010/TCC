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

# Private functions

## 
# @brief Opens a file explorer for the user to select a spreadsheet.
# @return The selected file path.
#
def __OpenFileExplorer():
    _root = tk.Tk()
    _root.withdraw()

    _fileSelected = filedialog.askopenfilename()  # File name selected by the user
    if _fileSelected:
        log.info(f"Spreadsheet selected: {_fileSelected}")
    else:
        log.debug("No spreadsheet selected.")
    
    return _fileSelected

##
# @brief Prompts the user to select multiple spreadsheets until they input 'end'.
# @param DataFrames A list to store the selected dataframes.
#
def __SelectedDataFrameFiles(DataFrames):
    _i = 0
    while True:
        _i += 1
        _controlInput = input(f"Press ENTER to select spreadsheet {_i} or type 'end' to finish: ")
        if _controlInput != 'end':
            _file = __OpenFileExplorer()
            if _file:
                _df = pd.read_excel(_file)  # Read the selected spreadsheet
                DataFrames.append(_df)  # Append the dataframe to the list
                log.info(f"Spreadsheet {_i} loaded and added to DataFrames list.")
            else:
                log.debug(f"Spreadsheet {_i} selection was skipped.")
        else:
            log.info(f"Spreadsheet selection process ended after {_i-1} files.")
            return

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
            _sort_filter_by_ = input("Enter the column name for timestamp: ")
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
