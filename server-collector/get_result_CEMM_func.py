#!/usr/bin/python

import logging,os
import long_file_collector_func,logpredef

def get_result_CEMM(host,filename,send_file_OID,port):

   logger = logging.getLogger('get_result_CEMM')

# SNMPv2-SMI::enterprises.10403.94.101.1 = STRING: "FILE CREATED = /root/wmsmon/bin/CE_MM.txt"
   ERRORFLAG = 1
   day,occ,num=None,None,None
   if (os.access(filename,os.F_OK) == True):
      file = open(filename)
   else:
      logger.error('Cannot open file = '+ filename)      
      logger.info('Returning all None')
      return None,None,None

   std = file.readlines()

   for line in std:

      if line.find('"FILE CREATED =') != -1:
         ERRORFLAG = 0
         logger.info('The remote file was created succesfully. We can now try to get the CE_MM statistics')
         # We need here the long file collector function becaus we do not know a priori how long the file can be
         dataline = long_file_collector_func.long_file_collector(host,send_file_OID,port)
         if dataline.find('START') != -1 and dataline.find('END') != -1:
            logger.info('Found line with data, Trying to parse it.')
            logger.info('Dataline is : ' + dataline)
            occ = [] 
            num = []
            linesp = dataline.split(';')
            for i in range(0,len(linesp)) :
               stri = linesp[i]
               stri = stri.strip().rstrip()
               if stri.find('DATE') != -1:
                  day = stri.split('=')[1]
                  day = day.strip().rstrip()
               else:
                  if stri != 'START' and stri != 'END' :
                     occ_num = stri.split()     # This list contains one entry the occurrence and ce number
                     if len(occ_num) >= 2: 
                        occ.append(occ_num[0])
                        num.append(occ_num[1])

         else:
            logger.info('No data found. Returning two empty lists')
            return None,None,None

   if ERRORFLAG:
         logger.error('Cannot open file = '+ filename)
         logger.info('Returning all None')
         return None,None,None
   else:
         return day,occ,num

       

