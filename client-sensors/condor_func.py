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

   #two condor version cases: condor <7.8 or condor >=7.8
   if  (os.access("/opt/condor-c/bin/condor_q",os.F_OK) == True):
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
       else:
          condor_list = [None,None,None,None]
        
       
   elif (os.access("/usr/bin/condor_q",os.F_OK) == True):
       cmd = "/usr/bin/condor_q 2>/dev/null | tail -1"
       std = os.popen(cmd)
       stdstr =  std.readlines()   #stdstr is a list of strings, if everything is ok condor_q output is in 0 position
       # if everything is ok....
       if ( len(stdstr) > 0 ) :
          strlist = stdstr[0].split()
          if (strlist[1] == 'jobs;') and (strlist[7] == 'idle,'):
             condor_list = [strlist[0],strlist[6],strlist[8],strlist[10]]
          else:
             condor_list = [None,None,None,None]
       else:
          condor_list = [None,None,None,None]
       
   else:
       condor_list = [None,None,None,None]
  
   return condor_list
