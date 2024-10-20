"""
Processing data from an industry that has two workstations. 
This script is intended to refine the data for process mining.
for the TCC1 discipline.

Creator: lucas.gomes
Email: lucassene2010@gmail.com 
"""

# Importing the required libraries and modules
from libs import log  # Logging functionality
import libs as DEF  # Custom library for constants and configurations
import treatmentData as t  # Module for handling data refinement and treatment
import processMining as p  # Module for process mining operations

# Store a list to hold the DataFrames from the database
DataFrames = []

##
# @brief Main function that coordinates data treatment and process mining.
#
# This function first processes the data by calling `TreatmentDataFromSheets`, 
# and then performs process mining using the `ProcessMining` function.
#
def main():
    # Log the initialization of the program with the current version
    log.info("TCC Program, version: %s initializing", DEF.VERSION_SCRIPT)
    
    try:
        # Log the start of data treatment process
        log.info("Starting data treatment process.")
        t.TreatmentDataFromSheets(DataFrames)  # Handle data treatment from spreadsheets
        
        # Log the completion of data treatment process
        log.info("Data treatment process completed. Number of DataFrames processed: %d", len(DataFrames))
        
        # Log the start of process mining analysis
        log.info("Starting process mining analysis.")
        p.ProcessMining()  # Perform process mining on the refined data
        
        # Log the completion of process mining analysis
        log.info("Process mining analysis completed successfully.")
    
    except Exception as _e:
        # Log any errors that occur during the execution with detailed exception info
        log.error("An error occurred during execution: %s", str(_e))

##
# @brief Entry point of the program.
#
# When this script is executed, it runs the `main()` function.
#
if __name__ == "__main__":
    main()
