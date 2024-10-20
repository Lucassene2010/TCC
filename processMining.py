"""
Processing data from an industry that has two workstations. 
This script is intended to refine the data for process mining.
for the TCC1 discipline.

Creator: lucas.gomes
Email: lucassene2010@gmail.com 
"""

# Libraries
from libs import pm4py  # Process Mining library
from libs import pd  # Pandas for data manipulation
from libs import log  # Logging functionality
import libs as DEF  # Importing other dependencies and constants

##
# @brief Performs process mining on an industry dataset using pm4py library.
#
def ProcessMining():
    try:
        # Load the Excel file containing the refined data
        log.info(f"Loading the refined spreadsheet from '{DEF.NEW_SPREADSHEET_NAME}.xlsx'.")
        df = pd.read_excel(DEF.NEW_SPREADSHEET_NAME + '.xlsx') 
        log.debug("Spreadsheet loaded successfully.")

        # Format the dataframe for pm4py process mining, setting the case ID, activity key, and timestamp
        log.info("Formatting dataframe for process mining.")
        event_log = pm4py.format_dataframe(df, case_id='ID da frequência', 
                                           activity_key='descrição Estado', 
                                           timestamp_key='Timestamp')
        log.debug("Dataframe formatted for process mining.")

        # Uncomment these lines for additional process mining functionalities:
        # pm4py.get_start_activities(event_log)  # To get the starting activities of cases
        # pm4py.get_end_activities(event_log)  # To get the ending activities of cases
        # pm4py.write_xes(event_log, 'running_example_csv_exported_as_xes.xes')  # Export log in XES format

        # Discover a heuristic net from the event log
        log.info("Discovering heuristic net from the event log.")
        heuristic_net = pm4py.discover_heuristics_net(event_log)
        log.debug("Heuristic net discovered.")

        # Visualize the discovered heuristic net
        log.info("Visualizing the heuristic net.")
        pm4py.view_heuristics_net(heuristic_net)

        # Print the last activity of each case and its occurrence count
        log.info("Displaying the last activity of each case and occurrence count.")
        print(event_log.groupby("case:concept:name").last()["concept:name"].value_counts())

        # View events distribution by day of the week
        log.info("Visualizing event distribution by day of the week.")
        pm4py.view_events_distribution_graph(event_log, distr_type="days_week")

        # Discover a Directly-Follows Graph (DFG) from the event log
        log.info("Discovering Directly-Follows Graph (DFG) from the event log.")
        dfg = pm4py.discover_dfg(event_log)
        log.debug("DFG discovered.")

        # Visualize the Directly-Follows Graph (DFG)
        log.info("Visualizing the Directly-Follows Graph (DFG).")
        pm4py.view_dfg(dfg[0], dfg[1], dfg[2])

        # Uncomment these lines to use other process discovery techniques:
        # Discover and visualize a process tree using inductive mining
        # log.info("Discovering and visualizing a process tree using inductive mining.")
        # process_tree = pm4py.discover_process_tree_inductive(event_log)
        # pm4py.view_process_tree(process_tree)

        # Discover and visualize a BPMN model using inductive mining
        # log.info("Discovering and visualizing a BPMN model using inductive mining.")
        # bpmn_model = pm4py.discover_bpmn_inductive(event_log)
        # pm4py.view_bpmn(bpmn_model)

    except Exception as _e:
        # Log any errors that occur during the process mining
        log.error(f"An error occurred during process mining: {_e}")
