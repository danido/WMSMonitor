#!/usr/bin/python

import os, sys

def file_desc(FD_WMS_WM,FD_WMS_LM,FD_WMS_JC,FD_WMS_LBINTERLOG) :
   ''' file_desc(FD_WMS_WM,FD_WMS_LM,FD_WMS_JC,FD_WMS_LBINTERLOG) -> list of integer or an empty list
       Function to return the number of file descriptors openedby the wms daemons
       Parses the output of ps and uses the lsof of the related process ID
       Returns a list of integer (None on failures) with the following order:
       WM,LM,JC,LL '''

   output = []
   EXE_list = []
   EXE_list.append(FD_WMS_WM)
   EXE_list.append(FD_WMS_LM)
   EXE_list.append(FD_WMS_JC)
   EXE_list.append(FD_WMS_LBINTERLOG)

   for i in range(0,len(EXE_list)):
      EXE_NAME = EXE_list[i]
      cmd = "ps auxwww | grep " + EXE_NAME + " | grep -v grep | awk '{ print $2 }'"
      FD_stream = os.popen(cmd)
      pid_tmp = FD_stream.readline()
      if len(pid_tmp) > 0 :
         pid_tmp = pid_tmp[0:len(pid_tmp) - 1]
      FD_stream.close()
      if pid_tmp.isdigit():
         pid = pid_tmp
         cmd = "/usr/sbin/lsof -p " + pid + " | tail -1 | awk '{ print $4 }' | sed 's/.$//'"
         FD_stream = os.popen(cmd)
         fd_tmp = FD_stream.readline()
         if len(fd_tmp) > 0 :
            fd_tmp = fd_tmp[0:len(fd_tmp) - 1]
         FD_stream.close()
         if fd_tmp.isdigit():
            output.append(fd_tmp)
         else:
            output.append(None)
      else:
         output.append(None)

   return output
