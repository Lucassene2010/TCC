"""
processing data from an industry that has two workstations. 
This script is intended to refine the data for process mining.
for the TCC1 discipline.

Creater: lucas.gomes
Email: lucassene2010@gmail.com 

"""
from libs import log
import libs as DEF
import treatmentData as t

# Store list about the DataFrames from data base
DataFrames = []

def main():
    log.info("TCC Program, version:%s init",DEF.VERSION_SCRIPT)

    try:
        t.TreatmentDataFromSheets(DataFrames)

    except Exception as _e:
        log.error(str(_e))

if __name__ == "__main__":
    main()