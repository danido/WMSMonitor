#!/usr/bin/python

import os, sys

def daemons_status(SCRIPT_PATH,ENV_FILE):
   ''' daemons_status(SCRIPT_PATH,ENV_FILE) -> checks the status of gLite daemons
       Returns a list of error code, with 0 for OK and >0 for errors
       for following daemons: 
       glite-lb-bkserverd,glite-lb-locallogger'''
   
   service_list=['glite-lb-bkserverd','glite-lb-locallogger','ntpd']
   status=[]
   SCRIPT_PATH = SCRIPT_PATH + '/'

   env_script = ENV_FILE

   for service in service_list:

      if (os.access(SCRIPT_PATH + service,os.F_OK)==True):
         cmd = '. ' + env_script + '; ' + SCRIPT_PATH + service + " status >/dev/null 2>&1"
         status.append(os.system(cmd))
      else:
          status.append(None)

   return status
