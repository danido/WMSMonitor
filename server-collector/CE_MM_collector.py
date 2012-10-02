#!/usr/bin/python

import os,sys,logging

import logpredef,readconf_func


logger = logging.getLogger('CE_MM_collector.py')


if len(sys.argv) < 2:
   print "\nUsage:\n"
   print "CE_MM_collector.py \PATH\wmsmonlist.conf\n"
   sys.exit(1)


conf_file = sys.argv[1]      #CONFIGURATION FILE REPORTING A LINE FOR EACH WMS TO MONITOR WITH
                             # WMS_HOST WMS_HOST_PORT LB_HOST DB_LB_USER DB_LB_PASSWD DB_LB_NAME
                             #EXAMPLE...
                             #wms002.cnaf.infn.it egee-rb-06.cnaf.infn.it


logger.info('Reading wmsmon conf file')
confvar=readconf_func.readconf();


####################################
# SNMP PARAMETERS INITIALIZATION   #
####################################

snmpuser = confvar.get('SNMPUSER')
snmppasswd = confvar.get('SNMPPASSWD')
#WMS_OID = confvar.get('WMS_OID')
#LB_OID = confvar.get('LB_OID')
timeout = confvar.get('SNMP_TIMEOUT')
#LB_PARAMETERS_FILENAME = '/tmp/LB_PARAMETERS' ##### NEVER CHANGE !!!!!


###################### !!!!!!!!!!!! THIS MUST GO ON CONFILE
CEMM_create_OID = ".1.3.6.1.4.1.10403.94 "
CEMM_send_OID   = ".1.3.6.1.4.1.10403.95.101.1"
##################### !!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!

##########################
# END OF SNMP INIT #######
##########################

#db = MySQLdb.connection(host=confvar.get('WMSMON_DB_HOST'),user=confvar.get('WMSMON_DB_USER'),passwd=confvar.get('WMSMON_DB_PWD'),db=confvar.get('WMSMON_DB_NAME'))
dbhost = confvar.get('WMSMON_DB_HOST')
dbuser = confvar.get('WMSMON_DB_USER')
dbpwd  = confvar.get('WMSMON_DB_PWD')
dbname = confvar.get('WMSMON_DB_NAME')

wmslist = []

#### LOOP TO CREATE THE WMSLIST FROM CONFILE

if (os.access(sys.argv[1],os.F_OK) == True):
      lsstr = open(sys.argv[1],'r')
      lines = lsstr.readlines()
      for line in lines: 
         line_tmp = line.split()
         if len(line_tmp) < 2:
             logger.error("check data in lines of \PATH\wmsmon.conf file. Exiting...\n")
             sys.exit(1)
         wmshost = line_tmp[0]
         wmslist.append(wmshost)
else:

   logger.error("CONFIGURATION file  wmsmon.conf NOT FOUND!!!Exiting.\n")
   sys.exit(1)

######### END OF LOOP ON CONF FILE, NOW WE HAVE THE WMSLIST

for wms in wmslist:


   ############################################################
   #Lauching create_CE_MM script on the WMS node
   #and searching for string FILE CREATED.FILENAME=filename
   ############################################################
   host = wms
   OID  = CEMM_create_OID
   cmd = "snmpwalk -v 3 -u " + snmpuser + " -l authNoPriv -a MD5 -A " + snmppasswd + ' ' + host + ' ' + OID + ' -t ' + timeout
   logger.info('Lauching create_CE_MM script on the WMS node. WMS = ' + wms)
   logger.info('Command is: ' + cmd)
   stream = os.popen(cmd)
   lines = stream.readlines()
#   print lines
   for line in lines:
      if line.find('FILE CREATED') != -1 :
         linesp = line.split('=')
         filename = linesp[len(linesp) - 1] 
         logger.info('Found string FILE CREATED. FILENAME = ' + filename)

   ###########################################################################
   # Launching send_CE_MM to retrive collected data
   # if EOF is found I can go on and write data to wmsmon db
   # if TBC is found relaunch the send script untill EOF if found
   # store all data collected and then go on with the db
   ############################################################################

   OID  = CEMM_send_OID

   occ = []
   num = []
   dataline = ''
   EOF = False


   cmd = "snmpget -v 3 -u " + snmpuser + " -l authNoPriv -a MD5 -A " + snmppasswd + ' ' + host + ' ' + OID + '.101.1' + ' -t ' + timeout
   
   while EOF == False :

      logger.info('Lauching send_CE_MM script on the WMS node. WMS = ' + wms)
      logger.info('Command is: ' + cmd)
      stream = os.popen(cmd)
      lines = stream.readlines()

      for line in lines:
         if line.find('START') != -1 :
            idx = line.find('START')

#START; 1 1;2 2;3 3;4 4;5 5;1 1;2 2;3 3;4 4;5 5;1 1;2 2;3 3;4 4;5 5;1 1;2 2;3 3;4 4;5 5;1 1;2 2;3 3;4 4;5 5;1 1;2 2;3 3;4 4;5 5;1 1;2 2;3 3;4 4;5 5;1 1;2 2;3 3;4 4;5 5;1 1;2 2;3 3;4 4;5 5;1 1;2 2;3 3;49 4;50 5; TBC; END;#
            logger.info('Found line with data')
            dataline = dataline + line

            if line.find('EOF') != -1 :
               EOF = True
               logger.info('This is also the last line')


# Now we have to parse dataline to extract data

         linesp = line[idx:].split(';')
         i = 1
         str = ''
         while str != 'END' :
            str = linesp[i]
            str = str.strip().rstrip()
            i = i + 1
 #           print str
            if str != 'TBC' and str != 'EOF' and str != 'END':
               occ_num = str.split()     # This list contains one entry the occurrence and ce number
               occ.append(occ_num[0])
               num.append(occ_num[1])
            elif str == 'EOF' :
               continue

###########################################
#  Writing to the db the data collected   #
###########################################

print occ
print num
