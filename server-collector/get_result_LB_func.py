#!/usr/bin/python

import logging,os
def get_result_LB(filename,wmshost,lbhost):

   logger = logging.getLogger('get_result_LB')

   data = []
   metrics = ['WMP_in','WMP_in_col','WMP_in_col_avg','WMP_in_col_std','WM_in','WM_in_res','JC_in','JC_out','load','lb_disk','LB_CON','LB','LL','JOB_DONE','JOB_ABORTED','lib_mysql_disk']


   if (os.access(filename,os.F_OK) == True):
      file = open(filename)
   else:
      logger.error('Cannot open file = '+ filename)      
      logger.info('Returning all Null')
      for str in metrics:
         data.append('Null')      
      return data

   std = file.readlines()
   logger.info('Searching for host: ' + wmshost + ' ' + lbhost)

   for line in std:
      if line.find(wmshost) != -1 and line.find(lbhost) != -1:
              if line.find('START') != -1 and line.find('END') != -1 :
                 logger.info("FOUND START END line, line is: " + line)
		 line = line[line.find('START') + 6 : line.find('END') - 1 ]
		 line2 = line
		 for str in metrics:
		    data_tmp = line2[line2.find('=',line2.find(str)) + 1 : line2.find(',',line2.find(str))]         
		    data.append(data_tmp)
		    idx = line2.find(',',line2.find(str))
		    line2 = line2[idx:]
	      else:
		 logger.info('No data Found. Returning all Null')
		 for str in metrics:
		    data.append('Null') 
      else:
           continue

   if len(data) == 0:
      for str in metrics:
                    data.append('Null')
   if len(data) < len(metrics):
      data = []
      for str in metrics:
                    data.append('Null')

   file.close()
   return data
