#!/usr/bin/python
import os, sys

def lb_connections():
   ''' lb_connections() -> number of connections established by lb server
       Returns an integer or a None '''
   
   cmd = "/usr/sbin/lsof -i :9000 -i :9001 -i :9003 |grep -v COMMAND |grep -v -c LISTEN "
   std = os.popen(cmd)
   stdstr =  std.readlines()   #stdstr is a list of strings, if everything is ok condor_q output is in 0 position
   # if everything is ok....
   if ( len(stdstr) > 0 ) :   
      strlist = stdstr[0].split()
      established_connections = strlist[0]
   else:
      established_connections = None      
  
   return established_connections 
