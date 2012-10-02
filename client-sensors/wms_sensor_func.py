#! /usr/bin/python

# Main program to call sensor functions

# Basic import

def wms_sensor():
	'''wms_sensor() -> list of string in the followind order:
        running  - running condor job as reported by condor_q
        idle     - idle condor job as reported by condor_q
        current  - current condor job as reported by condor_q
        load     - machine load 15 as reported /proc/loadavg
        input_fl - unprocessed entries in input.fl
        queue_fl - unprocessed entries in queue.fl
        dg20     - number of dg20logd files in /var/log/glite
        ism_size - ism size in 1kB blocks
        ism_entries - CE ism entries
        sandbox  - Sandbox partition occupancy (in %)
        tmp      - tmp partition occupancy (in %)
        gftp     - number of gftp process
        FD_WM    - number of file descriptors opened by WM
        FD_LM    - number of file descriptors opened by LM
        FD_JC    - number of file descriptors opened by JC
        FD_LL    - number of file descriptors opened by LL
        LB       - status of LB daemon (0 is ok)
        LL       - status of LL daemon (0 is ok)
        LBPX     - status of LBPX daemon (0 is ok)
        PX       - status of PX daemon (0 is ok)
        FTPD     - status of FTPD daemon (0 is ok)
        JC       - status of JC daemon (0 is ok)
        LM       - status of LM daemon (0 is ok)
        WM       - status of WM daemon (0 is ok)
        WMP      - status of WMP daemon (0 is ok)
        ICE      - status of ICE daemon (0 is ok)
        BDII      - status of BDII daemon (0 is ok)
        NTPD      - status of NTPD daemon (0 is ok)
        varlog   - /var/log partition occupancy (in %)
        varlibmysql - /var/lib/mysql partition occupancy (in %)
	'''

	import os, commands, sys, fpformat
        sys.path.append('../../common')
        sys.path.append('../../common/classes')
	#import MySQLdb
	import time
	import readconf_func
        import socket
	#Sensor functions import
	import condor_func
	import load_func
	import dg20_func
	import ism_stat_func
	import filelists_func
	import diskspace_checks_func
	import gftp_num_func
	import file_desc_func
	import daemons_status_func
	import wms_balancing_metric_func      
        import ice_jobs_func
        import wms_class
 
	#Initializing logger
        import logging
        logger = logging.getLogger('wms_sensor')
	
	confvar = readconf_func.readconf();

	# Starting Calling sensor functions....
####################################################################################
#### starting backgroung process, we will look at the end if they finished
####################################################################################

     ## NO MORE NEEDED
        #Launching in backgroud the creation of the mappping table
        #cmd = confvar['INSTALL_PATH'] + "/sensors/bin/wms_usermapping/wms_usermapping_func &"
        #os.system(cmd)
     #######################

        #Launching the creation of the CE_MM file in background
        cmd = confvar['INSTALL_PATH'] + "/sensors/bin/CE_MM.sh " + confvar['WORKLOAD_MANAGER_LOG_FILE'] + " " + confvar['CE_MM_FILE'] + " &"
        os.system(cmd)



######################################################################################
######################################################################################

	# The condor_jobs first...
	logger.info('Calling condor_jobs function')
	#Return a list of total, idle, running, held jobs as reported by condor_q

	condor_list = condor_func.condor_jobs(confvar.get('ENV_FILE'))
	if condor_list[2] != None:
	   running = condor_list[2]
	else:
	   running = 'Null'
	if condor_list[0] != None:
	   current = condor_list[0]
	else:
	   current = 'Null'
	if condor_list[1] != None:
	   idle = condor_list[1]
	else:
	   idle = 'Null'


        # ...Then the ice_jobs ...
        logger.info('Calling ice_jobs function')
        #Return a list of total, idle, running, held jobs as reported by icedb tool
        ice_dict = ice_jobs_func.ice_jobs(confvar['ENV_FILE'])

	# ....Then the average cpu load  in past 15 min
        logger.info('Calling load function')
	loadtmp=load_func.load_cpu()
	if loadtmp != None:
	   load = loadtmp
	else:
	   load = 'Null'

	# Number of jobs in Input.fl and Queue.fl and ice.fl
        logger.info('Calling filelists function')
	filelist_tmp = filelists_func.filelists(confvar.get('ENV_FILE'))
        #print "filelists_tmp = " + str(filelist_tmp)
	if filelist_tmp[0] != None:
	   input_fl = filelist_tmp[0][0:len(filelist_tmp[0]) - 1]
	else:
	   input_fl = 'Null'
	if filelist_tmp[1] != None:
	   queue_fl = filelist_tmp[1][0:len(filelist_tmp[1]) - 1]
	else:
	   queue_fl = 'Null'
        if filelist_tmp[2] != None:
           ice_fl = filelist_tmp[2][0:len(filelist_tmp[1]) - 1]
        else:
           ice_fl = 'Null'

	# ....Then the number of dg20 files in the wms
	logger.info('Calling dg20log function')
	dg20 = dg20_func.dg20log( confvar.get('DG20_PATH'))
	if dg20 == None:
	   dg20 = 'Null'

        #...Then the ism status
        logger.info('Calling ism_stat function')
        ism_tmp = ism_stat_func.ism_stat(confvar.get('ISMDUMP_PATH'),confvar.get('GLITE_LOG_DIR'))
        if ism_tmp[0] == None:
           ism_tmp[0] = 'Null'
        if ism_tmp[1] == None:
           ism_tmp[1] = 'Null'
        ism_size = ism_tmp[0]
        ism_entries = ism_tmp[1]


	# % of disk occupacy hosting Sandbox and tmp directories
	logger.info("Calling diskspace_checks function")
	output_tmp=diskspace_checks_func.diskspace_checks(confvar.get('SANDBOX_PATH'),confvar.get('TMP_PATH'),confvar.get('VAR_LOG_PATH'),confvar.get('VAR_LIB_MYSQL_PATH'))
	if output_tmp[0] != None:
	   sandbox = output_tmp[0][0:len(output_tmp[0])]
	else:
	   sandbox = 'Null'
	if output_tmp[1] != None:
	   tmp = output_tmp[1][0:len(output_tmp[1])]
	else:
	   tmp = 'Null'
	if output_tmp[2] != None:
	   varlog = output_tmp[2][0:len(output_tmp[2])]
	else:
	   varlog = 'Null'
	if output_tmp[3] != None:
	   varlibmysql = output_tmp[3][0:len(output_tmp[3])]
	else:
	   varlibmysql = 'Null'


	# ....Then the number of gridftp sessions in the wms
	logger.info("Calling gftp_num function")
	if gftp_num_func.gftp_num() != None:
	   gftp = gftp_num_func.gftp_num()
	else:
	   gftp = 'Null'

	#.... Then file descriptors for  WM,LM,JC,LL
	logger.info("Calling file descriptor function")
	output_tmp=file_desc_func.file_desc(confvar.get('FD_WMS_WM'),confvar.get('FD_WMS_LM'),confvar.get('FD_WMS_JC'),confvar.get('FD_WMS_LBINTERLOG'))
	if output_tmp[0] != None:
	   FD_WM = output_tmp[0]
	else:
	   FD_WM = 'Null'
	if output_tmp[1] != None:
	   FD_LM = output_tmp[1]
	else:
	   FD_LM = 'Null'
	if output_tmp[2] != None:
	   FD_JC = output_tmp[2]
	else:
	   FD_JC = 'Null'
	if output_tmp[3] != None:
	   FD_LL = output_tmp[3]
	else:
	   FD_LL = 'Null'

	#.... Then checking wms daemons status for 'glite-lb-bkserverd','glite-lb-locallogger','glite-lb-proxy',
	#       'glite-proxy-renewald','glite-wms-ftpd','glite-wms-jc',
	#       'glite-wms-lm','glite-wms-wm','glite-wms-wmproxy''''
	logger.info("Calling daemons status check function")
	output_tmp=daemons_status_func.daemons_status(confvar.get('GLITE_DAEMONS_PATH'))
#        print 'daemons:', output_tmp, '\n'
#        print confvar.get('GLITE_DAEMONS_PATH')
	if output_tmp[0]!=None:
	   LL = output_tmp[0]
	else:
	   LL = 'Null'
	if output_tmp[1]!=None:
	   LBPX = output_tmp[1]
	else:
	   LBPX = 'Null'
	if output_tmp[2]!=None:
	   PX = output_tmp[2]
	else:
	   PX = 'Null'
	if output_tmp[3]!=None:
	   FTPD = output_tmp[3]
	else:
	   FTPD = 'Null'
	if output_tmp[4]!=None:
	   JC = output_tmp[4]
	else:
	   JC = 'Null'
	if output_tmp[5]!=None:
	   LM = output_tmp[5]
	else:
	   LM = 'Null'
	if output_tmp[6]!=None:
	   WM = output_tmp[6]
	else:
	   WM = 'Null'
	if output_tmp[7]!=None:
	   WMP = output_tmp[7]
	else:
	   WMP = 'Null'
	if output_tmp[8] != None:
	   ICE = output_tmp[8]
	else:
	   ICE = 'Null'
	if output_tmp[9] != None:
	   BDII = output_tmp[9]
	else:
	   BDII = 'Null'
	if output_tmp[10] != None:
	   NTPD = output_tmp[10]
	else:
	   NTPD = 'Null'

	#Logging fields

# Now we create the WMS object
        hostname = socket.getfqdn()
        WMS = wms_class.WMS(hostname)
 
        WMS['condor_running'] = str(running)
        WMS['condor_idle'] = str(idle)
        WMS['condor_current'] = str(current)
        WMS['ice_idle'] = str(ice_dict['IDLE'])
        WMS['ice_pending'] = str(ice_dict['PENDING'])
        WMS['ice_running'] = str(ice_dict['RUNNING'])
        WMS['ice_held'] = str(ice_dict['HELD'])
        WMS['cpu_load'] = str(load)
        WMS['wm_queue'] = str(input_fl)
        WMS['jc_queue'] = str(queue_fl)
        WMS['ice_queue'] = str(ice_fl)
        WMS['ism_size'] = str(ism_size)
        WMS['ism_entries'] = str(ism_entries)
        WMS['disk_sandbox'] = str(sandbox)
        WMS['disk_tmp'] = str(tmp)
        WMS['disk_varlog'] = str(varlog)
        WMS['disk_varlibmysql'] = str(varlibmysql)
        WMS['gftp_con'] = str(gftp)
        WMS['lb_event'] = dg20
        WMS['FD_WM'] = str(FD_WM)
        WMS['FD_LM'] = str(FD_LM)
        WMS['FD_JC'] = str(FD_JC)
        WMS['FD_LL'] = str(FD_LL)
        #WMS['LB'] = str(LB) # removed in 3.0
        #WMS.daemons_dict['LB'] = WMS['LB']   # removed in 3.0
        WMS['daemon_LL'] = str(LL)
        WMS.daemons_dict['daemon_LL'] = WMS['daemon_LL']
        WMS['daemon_LBPX'] = str(LBPX)
        WMS.daemons_dict['daemon_LBPX'] = WMS['daemon_LBPX']
        WMS['daemon_PX'] = str(PX)
        WMS.daemons_dict['daemon_PX'] = WMS['daemon_PX']
        WMS['daemon_FTPD'] = str(FTPD)
        WMS.daemons_dict['daemon_FTPD'] = WMS['daemon_FTPD']
        WMS['daemon_JC'] = str(JC)
        WMS.daemons_dict['daemon_JC'] = WMS['daemon_JC']
        WMS['daemon_LM'] = str(LM)
        WMS.daemons_dict['daemon_LM'] = WMS['daemon_LM']
        WMS['daemon_WM'] = str(WM)
        WMS.daemons_dict['daemon_WM'] = WMS['daemon_WM']
        WMS['daemon_WMP'] = str(WMP)
        WMS.daemons_dict['daemon_WMP'] = WMS['daemon_WMP']
        WMS['daemon_ICE'] = str(ICE)
        WMS.daemons_dict['daemon_ICE'] = WMS['daemon_ICE']
        WMS['daemon_BDII'] = str(BDII)
        WMS.daemons_dict['daemon_BDII'] = WMS['daemon_BDII']
        WMS['daemon_NTPD'] = str(NTPD)
        WMS.daemons_dict['daemon_NTPD'] = WMS['daemon_NTPD']

        logger.info('Calling wms_balancing_metric_func')
        metric_output = wms_balancing_metric_func.wms_balancing_metric(WMS)
       
        logger.debug("WMS values collected are:")
        logger.debug(str(WMS))
         
        
        # Before reuturning check if the wms_usermapping and CE_MM have finished
        # If not wait for a maximun of 30 seconds

        #logger.info("Waiting for usermap to complete its job")
        file_tmp = confvar['MAPTABLE_FILENAME']
        file_tmp2 = confvar['CE_MM_FILE']
        MAP_DONE = False
        MM_DONE = False
        LOOP_TIMEOUT = int( confvar['LOOP_TIMEOUT'] ) 
        START_LOOP_TIME = time.time()
        EXIT_THE_LOOP = False
        while EXIT_THE_LOOP == False and (time.time() - START_LOOP_TIME) < LOOP_TIMEOUT:
         #  if (os.access(file_tmp,os.F_OK) == True) and (os.WEXITSTATUS(os.system(("/usr/sbin/lsof " + file_tmp + " >/dev/null  2>&1"))) == 1):        
#   if (os.access(file_tmp,os.F_OK) == True) and (os.WEXITSTATUS(os.system(("/usr/sbin/lsof " + file_tmp ))) == 1) :
                  #yes, good, the files are accessible
        #          MAP_DONE = True
        #          logger.info("Usermap completed. Returning")
#           if (os.access(file_tmp2,os.F_OK) == True) and (os.WEXITSTATUS(os.system(("/usr/sbin/lsof " + file_tmp2 ))) == 1) :
           if (os.access(file_tmp2,os.F_OK) == True) and (os.WEXITSTATUS(os.system(("/usr/sbin/lsof " + file_tmp2 + " >/dev/null  2>&1"))) == 1):
                  #yes, good, the files are accessible
                  MM_DONE = True
                  logger.info("CE_MM completed. Returning")
           EXIT_THE_LOOP = MM_DONE

#        if MAP_DONE == False:
#           logger.warning("Usermap did not complete its job.")  #change this log message
        if MM_DONE == False:
           logger.warning("CE_MM did not complete its job.")  #change this log message

# now we should return  a wms object and the presence of the mapping file
        return WMS , MM_DONE
