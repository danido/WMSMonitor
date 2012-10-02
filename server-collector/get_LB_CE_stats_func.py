#!/usr/bin/python

import logging,os,time
import long_file_collector_func,logpredef

def get_LB_CE_stats(wmshost,lbhost,send_file_OID,port):

   logger = logging.getLogger('get_LB_CE_stats')


# SNMPv2-SMI::enterprises.10403.94.101.1 = STRING: "FILE CREATED = /root/wmsmon/bin/CE_MM.txt"

   filename = 'out_CE_stat_' + wmshost + '_'  + lbhost + '_' + str(time.time()) + '.txt'

   logger.info('Opening file ' + filename + ' for writing')
   try:
      f = open(filename,'w')
   except IOError:
      logger.info('Cannot open file ' + filename + ' for writing.  Returning None')
      return None    

   logger.info('We can now try to get the CE_stats file')
   # We need here the long file collector function becaus we do not know a priori how long the file can be

   #creating the web request

   cmd = "echo " + wmshost + " " + lbhost + " > /var/www/html/wmsmon/tmp/CEstat_request.txt"
   os.system(cmd)
   #calling the send file on the LB

   
   dataline = long_file_collector_func.long_file_collector(lbhost,send_file_OID,port)

   datalinesp = dataline.split(';') 
   for line in datalinesp:
      line = line.strip().rstrip()
      if line != 'START' and line != 'END' and line != 'EOF':

         f.write(line + '\n')
   #f.write('\n')
   f.close()
   
   logger.info('Data got and written to file. Filename is: ' + filename)
   return filename
