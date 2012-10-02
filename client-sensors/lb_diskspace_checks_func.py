#!/usr/bin/python

import os, sys


# Performs checks on disk space occupacy 
# Returns % of occupacy of disk partition hosting Sandbox directory and tmp directory 

def diskspace_checks(LB_DISC_PATH,LB_DISC_LIB_MYSQL_PATH):
   '''diskspace_checks(LB_DISC_PATH,LB_DISC_LIB_MYSQL_PATH) -> returns in output % of occupacy of / partition '''

   if (os.access(LB_DISC_PATH,os.F_OK)==True):
      cmd = "df -h " + LB_DISC_PATH + "| tail -1"
      stdt = os.popen(cmd)
      std  =  stdt.readline() 
      occupancy =  std[std.find("%")-3:std.find("%")]
      stdt.close()   
   else:
      occupancy = None

   if (os.access(LB_DISC_LIB_MYSQL_PATH,os.F_OK)==True):
      cmd = "df -h " + LB_DISC_LIB_MYSQL_PATH + "| tail -1"
      stdt = os.popen(cmd)
      std  =  stdt.readline()
      libmysql =  std[std.find("%")-3:std.find("%")]
      stdt.close()
   else:
      libmysql = None

   output = []
   output.append(occupancy)
   output.append(libmysql)


   return output
