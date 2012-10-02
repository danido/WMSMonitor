#!/usr/bin/python

import os, sys

### Average load (in the last 15 minutes)
def load_cpu():
   ''' load_cpu() -> average cpu load in past 15 minutes
       Returns a float'''
   
   try:
       file = open('/proc/loadavg','r')
       loadstr = file.readline()
       loadstr = loadstr.split()
       load = loadstr[2]
       file.close()
   except IOError:
       load = None

   return load
