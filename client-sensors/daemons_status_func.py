#!/usr/bin/python

import os, sys

def daemons_status(GLITE_DAEMONS_PATH):
   ''' daemons_status() -> checks the status of gLite daemons
       Returns a list of error code, with 0 for OK and >0 for errors
       for following daemons: 
       glite-lb-locallogger,glite-lb-proxy
       glite-proxy-renewald,glite-wms-ftpd (globus-gridftp in SL4),glite-wms-jc
       glite-wms-lm,glite-wmsi-wm,glite-wms-wmproxy,glite-wms-ice,bdii'''
     
   GLITE_DAEMONS_PATH = GLITE_DAEMONS_PATH + '/'
   service_list=['glite-lb-locallogger','glite-lb-proxy','glite-proxy-renewald','globus-gridftp','glite-wms-jc','glite-wms-lm','glite-wms-wm','glite-wms-wmproxy','glite-wms-ice','bdii','ntpd'] 
   #trying to find OS system version and updating service list in case

   status=[]
   for service in service_list:
      if (service=='glite-lb-proxy') or (service=='glite-lb-locallogger'):
         status.append('0')
         continue
      if (os.access(GLITE_DAEMONS_PATH + service,os.F_OK)==True):
         cmd = GLITE_DAEMONS_PATH + '/' + service + " status >/dev/null 2>&1"
         status.append(os.system(cmd))
      elif (os.access('/etc/init.d/' + service,os.F_OK)==True):
	 cmd = '/etc/init.d/' + service + " status >/dev/null 2>&1"
	 status.append(os.system(cmd))
      else:
         status.append(None)

   print status
   return status
