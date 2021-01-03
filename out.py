from rich.console import Console
from rich.table import Table
from lmz import *
import datetime as dt
#####################
# pretty printing 
####################
def format_event(task): 
    #a task is a dict with due date and name
    #depending on the due data there is another color :)
    if len(task)==0:
        return ''
    else:
        now = dt.datetime.now()
        days = (task['due']-now).days
        if days < 0:
            color = 'red'
        elif days < 1:
            color = 'yellow'
        else:
            color = 'green'
        if task['due'].hour == 0 and task['due'].minute == 0:
            due_str = task['due'].strftime('%b %d')
        else:
            due_str = task['due'].strftime('%b %d %H%M')

        return f"[{color}]{task['name']} {due_str}[/{color}]"

def filltranspose(stuff, fill = {}):
    maxitems = max( len(x) for x in stuff  )
    for lis in stuff:
        lis+=[fill]*(maxitems-len(lis))
    return Transpose(stuff)
    

def show_prios(mystorage): 
    # print table and header
    console = Console()
    table = Table(show_header=True, header_style="bold magenta")
    for qname in mystorage.get_queues():    
        table.add_column(qname)
    
    tasks = mystorage.get_tasks(max=10)
    tasks = filltranspose(tasks)
    for taskrow in tasks: 
        table.add_row(*[format_event(task) for task in taskrow])

    console.print(table)
