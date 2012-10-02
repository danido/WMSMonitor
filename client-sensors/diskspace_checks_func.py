#!/usr/bin/python

import os, sys


# Performs checks on disk space occupacy 
# Returns % of occupacy of disk partition hosting Sandbox directory and tmp directory 

def diskspace_checks(SANDBOX_PATH,TMP_PATH,VAR_LOG_PATH,VAR_LIB_MYSQL_PATH):
   '''diskspace_checks(SANDBOX_PATH,TMP_PATH,VAR_LOG_PATH,VAR_LIB_MYSQL_PATH) -> returns in output % of occupacy of partitions hosting 
      Jobs Sandbox directory and tmp directory'''

   if (os.access(SANDBOX_PATH,os.F_OK)==True):
      cmd = "df -h " + SANDBOX_PATH + "| tail -1"
      stdt = os.popen(cmd)
      std  =  stdt.readline() 
      sandbox =  std[std.find("%")-3:std.find("%")]
      stdt.close()   
   else:
      sandbox = None

   if (os.access(TMP_PATH,os.F_OK)==True):
      cmd = "df -h " + TMP_PATH + "| tail -1"
      stdt = os.popen(cmd)
      std  =  stdt.readline() 
      tmp =  std[std.find("%")-3:std.find("%")]
      stdt.close()
   else:
      tmp = None

   if (os.access(VAR_LOG_PATH,os.F_OK)==True):
      cmd = "df -h " + VAR_LOG_PATH + "| tail -1"
      stdt = os.popen(cmd)
      std  =  stdt.readline()
      varlog =  std[std.find("%")-3:std.find("%")]
      stdt.close()
   else:
      varlog = None

   if (os.access(VAR_LIB_MYSQL_PATH,os.F_OK)==True):
      cmd = "df -h " + VAR_LIB_MYSQL_PATH + "| tail -1"
      stdt = os.popen(cmd)
      std  =  stdt.readline()
      varlibmysql =  std[std.find("%")-3:std.find("%")]
      stdt.close()
   else:
      varlibmysql = None


   output=[]
   output.append(sandbox)
   output.append(tmp)
   output.append(varlog)
   output.append(varlibmysql)
   return output
