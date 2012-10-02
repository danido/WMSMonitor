#!/usr/bin/python

import os, sys

def gftp_num():
   '''gftp_num() -> returns in output the number of gridftp sessions'''

   cmd = "netstat -tapn | grep -c 2811"
   stdt = os.popen(cmd)
   std = stdt.readline()
   std=std[0:len(std)-1]
   stdt.close()
   if std.isdigit():
      output = std
   else:
      output = None
   
   return output
