#! /usr/bin/python
# Main program to call sensor functions

# Basic import

def lb_sensor(confvar):
	'''lb_sensor() -> list of string in the followind order:
        load     - machine load 15 as reported /proc/loadavg
        lb_disk  - / partition occupancy (in %)
        LB       - status of LB daemon (0 is ok)
        LL       - status of LL daemon (0 is ok)
        NTPD       - status of NTPD daemon (0 is ok)
        LB_CON   - number of connections established by LB
        lib_misql_disk   - /lib/mysql partition usage in %
	'''

	import os, commands, sys, fpformat
	#import MySQLdb
	import time
	#import datetime

	#Sensor functions import

	import load_func
	import lb_diskspace_checks_func
	import lb_connections_func
        import lb_daemons_status_func

        #Initializing logger
        import logging

        logger = logging.getLogger('lb_sensor')
         
	# Start main here

        #Inizialising LB_dict
        nullstr = 'Null'
        LB_dict = {'cpu_load':nullstr,'LB_CON':nullstr,'disk_lb':nullstr,'disk_varlibmysql':nullstr,'daemon_LB':nullstr,'daemon_LL':nullstr,'daemon_NTPD':nullstr}

	# Starting Calling sensor functions....
	# ....Then the average cpu load  in past 15 min
	logger.info("Calling load function")
	loadtmp=load_func.load_cpu()
	if loadtmp != None:
	   LB_dict['cpu_load'] = loadtmp

	# ....Then the number of TCP connections for LB server on ports 9000:9001:9002:9003
	logger.info("Calling lb_connections function")
        LB_CON = lb_connections_func.lb_connections()
	if LB_CON != None:
	   LB_dict['LB_CON'] = LB_CON

	# % of disk occupacy hosting Sandbox and tmp directories
	logger.info("Calling diskspace_checks function")
	output_tmp = lb_diskspace_checks_func.diskspace_checks(confvar.get('LB_DISC_PATH'),confvar.get('LB_DISC_LIB_MYSQL_PATH'))
	if output_tmp[0] != None:
	   LB_dict['disk_lb'] = output_tmp[0]
        if output_tmp[1] != None:
           LB_dict['disk_varlibmysql'] = output_tmp[1]

	#.... Then checking lb daemons status for 'glite-lb-bkserverd','glite-lb-locallogger'
	logger.info("Calling daemons status check  function")
	output_tmp=lb_daemons_status_func.daemons_status(confvar.get('LB_DAEMONS_PATH'),confvar.get('ENV_FILE'))
	if output_tmp[0]!=None:
	   LB_dict['daemon_LB'] = output_tmp[0]
	if output_tmp[1]!=None:
	   LB_dict['daemon_LL'] = output_tmp[1]
	if output_tmp[2]!=None:
	   LB_dict['daemon_NTPD'] = output_tmp[2]

      #Logging fields
        outputstr= str(LB_dict)
        logger.debug("LB values collected are:")
        logger.debug(outputstr)

	return LB_dict
