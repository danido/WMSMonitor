#!/usr/bin/python

import os, sys


# Function to return the number of jobs in input.fl, queue.fl and ice.fl (or equivalent jobdirs) 
# Returns 3 integers 

def filelists(ENV_FILE):
   '''filelists((INPUT_FILE,QUEUE_FILE,ENV_FILE) -> returns in output the number of jobs in 
      input.fl and queue.fl'''

   #stri = os.popen(". " + ENV_FILE + "; echo $GLITE_WMS_CONFIG_DIR")
   #GLITE_WMS_CONFIG_DIR = stri.readline()
   #stri.close()
   #WMSCONF_FILE= GLITE_LOCATION.strip() + '/glite_wms.conf'

   stri = os.popen(". " + ENV_FILE + "; echo $GLITE_WMS_LOCATION_VAR")
   VAR_LOCATION = stri.readline()
   stri.close()
   
   # Trying to get inputfl, first with input.fl file then with jobdir
  
   if (os.access(VAR_LOCATION.strip() + '/workload_manager/jobdir/new',os.F_OK)==True):
      cmd = "ls -1 " + VAR_LOCATION.strip() + "/workload_manager/jobdir/new | wc -l" 
      std = os.popen(cmd)
      inputfl =  int(std.readline())
      cmd = "ls -1 " + VAR_LOCATION.strip() + "/workload_manager/jobdir/old | wc -l"
      std = os.popen(cmd)
      inputfl =  inputfl + int(std.readline())
      inputfl = str(inputfl) + ' '
      std.close()   
   else:
      inputfl = None

   # Trying to get queuefl, first with queue.fl file then with jobdir
   if (os.access(VAR_LOCATION.strip() + '/jobcontrol/jobdir/new',os.F_OK)==True):
      cmd = "ls -1 " + VAR_LOCATION.strip() + "/jobcontrol/jobdir/new |wc -l"
      std = os.popen(cmd)
      queuefl =  int(std.readline())
      cmd = "ls -1 " + VAR_LOCATION.strip() + "/jobcontrol/jobdir/old |wc -l"
      std = os.popen(cmd)
      queuefl =  queuefl + int(std.readline())
      queuefl = str(queuefl) + ' '
      std.close()
   else:
      queuefl = None


   # Trying to get icefl, first with ice.fl file then with jobdir
   if (os.access(VAR_LOCATION.strip() + '/ice/jobdir/new',os.F_OK)==True):
      cmd = "ls -1 " + VAR_LOCATION.strip() + "/ice/jobdir/new |wc -l"
      std = os.popen(cmd)
      icefl =  int(std.readline())
      cmd = "ls -1 " + VAR_LOCATION.strip() + "/ice/jobdir/old |wc -l"
      std = os.popen(cmd)
      icefl =  icefl + int(std.readline())
      icefl = str(icefl) + ' '
      std.close()
   else:
      icefl = None

   filelists=[]
   filelists.append(inputfl)
   filelists.append(queuefl)
   filelists.append(icefl)

   return filelists
