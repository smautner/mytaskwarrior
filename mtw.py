from lmz import *
import storage 
import sys
import inputs 
import out 

############################
# ARGPARSE
##########################
help = '''
mtw q add  qname
mtw q rm qname
mtw qname add / rm / done  
'''


def exec_cmds(mystorage,args):

    if args[0] == 'q' and len(args) == 3:
        if args[1] == 'add':
            mystorage.addQ(args[2])
        elif args[1] == 'rm':
            mystorage.delQ(args[2])
        else:
            print("what do u what with q? rm / add (qname)")
            
            

    elif args[0] in mystorage.get_queues():
        # first arg is a quename, now we can work on that Q 
        if args [1] == 'add':
            name, due, interval = inputs.parse_new_task(args[2:])
            mystorage.addT(q=args[0] ,t = name, due=due, interval=interval)
            
        elif args [1] == 'rm' and len(args)==3:
            mystorage.delT(q=args[0],t=args[2])

        elif args [1] == 'done' and len(args) ==3 :
                mystorage.done(q=args[0], tname= args[2])
        else:
            print('add name [repeat] [due] rm [name] done [name]')

        
    else:
        print(help)


if __name__ == "__main__":
    
    mystorage = storage.storage('/home/ikea/projects/mtw.dmp','/home/ikea/projects/mtw.json')

    if len(sys.argv[1:]) > 0:
        exec_cmds(mystorage, sys.argv[1:])
        mystorage.save()

    out.show_prios(mystorage)

