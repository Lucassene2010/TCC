"""
processing data from an industry that has two workstations. 
This script is intended to refine the data for process mining.
for the TCC1 discipline.

Creater: lucas.gomes
Email: lucassene2010@gmail.com 

"""

from libs import pm4py
from libs import pd
import libs as DEF

def ProcessMining():
    
    df = pd.read_excel(DEF.NEW_SPREADSHEET_NAME + '.xlsx') 
    # Carregar o arquivo Excel
    log = pm4py.format_dataframe(df, case_id='ID da frequência',activity_key='descrição Estado',
                             timestamp_key='Timestamp')

    #pm4py.get_start_activities(log)

    #pm4py.get_end_activities(log)

    #pm4py.write_xes(log, 'running_example_csv_exported_as_xes.xes')

    map = pm4py.discover_heuristics_net(log)
    pm4py.view_heuristics_net(map)

    print(log.groupby("case:concept:name").last()["concept:name"].value_counts())

    pm4py.view_events_distribution_graph(log, distr_type="days_week")

    dfg = pm4py.discover_dfg(log)
    #print(dfg[0]) # graph structure

    pm4py.view_dfg(dfg[0], dfg[1], dfg[2])
    
    #process_tree = pm4py.discover_process_tree_inductive(log)
    #pm4py.view_process_tree(process_tree)

    #bpmn_model = pm4py.discover_bpmn_inductive(log)
    #pm4py.view_bpmn(bpmn_model)


