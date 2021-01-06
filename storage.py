import basics as ba
import os 
from lmz import *
import datetime as dt

# tasks.due:
# gets iso-string as input when adding task
# will return datetime object 

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
        self.data[q].sort(key=lambda x:(x['due'], self.data_int.get(f"{q}_{x['name']}",0)))

    ########
    #  tasks 
    ###########

    def delT(self,q='queue',t='task'): 
        self.data[q] =  Filter(lambda task: task['name']!=t, self.data[q])

    def addT(self,q='queue',t='task', due ='', interval= ''):
        due = dt.datetime.fromisoformat(due) 
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
            now = dt.datetime.now()
            today = dt.datetime(year=now.year,month=now.month,day= now.day)
            t['due'] =   today + dt.timedelta(days = interval, hours= due.hour, minutes=due.minute)
            self.srt_queue(q)
