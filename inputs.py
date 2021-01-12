import datetime as dt



def parse_new_task(args):
    '''
    in: 
       due [hhmm] [interval]
    
    out: 
       datetime.fromisoformat('2011-11-04 00:05') and interval
    '''
	

    date= _readdate(args[0]) 
    
 
    
    hours = dt.timedelta(hours =23, minutes=59)
    interval = 0


    for e in args[1:]:
        if len(e) == 4:
            hours = _readhours(args.pop())
        else:
            interval = int(e) 

    return (date+hours).isoformat(),interval
	




# this is easy:
def _readhours(s):
    h,m =  s[:2],s[2:]
    return dt.timedelta(hours = int(h), minutes= int(m))



def _readdate(s): 
    now = dt.datetime.now()
   
    if s == 'now':
        ret = now
    elif s == 'today':
        ret = dt.datetime(year=now.year,month=now.month,day= now.day)
        
        
    # add zeros 
    y1,y2,m1,d1,d2=("0"*(5-len(s)))+s
    
    day = int(d1+d2)
     
    mon = int('0x'+m1,0) 
    if mon == 0:
        mon=now.month
        
    year = int('20'+y1+y2) 
    year = year if year > 2000 else now.year

    ret = dt.datetime(year,mon,day)
    
    return ret
