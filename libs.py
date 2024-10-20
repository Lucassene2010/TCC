# Libraries
import logging as log  # Standard Python logging for event logging
import tkinter as tk  # Tkinter for GUI elements (used for file selection)
from tkinter import filedialog  # Tkinter filedialog for opening files
import pandas as pd  # Pandas for data manipulation and analysis
import pm4py  # PM4Py for process mining
from pm4py.objects.log.util import dataframe_utils  # Utility functions for handling dataframes in pm4py
from pm4py.objects.conversion.log import converter as log_converter  # Converts logs into event logs for process mining
from pm4py.algo.discovery.alpha import algorithm as alpha_miner  # Alpha miner for process discovery

# Script version
VERSION_SCRIPT = "v0.0.0.3"

# Configure logging to display information messages
log.basicConfig(level=log.INFO)

# Constant for naming the new spreadsheet after concatenation and sorting
NEW_SPREADSHEET_NAME = "concAndSortDataFrame"
