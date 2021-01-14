i  auto add/del the queues;  so the usage is 

```
qname add tname duedate [hhmm] [interval]
qname rm tname duedate
qname done tname duedate
```

in any case we output the table


i could switch to docopt... would look like this: 
```
Usage:
    mtw.py <qname> (rm|done) <tname>
    mtw.py <qname> add <tname> <date> [INTHHMM ...]
```
