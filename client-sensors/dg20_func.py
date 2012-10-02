#!/usr/bin/python

import os, sys, logging


# Function to return the number of unprocessed dg20logd files in /var/tmp/
# Parses the output of ls 
# The path for dg20logd files is hardcoded here
# Returns an integer on success None on failure

def dg20log(DG20_PATH) :
   ''' dg20log(DG20_PATH) -> integer on success, None on failures
       Function to return the number of unprocessed dg20logd files in /var/tmp/
       Parses the output of ls
       The path for dg20logd files is hardcoded here
       Returns an integer on success None on failure'''

   logger = logging.getLogger('dg20')

   if (  os.access(DG20_PATH,os.F_OK)==False):
      logger.error('Error: dg20log directory does not exist ( ' + DG20_PATH + ')')
      count = None
   else:   
#      cmd = 'ls -1 ' + DG20_PATH
      cmd = 'ls -1 ' + DG20_PATH + '/glite-lbproxy-ilog_events.* |grep -v ".stat"| grep -v ".ctl" |wc -l'
      lsstr = os.popen(cmd)
      ls = lsstr.readlines()
      count = int(ls[0].strip())
   return count 
