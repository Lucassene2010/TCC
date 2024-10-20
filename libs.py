import logging as log
import tkinter as tk
from tkinter import filedialog
import pandas as pd
import pm4py
from pm4py.objects.log.util import dataframe_utils
from pm4py.objects.conversion.log import converter as log_converter
from pm4py.algo.discovery.alpha import algorithm as alpha_miner

VERSION_SCRIPT = "v0.0.0.2"
log.basicConfig(level=log.INFO)

NEW_SPREADSHEET_NAME = "concAndSortDataFrame"