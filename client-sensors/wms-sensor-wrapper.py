#!/usr/bin/python
import sys,os,time
sys.path.append('../../common')
sys.path.append('../../common/classes')
import readconf_func
import logging
import logpredef_wmslb
import os, sys
import check_running_func

logger = logging.getLogger('wms-sensor-wrapper')

confvar = readconf_func.readconf();

import lb_apiquery_func
import wms_class
import wms_sensor_func
import send_data_to_activemq
import mail_garbage_coll_func
import mappingtable_class
import socket

def loadmm(lines):
   d1 = {}
   try:
      idx = lines.index('START OF FILE\n')
   except ValueError:
      return None 
   try:
      idx2 = lines.index('END OF FILE\n')
   except ValueError:
      return None
   for line in lines[idx + 1 : idx2] :
      if line.find('DATE') == -1:
         linesp = line.split()
         nce =  linesp[0].strip().rstrip()
         occ =  linesp[1].strip().rstrip()
         d1[nce] = occ
   return d1

logger.info('####################################')
logger.info('## This is the wms-sensor-wrapper ##')
logger.info('####################################')

TIMELOCK = int(confvar.get('SENSORS_TIMELOCK'))
FLAG = 0

HOST = confvar.get('ACTIVEMQ_BROKER_HOST')
PORT = confvar.get('ACTIVEMQ_PORT')
TOPIC = confvar.get('ACTIVEMQ_TOPIC')
sent_mail_path = confvar['INSTALL_PATH'] + '/sensors/sent_mail'

#############################################################
### Look for already running wrapper process

pname = 'wms-sensor-wrapper'
RUNNING = check_running_func.check_running(pname)
if RUNNING:
   logger.error('Another wms-sensor-wrapper is running. Aborting')
   sys.exit(1)
##############################################################


##############################################################
### We check if the sensors run early in the past
### Security check not to overload the wms
### TIMELOCK is set in the site.def
##############################################################
logger.info('Looking for data file.')
cmd = 'ls -1tr /tmp/WMSLOCKFILE_*' + ' 2> /dev/null'
string = os.popen(cmd)
lines = string.readlines()
if len(lines) == 0:
    logger.info('No data files already exists. Creating a new one.')
    filename = '/tmp/WMSLOCKFILE_' + str(time.time())
    logger.info('Filename is : ' + filename)
    FLAG = 1
else:
    logger.info('Found data file. Checking if it not older than ' + str(TIMELOCK) + ' seconds.')
    for line in lines:
       if line.find('_'):
          filenametmp = line[line.find('_') + 1 :]
          if (time.time() - float(filenametmp)) < TIMELOCK:
             filename = line[:-1]
             logger.info('File is good. Filename is : ' + filename)
             FLAG = 0
          else: 
             cmd = 'rm -f ' + line
             logger.info('File is too old. Removing it. Cmd is : ' + cmd)
             status = os.system(cmd)
             if status == 0:
                logger.info('File ' + line + ' removed.')
             else:
                logger.error('Cannot remove file ' + line + '.')
             FLAG = 1
             filename = '/tmp/WMSLOCKFILE_' + str(time.time())

if FLAG == 1:

   ###################################################################
   #### First we call wms_sensor_func to get wms punctual data #######
   #### ##############################################################
   logger.info('Calling wms_sensor_func')

   timenow = time.time()
   enddate_epoch = timenow
   comp_time = str(timenow)
   comp_date_str = time.strftime("%Y-%m-%d %H:%M:%S",time.localtime(timenow))

   wms, MM_DONE = wms_sensor_func.wms_sensor()
   
   timenow2 = time.time()
   comp_time2 = str(timenow2)
   comp_date_str2 = time.strftime("%Y-%m-%d %H:%M:%S",time.localtime(timenow2))

   logger.info ('Back from wms_sensor_func')

   logger.info('Data Collected are:')
   logger.info(wms)

   ###################################################################
   #### Now we call lb_apiquery_func to get job flow rates          ##
   #### If DATA_FROM_LBPROXY is enable quries are performed on the  ##
   #### LBProxy DB. The enddate for the queries if the same value   ##
   #### of the starting time for the wms_sensor_func                ##
   #### The query interval is imited by MAX_QUERY_STEP in conf file ##
   ###################################################################
 
   wmsdata_list = []
   if confvar['DATA_FROM_LBPROXY'] == 'True':


      # Loading the USERMAP_TABLE
      maptable = mappingtable_class.mappingtable( int(confvar['MAPPING_EXPIRY_TIME']) )
      if confvar['USE_MAP_FILE'] == 'True':
         mapstatus = maptable.load(confvar['MAPTABLE_FILENAME'])
         if mapstatus  == 0:
            logger.info("Map table successfully imported from file: " + confvar['MAPTABLE_FILENAME'])
         else:
            logger.warning("Cannot import maptable from file: " + confvar['MAPTABLE_FILENAME'])


      if confvar['QUERY_PARAMETERS_TYPE'] == 'USE_SERVER_PARAMETERS_FILE':
         logger.error('USE_SERVER_PARAMETERS_FILE method not implemented yet. Please change conf file. Aborting sensor')
         sys.exit(1)

      elif confvar['QUERY_PARAMETERS_TYPE'] == 'USE_LAST_RUN_DATE':
         logger.info("Using last run date to obtain the STARTDATE in queries")
         try:
            datefl = open(confvar["INSTALL_PATH"] + '/sensors/tmp/last_run_date','r')
            startdate_epoch = int(float(datefl.readline()))
            datefl.close()
            if (enddate_epoch - startdate_epoch) < int(confvar['MAX_QUERY_STEP']):
               ENDDATE = time.strftime("%Y-%m-%d:%H:%M:%S",time.gmtime(enddate_epoch))
               STARTDATE = time.strftime("%Y-%m-%d:%H:%M:%S",time.gmtime(startdate_epoch))
               step = enddate_epoch - startdate_epoch
               logger.info('ENDDATE = ' + ENDDATE + '   STARTDATE = ' + STARTDATE + '   STEP = ' + str(step))
            else:
               logger.warning('Query interval too long, reduced to MAX_QUERY_STEP = ' + confvar['MAX_QUERY_STEP'])
               ENDDATE = time.strftime("%Y-%m-%d:%H:%M:%S",time.gmtime(enddate_epoch))
               STARTDATE = time.strftime("%Y-%m-%d:%H:%M:%S",time.gmtime(enddate_epoch - int(confvar['MAX_QUERY_STEP'])))
               step = int(confvar['MAX_QUERY_STEP'])
               logger.info('ENDDATE = ' + ENDDATE + '   STARTDATE = ' + STARTDATE + '   STEP = ' + confvar['MAX_QUERY_STEP'])
         except IOError:
            logger.warning("Cannot open/read last_run_date file. Using fixed step STEPDATE")
            logger.info('STEPDATE = ' + confvar['STEPDATE'])
            step = int(confvar['STEPDATE'])
            ENDDATE = time.strftime("%Y-%m-%d:%H:%M:%S",time.gmtime(enddate_epoch))
            STARTDATE = time.strftime("%Y-%m-%d:%H:%M:%S",time.gmtime(enddate_epoch - step))
            logger.info('ENDDATE = ' + ENDDATE + '   STARTDATE = ' + STARTDATE + '   STEP = ' + confvar['STEPDATE'])
         try:
            fnametmp = confvar["INSTALL_PATH"] + '/sensors/tmp/last_run_date'
            cmd = 'touch ' + fnametmp + '; mv -f ' + fnametmp + '  ' + fnametmp + '.old'
            os.system(cmd)
            datefl = open(fnametmp,'w')
            datefl.write(str(enddate_epoch))
            datefl.close()
         except IOError:
            logger.warning("Cannot write last_run_date file. Next time conf file stepdate will be used")
            
      elif confvar['QUERY_PARAMETERS_TYPE'] == 'USE_FIXED_STEP':
         logger.info('Using fixed step to perform queries. STEP = ' + confvar['STEPDATE'])
         ENDDATE = time.strftime("%Y-%m-%d:%H:%M:%S",time.gmtime(enddate_epoch))
         STARTDATE = time.strftime("%Y-%m-%d:%H:%M:%S",time.gmtime(enddate_epoch - int(confvar['STEPDATE'])))
         logger.info('ENDDATE = ' + ENDDATE + '   STARTDATE = ' + STARTDATE + '   STEP = ' + confvar['STEPDATE'])

      timenow = time.time()
      comp_time3 = str(timenow)
      comp_date_str3 = time.strftime("%Y-%m-%d %H:%M:%S",time.localtime(timenow))
#      wmsdata_list = lb_apiquery_func.lb_query(socket.getfqdn(),'2011-06-17:12:30:01','2011-06-17:12:43:19')
      wmsdata_list = lb_apiquery_func.lb_query(socket.getfqdn(),STARTDATE,ENDDATE)
      #SWITCHING TO LOCALTIME WHICH IS THE ONE TO REPORT ON DATA MESSAGE
      ENDDATE = time.strftime("%Y-%m-%d:%H:%M:%S",time.localtime(enddate_epoch))
      STARTDATE = time.strftime("%Y-%m-%d:%H:%M:%S",time.localtime(enddate_epoch - int(confvar['STEPDATE'])))

      # Trying to map the all the users and aggregating to have global data for wms 
      logger.info("Starting the mapping/aggregation loop.")
      for wmsdata in wmsdata_list:
         for user in wmsdata.userlist:
            if maptable.mapuser(user) == 0:
               continue
            else:
               if maptable.get_map_from_file(confvar['WMPROXY_LOG_FILE'],confvar['MAX_ROTATED_LOG'],confvar['MAPPING_COMMAND'],user) == 0:
                  maptable.mapuser(user)
               else:
                  logger.warning("It was not possible to map a user. DN = " + user['dn'])
         wmsdata.aggregate_on_user()
      if maptable.save(confvar['MAPTABLE_FILENAME']) == 0:
         logger.info("Mapping table saved to file.")
      else:
         logger.warning("Cannot save mapping table to file")


      timenow = time.time()
      comp_time4 = str(timenow)
      comp_date_str4 = time.strftime("%Y-%m-%d %H:%M:%S",time.localtime(timenow))

########################################################################################
####Creating the file to send
########################################################################################

   file_to_send = confvar['INSTALL_PATH'] + '/sensors/tmp/MESSAGE_IN_A_BOTTLE_' + comp_time + '.txt'
   logger.info('Preparing message to be sent. File is: ' + file_to_send)
   try:
      mfile = open(file_to_send,'w')
      mfile.write('START: WMS SENSOR\n\n')
      mfile.write('WMS SENSOR RESULT for WMS: ' + wms.host + '\n')
      mfile.write('DATA COLLECTION STARTED ON: ' + comp_date_str + ' = ' + comp_time + ' seconds since Epoch\n')
      mfile.write('DATA COLLECTION COMPLETED ON: ' + comp_date_str2 + ' = ' + comp_time2 + ' seconds since Epoch\n')
      mfile.write( wms.make_lines() )
      mfile.write('\nSTART: CE_MM HIST\n')
      if MM_DONE:
         logger.info('Reading CE_MM file. File is ' + confvar['INSTALL_PATH'] + '/sensors/tmp/CE_MM.txt')
         try:
            mmfile = open(confvar['CE_MM_FILE'] , 'r')
            lines = mmfile.readlines()
            logger.info('Calling loadmm function')
            mmdict = loadmm(lines)
            mmfile.close()
            if mmdict != None:
               try:
                  logger.info('Writing CE_MM dict to file to send')
                  mfile.write(str(mmdict) + '\n')
               except IOError:
                  logger.info('ERROR: cannot write CE_MM dict on file')
            else:
               logger.warning('Malformed MM file. Please check.')
         except IOError:
            logger.info('ERROR: cannot acces CE_MM.txt even if MM_DONE is True')
            logger.info(confvar['INSTALL_PATH'] + '/sensors/tmp/CE_MM.txt')
      mfile.write('END: CE_MM HIST\n\n')
      #########################################################################
      ## Now it's the globus error time                                      ##
      ## if new globus error file exist addd it to the file_to_send          ##
      #########################################################################
      logger.info("It's the globus error time. First we check if we need to have those info.")
      mfile.write('START: GLOBUS ERROR STATS\n')
      try:
         glob_last_up_fl = open(confvar['INSTALL_PATH'] + '/sensors/tmp/globus_last_update','r')
         last_globus_update = float(glob_last_up_fl.readline())
         glob_last_up_fl.close()
      except:
         logger.warning('Cannot open file to get the last run time of globus error. File is ' + confvar['INSTALL_PATH'] + '/sensors/tmp/globus_last_update')
         logger.info('Set last update run time to 0s since Epoch')
         last_globus_update = 0
      try:
         logger.info('Getting stat information about the GLOBUS_ERROR_FILE')
         glerrfile = confvar['GLOBUS_ERROR_FILE_LOCATION']
         globus_stat = os.stat(glerrfile)
         print "error globus",globus_stat.st_mtime, last_globus_update
         if globus_stat.st_mtime > last_globus_update:
            logger.info('We have a brand new GLOBUS_ERROR_FILE so we add it to the file to send')
            globfile = open(glerrfile,'r')
            globlines = globfile.readlines()
            mfile.writelines(globlines)
            logger.info('Creating the new globus_last_update file')
            glob_last_up_fl = open(confvar['INSTALL_PATH'] + '/sensors/tmp/globus_last_update','w')
            glob_last_up_fl.write(str(time.time()))
            glob_last_up_fl.close()
         else:
            logger.info('This GLOBUS_ERROR_FILE was already sent. Doing nothing with this file.')
      except OSError:
         logger.warning('GLOBUS_ERROR_FILE not accessible. file is ' + confvar['GLOBUS_ERROR_FILE_LOCATION'] + ' No globus error data sent.')
      mfile.write('END: GLOBUS ERROR STATS\n\n')

      #########################################################################
      ## Now it's the ice error time                                      ##
      ## if new ice error file exist addd it to the file_to_send          ##
      #########################################################################
      
      # TO BE INCLUDED, for now we only write the plaeholders on the mfile
      
      mfile.write('START: CREAM ERROR STATS\n')
      mfile.write('END: CREAM ERROR STATS\n\n')


      mfile.write('END: WMS SENSOR\n\n')
     
      #################################
      ##   Now the lb-sensor data    ##
      #################################

      if confvar['DATA_FROM_LBPROXY'] == 'True':

         mfile.write('START: LB SENSOR\n\n')
         mfile.write('DATA COLLECTION STARTED ON: ' + comp_date_str3 + ' = ' + comp_time3 + ' seconds since Epoch\n')
         mfile.write('DATA COLLECTION COMPLETED ON: ' + comp_date_str4 + ' = ' + comp_time4 + ' seconds since Epoch\n')
         mfile.write('TYPE OF THE REQUEST: ' + 'NORMAL' + '\n')
         mfile.write('STARTDATE = ' + STARTDATE + '\n')
         mfile.write('ENDDATE = ' + ENDDATE + '\n')
         mfile.write('DELTAT = ' + str(step) + '\n\n')
         if len(wmsdata_list) == 0:   # write headers for compatibility even if no data are present
            mfile.write('START: USERDATA DICTIONARY\n')
            mfile.write('END: USERDATA DICTIONARY\n')
            mfile.write('\nSTART: CE DATA\n')
            mfile.write('END: CE DATA\n')
            mfile.write('\nSTART: WMS RATE DATA\n')

            WMSzero = wms_class.WMS(socket.getfqdn())
            WMSzero.wmsrate_dict['dn'] = socket.getfqdn()
            for key in WMSzero.wmsrate_dict:
               if key != 'dn' and key != 'voms_group' and key != 'role' and key != 'VO':
                  WMSzero.wmsrate_dict[key] = '0'
            mfile.write(str(WMSzero.wmsrate_dict) + '\n')
 
            mfile.write('END: WMS RATE DATA\n')
            mfile.write('\nSTART: LBSERVER HIST\n')
            mfile.write('END: LBSERVER HIST\n\n')
         else:
            for wmsdata in wmsdata_list:
               mfile.write(str(wmsdata))
      
      mfile.write('END: LB SENSOR\n')
      mfile.write('\nEOF\n')
      mfile.close()
      #############################################################################################
   
      #################################
      ### ACTIVEMQ SENDING   ##########
      #################################

      logger.info('Sending ActiveMQ message')
      metrics = 'WMS-SENSOR'
      send_status = send_data_to_activemq.send_data_to_activemq(file_to_send,HOST,PORT,TOPIC,metrics)

      #############################################################################
      ### Creating the LOCKFILE that it is just a a copy of the file_to_send so 
      ### that in case of a new request close in time
      ### with the same parameters, we can just send the LOCKFILE or do nothing
      #############################################################################

      logger.info('Coping file sent to the LOCKFILE')
      cmd = 'cp -f ' + file_to_send + ' ' + filename
      status = os.system(cmd)

      #############################################################################
      ### Moving the file_to_sent to sent mail for future reference
      ### A garbage collector will clean sent mail periodically
      #############################################################################

      logger.info('Moving file sent to sent_mail')
      cmd = 'mv -f ' + file_to_send + ' ' + sent_mail_path
      status = os.system(cmd)
      if status == 0 :
         logger.info('File now is in : ' + sent_mail_path + '/' + file_to_send[ file_to_send.find('MESS') : ] )
         print 'File now is in : ' + sent_mail_path + '/' + file_to_send[ file_to_send.index('MESS') : ]
      else:
         logger.warning('Cannot copy file to sent_mail dir')
         print 'Cannot copy file to sent_mail dir'

   except IOError: # comes from the try to open mfile
      logger.error('Cannot open file for writing. Filename is : ' + file_to_send)
      logger.error('Not sending message')

else:  # comes from if FLAG == 1, means that we already have a file for this query
       # we have to send the LOCKFILE

   logger.info('WMSENSOR Already performed this query. RESULT IN LOCKFILE: ' + filename)
   
   #################################
   ### ACTIVEMQ SENDING   ##########
   #SENDING FILES DISABLED TO NOT DUPLICATE DATA IN SERVER DB#
   #################################
   if False:
      logger.info('Sending ActiveMQ message')
      metrics = 'WMS-SENSOR'
      send_status = send_data_to_activemq.send_data_to_activemq(filename,HOST,PORT,TOPIC,metrics)

   #############################################################################
   ### Coping the file_to_sent to sent mail for future reference
   ### A garbage collector will clean sent mail periodically
   #############################################################################

      logger.info('Coping file sent to sent_mail')
      cmd = 'cp -f ' + filename + ' ' + sent_mail_path
      status = os.system(cmd)
      if status == 0 : 
         logger.info('File now is in : ' + sent_mail_path + '/' + filename[ filename.find('WMSL') : ] )
         print 'File now is in : ' + sent_mail_path + '/' +  filename[ filename.find('WMSL') : ]
      else:
         logger.warning('Cannot copy file to sent_mail dir')
         print 'Cannot copy file to sent_mail dir'

###########################################################
### need a call to a mail garbage collector now
###########################################################

INVOKE_GARBAGE = False
lastrun = 0 # Initialized to 0 so if lastrun file is not present garbage collector is invoked without errors

try:
   lastrunf = open(confvar['INSTALL_PATH'] + '/sensors/sent_mail/last_garbage_run.txt')
   lastrun = lastrunf.readline()
   lastrunf.close()
except IOError:
   logger.error('Cannot access last garbage collector runtime file: ' + confvar['INSTALL_PATH'] + '/sensors/sent_mail/last_garbage_run.txt')
   logger.info('Invoking the sent mail garbage collection anyway')
   INVOKE_GARBAGE = True

if (time.time() - float(lastrun)) > int( confvar['SENT_MAIL_CHECK_FREQ'] ) :   #DO NOT USE TIMENOW HERE!!! cannot be defined!!!
   logger.info('Invoking the sent mail garbage collection. Last run was:' + str(lastrun) + '. Now is: ' + str(time.time()) + '.')
   INVOKE_GARBAGE = True
if INVOKE_GARBAGE:
   mail_garbage_coll_func.mail_garbage_coll(sent_mail_path, int( confvar['SENT_MAIL_EXPIRY_TIME'] ) )
else:
   logger.info('There is not need to run the sent mail garbage collector according to SENT_MAIL_CHECK_FREQ: ' + confvar['SENT_MAIL_CHECK_FREQ'])

###########################################################

if send_status == 'OK':
   logger.info('MESSAGE SENT!')
   # Send the sent file to snmp for output
   print 'EVERYTHING was fine. Message SENT.'
else:
   print 'Sending Problems'
