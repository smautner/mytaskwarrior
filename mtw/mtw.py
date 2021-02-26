from lmz import *
import mtw.storage  as storage
import sys
import mtw.inputs  as inputs 
import mtw.out  as out

############################
# ARGPARSE
##########################
help = '''
qname add tname duedate [hhmm] [interval]
qname rm tname 
qname done tname 
qname mv tname duedate [hhmm] [inteval] 
--> in any case print table
'''


def exec_cmds(mystorage,args):
    qname = args[0]
    command = args[1]
    tname = args[2]
    rest = args[3:]
    
    

    if command == 'rm':
        mystorage.delT(q=qname,t=tname)
        
    elif command == 'done':
        mystorage.done(q=qname, tname= tname)
    
    elif command == 'add':
        due, interval = inputs.parse_new_task(rest)
        mystorage.addT(q=qname ,t = tname, due=due, interval=interval)
        
    elif command == 'mv':
        mystorage.delT(q=qname,t=tname)
        due, interval = inputs.parse_new_task(rest)
        mystorage.addT(q=qname ,t = tname, due=due, interval=interval)
    else:
        print(help)
    




def main():
    mystorage = storage.storage('/home/ikea/projects/mtw.dmp','/home/ikea/projects/mtw.json')

    if len(sys.argv[1:]) > 0:
        exec_cmds(mystorage, sys.argv[1:])
        mystorage.save()

    out.show_prios(mystorage)

if __name__ == "__main__":
    main()
