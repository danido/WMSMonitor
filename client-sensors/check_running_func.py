#! /usr/bin/python
import os

def check_running(pname):
   stream = os.popen('ps auxwf | grep python | grep ' + pname + ' | grep -v grep')
   mypid = os.getpid()
   lines = stream.readlines()
   
#   print lines
   for line in lines:
     linesp = line.split()
     print line
     if len(linesp) >= 2:
        pid = linesp[1].strip().rstrip()
        #print pid, '   ', mypid
        if pid != str(mypid):
           return True
   return False
