#!/usr/bin/python

import os, sys


def condor_jobs(ENV_FILE):
   ''' condor_jobs(ENV_FILE) -> list of jobs handled by condor
       Function to return the number of jobs handled by condor
       Parses the last line of the condor_q output
       It needs the condor path to be correctly set on the WMS
       Returns a list with total, idle, running, held number of jobs
       or a list of None if fails'''



   env_script = ENV_FILE


   #if  (os.access("/opt/glite/etc/profile.d/grid-env.sh",os.F_OK) == True):
   #   env_script = "/opt/glite/etc/profile.d/grid-env.sh"
   #else:
   #   env_script = "/etc/glite/profile.d/glite_setenv.sh"
   
   cmd = ". " + env_script + "; /opt/condor-c/bin/condor_q 2>/dev/null | tail -1"
   std = os.popen(cmd)
   stdstr =  std.readlines()   #stdstr is a list of strings, if everything is ok condor_q output is in 0 position
   # if everything is ok....
   if ( len(stdstr) > 0 ) :   
      strlist = stdstr[0].split()
      if (strlist[1] == 'jobs;') and (strlist[3] == 'idle,'):
         condor_list = [strlist[0],strlist[2],strlist[4],strlist[6]]
      else:
         condor_list = [None,None,None,None]
#         print 'Unable to fetch condor jobs'
   else:
      condor_list = [None,None,None,None]
#      print 'Unable to fetch condor jobs'
  
   return condor_list
