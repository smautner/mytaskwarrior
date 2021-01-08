import datetime as dt



def parse_new_task(args):
	#datetime.fromisoformat('2011-11-04 00:05') <- this will work so we return this as date

    name = args[0] # <- so this is easy.. 

    # get hours: either last arg is hhmm or we assume 2359
    if len(args[-1]) == 4:
        hours = _readhours(args.pop())
    else:
        hours = dt.timedelta(hours =23, minutes=59)
        
    # get date, since we popped the hour(if it existed) we know that the date is next
    date = _readdate(args.pop())

    interval = 0 if len(args) == 1 else int(args[1]) # if len is 1 there is only "name"

    return name,date.isoformat(),interval
	




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
