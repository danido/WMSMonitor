#!/usr/bin/python

import logging,os

def get_result_WMS(filename):

   logger = logging.getLogger('get_result_WMS')

# START running=4, idle=0,current=4, load=0.03,input_fl=0, queue_fl=0, dg20=0, ism_size=7132, ism_entries=675, sandbox= 3,tmp= 3, gftp=1, FD_WM=7, FD_LM=9, FD_JC=4, FD_LL=4, LB0, LL=0, LBPX=0, PX=0, FTPD=Null, JC=0, LM=0, WM=0, WMP=0, END

   data = []
   metrics = ['running','idle','current','load','input_fl','queue_fl','dg20','ism_size','ism_entries','sandbox','tmp','gftp','FD_WM','FD_LM','FD_JC','FD_LL','LB','LL','LBPX','PX','FTPD','JC','LM','WM','WMP','varlog','varlibmysql','MEMUSAGE','LOADLIMIT','MEMLIMIT','DISKLIMIT','fdrain','fload','ftraversaltime']


   if (os.access(filename,os.F_OK) == True):
      file = open(filename)
   else:
      logger.error('Cannot open file = '+ filename)      
      logger.info('Returning all Null')
      for str in metrics:
         data.append('Null')      
      return data

   std = file.readlines()

   DataFound = False

   for line in std:
      if line.find('START') != -1 and line.find('END') != -1 :
         line = line[line.find('START') + 6 : line.find('END') - 1 ]
         line2 = line
         for str in metrics:
            data_tmp = line2[line2.find('=',line2.find(str)) + 1 : line2.find(',',line2.find(str))]         
            data.append(data_tmp)
            idx = line2.find(',',line2.find(str))
            line2 = line2[idx:]
         DataFound = True

   if DataFound == False:
      logger.info('No data Found. Returning all Null')
      for str in metrics:
         data.append('Null') 

   return data
