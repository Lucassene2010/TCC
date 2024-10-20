"""
processing data from an industry that has two workstations. 
This script is intended to refine the data for process mining.
for the TCC1 discipline.

Creater: lucas.gomes
Email: lucassene2010@gmail.com 

"""
#Libraries
from libs import tk
from libs import filedialog
from libs import pd
from libs import log
import libs as DEF

#Private functions
def __OpenFileExplorer():

    _root = tk.Tk()
    _root.withdraw()  # Hidden main window

    _fileSelected = filedialog.askopenfilename() # File name selected
    log.debug("Open the spreadsheet: " + _fileSelected)
    return _fileSelected

def __SelectedDataFrameFiles(DataFrames):
    # Loop for the user selects the spreadsheets
    _i = 0
    while True:
        _i += 1
        _controlInput = input("inputing ENTER key to select a spreadsheet" + 
                              str(_i) + "and texting 'end' to finish: ")
        if('end' != _controlInput):
            _file = __OpenFileExplorer()
            if not _file:
                log.debug("_file is None")
                break
            _df = pd.read_excel(_file)
            DataFrames.append(_df)
        else:
            return

# Função para converter o formato de data
def __data_format_converter(data):
    return pd.to_datetime(data, format='%d/%m/%Y %H:%M:%S').strftime('%m/%d/%Y %H:%M:%S')

def __ConvertExcelToTxt(txt_file_path):
    df = pd.read_excel(DEF.NEW_SPREADSHEET_NAME + '.xlsx')

    # Selecionar as colunas necessárias e salvar no formato .txt
    df[['ID da frequência', 'Timestamp', 'descrição Estado']].to_csv(
        txt_file_path, sep=',', index=False, header=['case_id', 'timestamp', 'activity']
    )
    log.info(f"Log saved as {txt_file_path}")

def __AppendDataFrame(DataFrames):

    if DataFrames:
        try:
            _df_concatenated = pd.concat(DataFrames)
            _sort_filter_by_ = input("texting the columm name from timestamp: ")
            _df_concatenated_order = _df_concatenated.sort_values(by=_sort_filter_by_)
            log.info("spreadsheet in order and concatenated.")

            # Saving the new dataframe in new spreadsheet
            _df_concatenated_order.to_excel(DEF.NEW_SPREADSHEET_NAME + '.xlsx', index=False)
            log.debug(f"spreadsheet '{DEF.NEW_SPREADSHEET_NAME}.xlsx' created with sucess.")

            # Aplicar a função para criar a nova coluna 'Timestamp'
            df = pd.read_excel(DEF.NEW_SPREADSHEET_NAME + '.xlsx')  
            
            # Altere o nome do arquivo conforme necessário
            df['Timestamp'] = df['Horário do servidor'].apply(__data_format_converter)

            # Preencher células vazias na coluna 'ID da frequência' com a próxima célula preenchida
            df['ID da frequência'] = df['ID da frequência'].bfill()

            # Salvar a planilha com as alterações
            df.to_excel(DEF.NEW_SPREADSHEET_NAME + '.xlsx', index=False)
        
        except Exception as _e:
            log.error(str(_e))

    else:
        log.error("DataFrames is None.")

#Public functions
def TreatmentDataFromSheets(DataFrames):
    __SelectedDataFrameFiles(DataFrames)
    __AppendDataFrame(DataFrames)
