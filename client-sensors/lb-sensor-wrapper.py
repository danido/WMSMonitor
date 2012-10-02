#!/usr/bin/python

import sys,os
sys.path.append('../../common')
sys.path.append('../../common/classes')
import readconf_func
import logging
import logpredef_wmslb, check_running_func, send_data_to_activemq
import os, sys, time

logger = logging.getLogger('lb-sensor-wrapper')

import mail_garbage_coll_func
import lb_sensor_func
import socket 


#############################################################
### Look for already running wrapper process

pname = 'lb-sensor-wrapper'
RUNNING = check_running_func.check_running(pname)
if RUNNING:
   logger.error('Another lb-sensor-wrapper is running. Aborting')
   ### THIS PRINT IS RETURNED TO SNMP
   print 'NOT EXECUTED BECAUSE ANOTHER INSTANCE IS RUNNING'
   sys.exit(1)
#############################################################

logger.info('###################################')
logger.info('## This is the lb-sensor-wrapper ##')
logger.info('###################################')


hostname = socket.getfqdn()

if hostname == '' or hostname == None:
   logger.error('Could not determine machine hostname! Exiting...')
   print 'None'
   sys.exit(1)

####### variable init from .def file

confvar=readconf_func.readconf();

TIMELOCK = int(confvar.get('SENSORS_TIMELOCK'))

HOST = confvar.get('ACTIVEMQ_BROKER_HOST')
PORT = confvar.get('ACTIVEMQ_PORT')
TOPIC = confvar.get('ACTIVEMQ_TOPIC')
sent_mail_path = confvar['INSTALL_PATH'] + '/sensors/sent_mail'

###########################################

############# all this part is not needed if lbproxy is used...skipped using the lbproxy flag, set in defaults
##########################################


if confvar['DATA_FROM_LBPROXY'] == 'False':
        import lb_query_func 
        host = confvar.get('WMSMON_HOST')
        LB_PARA_HOST = confvar.get('LB_PARA_HOST')



	###########################################
	# now get the PARAMETERS file using wget
	###########################################

	logger.info("Retriving LB_PARAMETERS file")
	cmd = "rm -f LB_PARA*"
	os.system(cmd)

	cmd = "wget -t 1 -nc --quiet --no-check-certificate --certificate=/etc/grid-security/hostcert.pem --private-key=/etc/grid-security/hostkey.pem  --ca-directory=/etc/grid-security/certificates/ " + LB_PARA_HOST + "/wmsmon/tmp/LB_PARAMETERS"
	logger.info("Command is: " + cmd)
	status = os.system(cmd)
	if status != 0:
	   logger.error("Error in getting the file. Exiting!")
	   sys.exit(1)
	os.system("mv -f LB_PARAMETERS /tmp")
	std = open("/tmp/LB_PARAMETERS",'r')
	lines = std.readlines()
	logger.info(lines)
	std.close()

	#Searching parameter for query regarding this LB
	logger.info('Searching parameters for queries regarding this LB')
	Found_flag = False
	N_SEND_ERRORS = 0
	N_PROCESSED_REQ = 0

	for line in lines:
	    linetmp = line[line.find(hostname):]
	    linesp = linetmp.split(';')
	    if linesp.count(hostname) > 0 :
	       N_PROCESSED_REQ = N_PROCESSED_REQ + 1 
	       ############################################################
	       ## check that the number of requests did not exceed the max
	       ############################################################

	       if N_PROCESSED_REQ > confvar['MAX_LB_QUERY']:
		  logger.error('NEXT QUERY NOT PERFORMED. MAX NUMBER REACHED.')
		  logger.info('Returning error to snmp and exiting!')
		  break

	       ###################################################

	       Found_flag = True
	       STARTDATE = linesp[1]
	       start_epoch =  time.mktime(time.strptime(STARTDATE,"%Y-%m-%d %H:%M:%S"))
	       ENDDATE = linesp[2]
	       end_epoch = time.mktime(time.strptime(ENDDATE,"%Y-%m-%d %H:%M:%S"))
	       TYPE = linesp[3][:-1].strip().rstrip()
	       logger.info('Found interesting parameters: ' + hostname + ',' + STARTDATE + ',' + ENDDATE + ',' + 'TYPE = ' + TYPE)
	       if (end_epoch - start_epoch) > confvar['MAX_QUERY_SPAN']:
		  logger.error('Query interval too long in time (' + str(end_epoch - start_epoch) + 's) - QUERY NOT PERFORMED!')
		  N_SEND_ERRORS = N_SEND_ERRORS + 1
		  continue
	       #############################################
	       ##  Looking if we have a recent file with  ##
	       ##      the result of the same query       ##
	       #############################################

	       logger.info('Looking for data file.')
	       cmd = 'ls -1tr /tmp/LBLOCKFILE_' + hostname + '*' + ' 2> /dev/null'
	       string = os.popen(cmd)
	       ls_lines = string.readlines()
	       FLAG = 1
	       if len(ls_lines) == 0:
		  logger.info('No data files already exists. Creating a new one.')
		  filename = '/tmp/LBLOCKFILE_' + hostname + '_' + str(start_epoch) + '_' + str(end_epoch)
		  logger.info('Filename is : ' + filename)
		  FLAG = 1
	       else:
		  logger.info('Found data files.')
		  for line2 in ls_lines:
			logger.info('Checking if it refers to this request.')
			if line2.find('_'):
			   filenametmp = line2[line2.find('_') + 1 : len(line2) - 1]
			   file_endstr = hostname + '_' + str(start_epoch) + '_' + str(end_epoch)
			   if filenametmp == file_endstr :
			      filename = line2[:-1]
			      logger.info('File is for this query. Filename is : ' + filename)
			      FLAG = 0
			      break # we need to end the loop we have our file
			   else:
			      logger.info('File is not good.  Filename is : ' + line2 + '.')
			      logger.info('Maybe we will be more lucky with the next one.')
			      filename = '/tmp/LBLOCKFILE_' + hostname + '_' + str(start_epoch) + '_' + str(end_epoch)
			      FLAG = 1
			      cmd = 'rm -f ' + line2[:len(line2) - 1]
			      status = os.system(cmd)
			      if status == 0:
				 logger.info('File removed.')
			      else:
				 logger.error('File cannot be removed. File is ' + line2)

	       ############################################
	       ## Check on existing file is now finished ##
	       ##  if FLAG == 1 if have to create a new  ##
	       ##       one through another query        ##
	       ## otherwise we can just send the LOCKFILE #
	       ##    or do nothing                       ##
	       ############################################

	       if FLAG == 1:
		  logger.info('Launching lb_query')
		  # now lb_queryfunc return LB_dict with machine parameters and a list of wmsdata class
		  timenow = time.time()
		  comp_time = str(timenow)
		  comp_date_str = time.strftime("%Y-%m-%d %H:%M:%S",time.localtime(timenow))

		  #COLLECTING DATA ABOUT LB MACHINE STATUS
		  LB_dict = {}
		  LB_dict = lb_sensor_func.lb_sensor(confvar)

		  wmsdata_list = lb_query_func.lb_query(hostname,STARTDATE,ENDDATE,'LBSERVER')
		  logger.info('Data Retrieved. Creating the output string to be sent back to WMSMonitor')

		  timenow2 = time.time()
		  comp_time2 = str(timenow2)
		  comp_date_str2 = time.strftime("%Y-%m-%d %H:%M:%S",time.localtime(timenow2))



		  ############################################################################################
		  ##### here we have to agreegata per wms - -now wmsdata contains data per wms and per user
		  ##### it is done through a wmdatadata method - aggregate_on_user()
		  ##### then everything is ready to create the mail to be sent to actvemq broker
		  ##### and to return a string via snmp to the collector
		  ############################################################################################

		  for wmsdata in wmsdata_list:
		     wmsdata.aggregate_on_user()

		  file_to_send = confvar['INSTALL_PATH'] + '/sensors/tmp/LB_' + TYPE + '_MESSAGE_IN_A_BOTTLE_' + comp_time + '.txt'
		  logger.info('Preparing message to be sent. File is: ' + file_to_send)

		  try:
		     mfile = open(file_to_send,'w')
		     mfile.write('###################################################################################################\n')
		     mfile.write('LB SENSOR RESULT for LB: ' + hostname + '\n')
		     mfile.write('DATA COLLECTION STARTED ON: ' + comp_date_str + ' = ' + comp_time + ' seconds since Epoch\n')
		     mfile.write('DATA COLLECTION COMPLETED ON: ' + comp_date_str2 + ' = ' + comp_time2 + ' seconds since Epoch\n')
		     mfile.write('TYPE OF THE REQUEST: ' + TYPE + '\n')
		     mfile.write('STARTDATE = ' + STARTDATE + '\n')
		     mfile.write('ENDDATE = ' + ENDDATE + '\n')
		     mfile.write('###################################################################################################\n')
		     mfile.write('\nLB Sensors Output:\n')
		     mfile.write(str(LB_dict) + '\n')
		     mfile.write('LB SENSOR FOUND DATA about ' + str(len(wmsdata_list)) + ' WMS\n')
		     for wmsdata in wmsdata_list:
			mfile.write(str(wmsdata))
		     mfile.write('\nEOF\n')
		     mfile.close()

		     #################################
		     ### ACTIVEMQ SENDING   ##########
		     #################################

		     logger.info('Sending ActiveMQ message')
		     metrics = 'LB-SENSOR-' + TYPE
		     send_status = send_data_to_activemq.send_data_to_activemq(file_to_send,HOST,PORT,TOPIC,metrics)
		     if send_status != 'OK':
			logger.error('FILE NOT SENT!')
			N_SEND_ERRORS = N_SEND_ERRORS + 1

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

		  except IOError:
		     logger.error('Cannot open file for writing. Filename is : ' + file_to_send)
		     logger.error('Not sending message')
		     N_SEND_ERRORS = N_SEND_ERRORS + 1

	       else:    # come from FLAG == 1 , means that we already have a file for this query
			# we have to send the LOCKFILE
		  logger.info('LBSENSOR Already performed this query.  We send the LOCKFILE: ' + filename)
		  #################################
		  ### ACTIVEMQ SENDING   ##########
		  #################################

		  logger.info('Sending ActiveMQ message')
		  metrics = 'LB-SENSOR-' + TYPE
		  send_status = send_data_to_activemq.send_data_to_activemq(filename,HOST,PORT,TOPIC,metrics) 
		  if send_status != 'OK':
		     logger.error('FILE NOT SENT!')
		     N_SEND_ERRORS = N_SEND_ERRORS + 1

		  #############################################################################
		  ### Coping the file_to_sent to sent mail for future reference
		  ### A garbage collector will clean sent mail periodically
		  #############################################################################

		  logger.info('Coping file sent to sent_mail')
		  cmd = 'cp -f ' + filename + ' ' + sent_mail_path
		  status = os.system(cmd)

	if Found_flag == False:
	   logger.warning('No interesting parameters found, no query performed!')
	   # This print is returned to snmp
	   print 'No interesting parameters found, no query performed!'


	###############################################################
	### MAIN PRINT RETURNED TO SNMP IF EVERYTHING WAS FINE
	### Threated the max number reached and returned
	###############################################################

	if N_PROCESSED_REQ > confvar['MAX_LB_QUERY']:
	   print 'MAX NUMBER OF QUERY PERFORMED! ' + str(N_SEND_ERRORS) + ' ERRORS ON SEND HAPPENED! MAX NUMBER REACHED.'
	else:
	   print 'ALL QUERY PERFORMED! ' + str(N_SEND_ERRORS) + ' ERRORS ON SEND HAPPENED!'

	###############################################################







        ######################################################################
        ######################################################################
	######################################################################
	######## END OF SENSOR SKIPPED WITH LBPROXY FLAG
	######################################################################
        ######################################################################
        ######################################################################







elif confvar['DATA_FROM_LBPROXY'] == 'True':

   #############################################
   ##  Looking if we have a recent file with  ##
   ##      the result of the same query       ##
   #############################################

   logger.info('Looking for data file.')
   cmd = 'ls -1tr /tmp/LBLOCKFILE_' + '*' + ' 2> /dev/null'
   string = os.popen(cmd)
   ls_lines = string.readlines()
   FLAG = 1
   if len(ls_lines) == 0:
      logger.info('No data files already exists. Creating a new one.')
      filename = '/tmp/LBLOCKFILE_' + str(time.time())
      logger.info('Filename is : ' + filename)
      FLAG = 1
   else:
      logger.info('Found data file. Checking if it not older than ' + str(TIMELOCK) + ' seconds.')
      for line in ls_lines:
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
                filename = '/tmp/LBLOCKFILE_' + str(time.time())


   if FLAG == 1: # no LOCKFILE FOUND or file too old
      timenow = time.time()
      comp_time = str(timenow)
      comp_date_str = time.strftime("%Y-%m-%d %H:%M:%S",time.localtime(timenow))

      #COLLECTING DATA ABOUT LB MACHINE STATUS
      LB_dict = {}
      LB_dict = lb_sensor_func.lb_sensor(confvar)

      timenow2 = time.time()
      comp_time2 = str(timenow2)
      comp_date_str2 = time.strftime("%Y-%m-%d %H:%M:%S",time.localtime(timenow2))

      ############################################################################################
      ##### Everything is ready to create the mail to be sent to actvemq broker
      ##### and to return a string to std
      ############################################################################################

      file_to_send = confvar['INSTALL_PATH'] + '/sensors/tmp/LB_' + 'MESSAGE_IN_A_BOTTLE_' + comp_time + '.txt'
      logger.info('Preparing message to be sent. File is: ' + file_to_send)

      try:
         mfile = open(file_to_send,'w')
         mfile.write('START: LB SENSOR\n\n')
         mfile.write('LB SENSOR RESULT for LB: ' + hostname + '\n')
         mfile.write('DATA COLLECTION STARTED ON: ' + comp_date_str + ' = ' + comp_time + ' seconds since Epoch\n')
         mfile.write('DATA COLLECTION COMPLETED ON: ' + comp_date_str2 + ' = ' + comp_time2 + ' seconds since Epoch\n\n')
         mfile.write('START: LB DATA DICTIONARY\n')
         mfile.write(str(LB_dict) )
         mfile.write('\nEND: LB DATA DICTIONARY\n')
         mfile.write('\nEND: LB SENSOR\n')
         mfile.write('\nEOF\n')
         mfile.close()

         #################################
         ### ACTIVEMQ SENDING   ##########
         #################################

         logger.info('Sending ActiveMQ message')
         metrics = 'LB-SENSOR'
         send_status = send_data_to_activemq.send_data_to_activemq(file_to_send,HOST,PORT,TOPIC,metrics)
         if send_status != 'OK':
            logger.error('FILE NOT SENT!')

         #############################################################################
         ### Creating the LOCKFILE that it is just a a copy of the file_to_send so 
         ### that in case of a new request close in time
         ### we can just send the LOCKFILE or do nothing
         #############################################################################

         logger.info('Coping file sent to the LOCKFILE')
         cmd = 'cp -f ' + file_to_send + ' ' + filename
         logger.info("Command is : " + cmd)
         status = os.system(cmd)

         #############################################################################
         ### Moving the file_to_sent to sent mail for future reference
         ### A garbage collector will clean sent mail periodically
         #############################################################################

         logger.info('Moving file sent to sent_mail')
         cmd = 'mv -f ' + file_to_send + ' ' + sent_mail_path
         logger.info("Command is : " + cmd)
         print 'File now is in : ' + sent_mail_path + '/' + file_to_send[ file_to_send.index('LB_MESS') : ]
         status = os.system(cmd)

      except IOError:
         logger.error('Cannot open file for writing. Filename is : ' + file_to_send)
         logger.error('Not sending message')


   elif FLAG == 0:   # LOCKFILE FOUND

      logger.info('LBSENSOR Already performed this request.  We send the LOCKFILE: ' + filename)

      #################################
      ### ACTIVEMQ SENDING   ##########
      #################################

      logger.info('Sending ActiveMQ message')
      metrics = 'LB-SENSOR'
      send_status = send_data_to_activemq.send_data_to_activemq(filename,HOST,PORT,TOPIC,metrics)
      if send_status != 'OK': logger.error('FILE NOT SENT!')

      #############################################################################
      ### Coping the file_to_sent to sent mail for future reference
      ### A garbage collector will clean sent mail periodically
      #############################################################################

      logger.info('Coping file sent to sent_mail')
      cmd = 'cp -f ' + filename + ' ' + sent_mail_path
      logger.info("Command is : " + cmd)
      print 'File now is in : ' + sent_mail_path + '/' +  filename[ filename.find('LBL') : ]
      status = os.system(cmd)



   if send_status == 'OK':
      logger.info('MESSAGE SENT!')
      # Send the sent file to snmp for output
      print 'EVERYTHING was fine. Message SENT.'
   else:
      print 'Sending Problems'


###########################################################
### need a call to a mail garbage collector
###########################################################

INVOKE_GARBAGE = False
try:
   lastrunf = open(confvar['INSTALL_PATH'] + '/sensors/sent_mail/last_garbage_run.txt')
   lastrun = lastrunf.readline()
   lastrun_local_str = time.strftime("%Y-%m-%d %H:%M:%S",time.localtime(float(lastrun)))
   lastrunf.close()
except IOError:
   logger.error('Cannot access last garbage collector runtime file: ' + confvar['INSTALL_PATH'] + '/sensors/sent_mail/last_garbage_run.txt')
   logger.info('Invoking the sent mail garbage collection anyway')
   INVOKE_GARBAGE = True
   lastrun='0\n'
   lastrun_local_str = time.strftime("%Y-%m-%d %H:%M:%S",time.localtime(float(lastrun)))
if (time.time() - float(lastrun)) > float(confvar['SENT_MAIL_CHECK_FREQ']):
   logger.info( 'Invoking the sent mail garbage collection. Last run was:' + str(lastrun[:-1]) + '  (Local Time: ' + lastrun_local_str +'). Now is: ' + str(time.time()) + '  (Local time: ' + time.strftime("%Y-%m-%d %H:%M:%S",time.localtime()) + ').')
   INVOKE_GARBAGE = True
if INVOKE_GARBAGE:
   mail_garbage_coll_func.mail_garbage_coll(sent_mail_path,confvar['SENT_MAIL_EXPIRY_TIME'])
else:
   logger.info('There is not need to run the sent mail garbage collector according to SENT_MAIL_CHECK_FREQ: ' + confvar['SENT_MAIL_CHECK_FREQ'])


###########################################################
### END OF LB-SENSOR-WRAPPER
###########################################################

logger.info('END OF LB-SENSOR-WRAPPER')

###########################################################
###########################################################
###########################################################
