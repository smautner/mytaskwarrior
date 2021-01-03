from lmz import *
import os 
import sys
import basics as ba
from rich.console import Console
from rich.table import Table
import time
import datetime as dt
##########################
# we need a storage object
##########################
class storage:

    def __init__(self, fname, fname_int):
        self.fname = fname
        if os.path.isfile(fname): 
            self.data  = ba.loadfile(fname) 
        else:
            self.data={}

        self.fname_int = fname_int
        if os.path.isfile(fname_int): 
            self.data_int  = ba.jloadfile(fname_int)
        else:
            self.data_int={} # q_t:interval

        '''
        for qname,qlist in self.data.items():
            # qlist is [taskdict]
            # a task dict has a name and an interval 
            for t in qlist:
                if t['interval'].days >0:
                    self.data_int[f"{qname}_{t['name']}"]= t['interval'].days
        '''



    def save(self):
        ba.dumpfile(self.data, self.fname) 
        ba.jdumpfile(self.data_int, self.fname_int)
   


    #################
    # QUEUES
    ##############
    def addQ(self,q): 
        if q in self.data:
            print("already exists")
        else:
            self.data[q]=[]
    def delQ(self,q): 
        self.data.pop(q)

    def get_queues(self):
        return self.data.keys()

    def srt_queue(self,q):
        self.data[q].sort(key=lambda x:(x['due'], self.data_int.get(f"{q}_{x[name]}",0)))

    ########
    #  tasks 
    ###########

    def delT(self,q='queue',t='task'): 
        self.data[q] =  Filter(lambda task: task['name']!=t, self.data[q])

    def addT(self,q='queue',t='task', due ='', interval= ''): 
        task = {'name':t,'due':due}
        interval = int(interval)
        if interval >0 :
            self.data_int[f"{q}_{t}"]  = interval
        self.data[q].append(task)
        self.srt_queue(q)

    def get_tasks(self,max=1000): 
        return [v[:max] for v in self.data.values()  ] # note: i should sort on insert

    def done(self,q,tname): 
        for i,t in enumerate(self.data[q]):
            if t['name'] == tname:
                break
        else:
            print (f"task {t} not in quque {q}")
            return
        
        interval = self.data_int.get(f"{q}_{tname}"  ,0)
        if interval == 0:
            self.data[q].remove(t)
        else:
            due=t['due']
            t['due'] =   today() + dt.timedelta(days = interval, hours= due.hour, minutes=due.minute)
            self.srt_queue(q)


# task: name, due, rep 
###########3
# READ TIME STGING 
###########
def today():
    now = dt.datetime.now()
    return dt.datetime(year=now.year,month=now.month,day= now.day)

def readdate(s): 
    now = dt.datetime.now()
    if s == 'now':
        return now
    if s == 'today':
        return today()
    # add zeros 
    y1,y2,m1,d1,d2=("0"*(5-len(s)))+s
    
    day = int(d1+d2)  
    mon = int('0x'+m1,0) 
    if mon == 0:
        mon=now.month
    year = int('20'+y1+y2) 
    year = year if year > 2000 else now.year

    return dt.datetime(year,mon,day)
    

def readhours(s):
    h,m = s[:2],s[2:]
    return dt.timedelta(hours = int(h), minutes= int(m))

def get_time(s):
    p = s.split()
    if len(p)==2:
        return readdate(p[0])+readhours(p[1])
    elif len(p) ==1:
        return readdate(p[0])
    else:
        print('cannot read p',p)
    

############################
# ARGPARSE
##########################
'''
mtw q add 
mtw q rm

mtw qname add / rm / done X 

mtw ls 
'''
def exec_cmds(mystorage):
    help = "options are: q(queue), any qeue name and ls "
    args = sys.argv[1:]
    if len(args) == 0:
        print (help)
    elif args[0] == 'q':
        if args[1] == 'add':
            mystorage.addQ(args[2])
        elif args[1] == 'rm':
            mystorage.delQ(args[2])
        else:
            print("what do u what with q? rm / add")

    elif args[0] in mystorage.get_queues():
        # first arg is a quename, now we can work on that Q 
        if args [1] == 'add':
            name, due, interval = parse_new_task(args)
            mystorage.addT(q=args[0] ,t = name, due=due, interval=interval)

        elif args [1] == 'rm':
            mystorage.delT(q=args[0],t=args[2])

        elif args [1] == 'done':
            if len(args)<=2:
                print("which task is done?")
            else:
                mystorage.done(q=args[0], tname= args[2])
        else:
            print('add[name][due][repeat] rm [name] done [name]')




    elif args[0] == 'ls':
        show_prios(mystorage)
    else:
        print(help)


def parse_new_task(args):
    if len(args) > 2:
        name = args[2]
    else:
        name = input('name: ')

    if len(args) > 3:
        interval = int(args[3])
    else:
        interval = int(input('interval in days: '))

    if len(args) > 4:
        due_raw = " ".join(args[4:])
    else:
        due_raw = input('due: yymDD hhmm :')

    due = get_time(due_raw)
    return name, due, interval


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

##################
# DO STUFF
#############

mystorage = storage('mytodolist','mydotolist_intervals')
exec_cmds(mystorage)
mystorage.save()


