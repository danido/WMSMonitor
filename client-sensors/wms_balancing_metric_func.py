#! /usr/bin/python
# Main program to call sensor functions

def wms_balancing_metric(WMS):
	'''wms_balancing_metric() -> returning a list conatining:
           memusage,loadcpulimit,memlimit,disklimit,fdrain,fload,ftraversaltime
           metric for wms load balancing is:
	      <0 if (service is failing)||(service is in drain)
	      >0 if (service is available ) N.B. the higher the number the higher the load on wms
           Return None if errors are raised during calculation.
	'''

	import os, commands, sys, fpformat
        sys.path.append('../../common')
        sys.path.append('../../common/classes')
	import time, urllib
	import datetime
	import readconf_func
	import f_metric_func
        import wms_class
        import socket 

	#Initializing 
        import logging
        logger = logging.getLogger('wms_balancing_metric')


        def mk_float_or_0(val):
           try:
              fval = float(val)
           except:
              return 0
           return fval

	confvar=readconf_func.readconf()
	fdrain=1
	fload=1
	ftraversaltime=1
        loadcpulimit = 15
        memlimit = 99
        memusage = 1
        disklimit = 90
        wmsdata = []

        ###########   LOAD BALANCING PARAMETERS    #####################
        LATENCY = 0 #confvar.get('LATENCY')
        LATENCY_PATH = ' ' #confvar.get('LATENCY_PATH')
        SUBMISSION_TEST = 0 # confvar.get('SUBMISSION_TEST')
        NAGIOS_PATH = ' ' #confvar.get('NAGIOS_PATH')
        LOAD_BALANCING_SITE_CONTACT = 'root@localhost' #confvar.get('LOAD_BALANCING_SITE_CONTACT')
        ####################################################



	#Calculating fdrain component
	#checks on daemons
        logger.info('checking daemons')
        for dae in WMS.daemons_dict.itervalues():
           if dae != '0' and dae != 'Null':
              logger.info('fdrain = -1 because of daemons:' + str(dae))
              fdrain = -1
              break
         
        env_script = confvar.get('ENV_FILE')

        #checkung whether the wms has been manually put in drain 
        cmddrain = '. ' + env_script + '; echo $GLITE_LOCATION_VAR'
        stddrain = os.popen(cmddrain)
        strtmp = stddrain.readlines()
        drainfile = strtmp[0].strip() + '/.drain'
	if  (os.access(drainfile,os.F_OK) == True):
              logger.info('fdrain = -1 because of drainfile presence')
              fdrain = -1

	#checking whether the wms is in autodrain for overload detection
#cmd = "grep glite_wms_wmproxy_load_monitor ${GLITE_LOCATION}/etc/glite_wms.conf |grep jobSubmit"
        cmdwmsconfig = '. ' + env_script + '; echo $GLITE_WMS_CONFIG_DIR'
        stddrain = os.popen(cmdwmsconfig)
        strtmp = stddrain.readlines()
        WMSFILE = strtmp[0].strip() + '/glite_wms.conf'
	cmd = "grep glite_wms_wmproxy_load_monitor " + WMSFILE + " |grep jobSubmit"
	std = os.popen(cmd)
        stdstr1 =  std.readlines() 
# if everything is ok....
	if ( len(stdstr1) > 0 ):
	      cmd= ". " + env_script + ";" + stdstr1[0][stdstr1[0].find("\"")+1:stdstr1[0].find("\"", stdstr1[0].find("\"")+1)] 
              logger.info("invoking jobsubmit script: " +cmd)
	      status=os.system(cmd + ' > /dev/null 2>&1')
              if (status != 0):
                      logger.info('fdrain = -1 because the command failed. Cmd is:')
                      logger.info(cmd)
                      fdrain=-1
              std = os.popen(cmd)
              stdstr =  std.readlines()
   	      if ( len(stdstr) > 0 ) :
		      if  (stdstr[2].split()[2] == 'Load') & (stdstr[2].split()[3].find('15')>0):                   
			   loadcpulimit=stdstr[2].split()[5];
		      else:
	  		   logger.error("Unable to find LoadCPU parsing the /sbin/glite_wms_wmproxy_load_monitor wmsdata")
                           return None
                      if  (stdstr[3].split()[2] == 'Memory'):
                           memlimit=stdstr[3].split()[4]
                           memusage=stdstr[3].split()[len(stdstr[3].split())-1]
                           memusage=memusage[0:memusage.find('%')]
                      else:
                           logger.error("Unable to find Memory Usage parsing the /sbin/glite_wms_wmproxy_load_monitor wmsdata")
                           return None
                      if  (stdstr[7].split()[2] == 'Disk'):
                           disklimit=stdstr[7].split()[4]
			   disklimit=disklimit[0:disklimit.find('%')]
                      else:
                           logger.error("Unable to find Disk Usage Limit parsing the /sbin/glite_wms_wmproxy_load_monitor wmsdata")
                           return None
 
	else : 
  	      logger.error("Problem reading glite_wms.conf file")
              return None
	
	#if status == 1:
	#      fdrain = -1;

        server_hostname = socket.getfqdn()

        #Site Nagios Submission Test       
        nagiossubtest = 1
        if SUBMISSION_TEST == '1':
                nagiossubtest = 1
                cmd1 = 'wget -q ' + NAGIOS_PATH
                logger.info("BALANCING COMMAND: " + cmd1 )
                if ( os.system(cmd1) == 0 ):
                   #checking date
                   cmdcheck = 'grep ' + server_hostname + ' ' + NAGIOS_PATH.split('/')[NAGIOS_PATH.count('/')]
                   std = os.popen(cmdcheck)
                   stdstr =  std.readlines()
                   if ( len(stdstr) > 0 ):
                      timestr = stdstr[0].split('\t')[0] 
                      deltatime = int(time.time())-int(time.mktime(time.strptime(timestr,"%Y-%m-%d %H:%M:%S")))
                      logger.info("NAGIOS DELTATIME: " + deltatime )
                      print "NAGIOS DELTATIME: ", deltatime,'\n' 
                      if (deltatime < 3600) :
                              logger.info("NAGIOS CURRENT STATUS SUBTEST: " + stdstr[0].split('\t')[1] )
                              if stdstr[0].split('\t')[1] == '2':
                                      nagiossubtest = -1
                              elif stdstr[0].split('\t')[1] == '3':
				      SENDMAIL = "/usr/sbin/sendmail" # sendmail location
				      p = os.popen("%s -t" % SENDMAIL, "w")
				      p.write("To: " + LOAD_BALANCING_SITE_CONTACT + "\n")
				      p.write("Subject: WARNING NAGIOS LOAD BALANCING SUBMISSION TEST FAILS\n")
				      p.write("\n") # blank line separating headers from body
				      p.write("WARNING: SUBMISSION TEST TOO OLD!!!\n\n\n")
				      p.write("FILE : " + NAGIOS_PATH +  "\n")
				      sts = p.close()
				      if sts != 0:
                                         logger.info("Sendmail exit status" + str(sts))

                      else:
			      SENDMAIL = "/usr/sbin/sendmail" # sendmail location
			      p = os.popen("%s -t" % SENDMAIL, "w")
			      p.write("To: " + LOAD_BALANCING_SITE_CONTACT + "\n")
			      p.write("Subject: WARNING NAGIOS LOAD BALANCING SUBMISSION TEST FAILS\n")
			      p.write("\n") # blank line separating headers from body
			      p.write("WARNING: SUBMISSION TEST TOO OLD!!!\n\n\n")
			      p.write("FILE : " + NAGIOS_PATH + "\n")
                              p.write("For wmsserver: " + server_hostname + "\n")
                              sts = p.close()
                              if sts != 0:
                                 logger.info("Sendmail exit status" + str(sts))
                   cmdrm = 'rm -f ' + NAGIOS_PATH.split('/')[NAGIOS_PATH.count('/')]
                   status=os.system(cmdrm + ' 2&>1')

                else :
                   SENDMAIL = "/usr/sbin/sendmail" # sendmail location
                   p = os.popen("%s -t" % SENDMAIL, "w")
                   p.write("To: " + LOAD_BALANCING_SITE_CONTACT + "\n")
                   p.write("Subject: WARNING NAGIOS LOAD BALANCING SUBMISSION TEST FAILS\n")
                   p.write("\n") # blank line separating headers from body
                   p.write("WARNING: COULD NOT READ SUBMISSION TEST RESULTS!!!\n")
                   p.write("PROBLEMS WHILE DOWNLOADING FILE : " + NAGIOS_PATH + "\n")
                   p.write("For wmsserver: " + server_hostname + "\n")
                   sts = p.close()
                   if sts != 0:
                      logger.info("Sendmail exit status" + str(sts))

        if fdrain > 0:
               fdrain = fdrain * nagiossubtest
 
        #CMS Latency Monitor Submission Test
        latencysubtest = 1
        if LATENCY == '1':
		cmd1 = 'wget -q ' + LATENCY_PATH + server_hostname + '.log'
		if ( os.system(cmd1) == 0 ):
		   #checking date
		   cmdcheck = 'tail -1 submit-tracks_' + server_hostname + '.log |awk \'{print $1}\''
		   std = os.popen(cmdcheck)
		   stdstr =  std.readlines()
		   if ( len(stdstr) > 0 ):
		      timestr = stdstr[0].strip(':\n')
		      deltatime = int(time.time())-int(time.mktime(time.strptime(timestr,"%Y-%m-%d@%H.%M.%S")))

		   if deltatime < 1800:
		      cmd2 = 'tail -1 submit-tracks_' + server_hostname + '.log|grep -c " done in"'
		      std = os.popen(cmd2)
		      stdstr =  std.readlines()
		      if ( len(stdstr) > 0 ) :
			 latencysubtest = int(stdstr[0].strip('\n'))
			 if latencysubtest == 0:
			    latencysubtest = -1
		   else:
		      SENDMAIL = "/usr/sbin/sendmail" # sendmail location
		      p = os.popen("%s -t" % SENDMAIL, "w")
		      p.write("To: " + LOAD_BALANCING_SITE_CONTACT + "\n")
		      p.write("Subject: WARNING LATENCY LOAD BALANCING SUBMISSION TEST FAILS\n")
		      p.write("\n") # blank line separating headers from body
		      p.write("WARNING: SUBMISSION TEST TOO OLD!!!\n\n\n")
		      p.write("FILE : " + LATENCY_PATH + server_hostname + ".log\n")
		      sts = p.close()
		      if sts != 0:
			 logger.info("Sendmail exit status" + str(sts))
		else :
		   SENDMAIL = "/usr/sbin/sendmail" # sendmail location
		   p = os.popen("%s -t" % SENDMAIL, "w")
                   p.write("To: " + LOAD_BALANCING_SITE_CONTACT + "\n")
		   p.write("Subject: WARNING LATENCY LOAD BALANCING SUBMISSION TEST FAILS\n")
		   p.write("\n") # blank line separating headers from body
		   p.write("WARNING: COULD NOT READ SUBMISSION TEST RESULTS!!!\n")
		   p.write("PROBLEMS WHILE DOWNLOADING FILE : " + LATENCY_PATH + server_hostname + ".log\n")
		   sts = p.close()
		   if sts != 0:
		      logger.info("Sendmail exit status" + str(sts))

        if fdrain > 0:
               fdrain = fdrain * latencysubtest

	#Calculating load metric
	logger.info("Building load metric")
#	print disklimit

	fload = f_metric_func.f_metric( mk_float_or_0(WMS['cpu_load']) , loadcpulimit, 0 ) + f_metric_func.f_metric( memusage , memlimit, 1 ) + f_metric_func.f_metric( mk_float_or_0(WMS['disk_sandbox']) , disklimit , 1 )

	#Calculating traversaltime  metric
	ftraversaltime =  min(f_metric_func.f_metric( mk_float_or_0(WMS['wm_queue']) , 500 , 0 ) , 1 ) + min(f_metric_func.f_metric(mk_float_or_0(WMS['jc_queue']) , 500 , 0 ) , 1 ) + min(f_metric_func.f_metric( mk_float_or_0(WMS['lb_event']) , 3000 , 0 ) , 1 )

	#summing metric components 
 
	if fdrain > 0:
		load_balancing_metric = fload + ftraversaltime
	else:
	        load_balancing_metric = fdrain

	#writing resulting metric to file
	filename = confvar.get('LOAD_BALANCING_FILENAME')
        try:
            logger.info('Trying to open file : ' + filename )
 	    f=open(filename, mode = 'a')
        
	    logger.info("writing load balancing metric to file: fdrain=" + str(fdrain) + ", fload= " + str(fload) + ", ftraversaltime= " + str(ftraversaltime))
	    f.write(str(load_balancing_metric) + '\n')
	    f.close()
        except IOerror :
            logger.error('CANNOT ACCESS FILE : ' + filename ) 

#{'wm_queue':null_str,'jc_queue':null_str,'lb_event':null_str,'loadb_fdrain':null_str,'loadb_ftraversaltime':null_str,'loadb_fload':null_str,'loadb_fmetric':null_str,'condor_running':null_str,'condor_idle':null_str,'condor_current':null_str,'ism_size':null_str,'ism_entries':null_str,'gftp_con':null_str,'FD_WM':null_str,'FD_LM':null_str,'FD_JC':null_str,'FD_LL':null_str,'loadb_memusage':null_str,'ice_running':null_str,'ice_idle':null_str,'ice_pending':null_str,'ice_held':null_str,'ice_queue':null_str,'cpu_load':null_str}
        WMS['loadb_memusage'] = float(memusage)/float(memlimit)
        #WMS['loadcpulimit'] = loadcpulimit
        #WMS['memlimit'] = memlimit  #removed from class to be returned as %
        #WMS['disklimit'] = disklimit # removed from class to be returned as %
        WMS['loadb_fdrain'] = fdrain
        WMS['loadb_fload'] = fload
        WMS['loadb_ftraversaltime'] = ftraversaltime
        WMS['loadb_fmetric'] = load_balancing_metric
#        logger.info('memusage: ' + str(WMS['memusage']))
#        logger.info('fdrain: '+ str(WMS['fdrain']))
#        logger.info('fload: '+ str(WMS['fload']))
#        logger.info('ftraversaltime: '+ str(WMS['ftraversaltime']))
#        logger.info('fmetric: '+ str(WMS['fmetric']))

        #f=open('/tmp/loadbalancingtest.txt', mode = 'a')
        #strtest=  str(int(time.time())) + ' ' + str(load_balancing_metric) + ' ' + str(fdrain) + ' ' + str(fload) + ' ' + str(ftraversaltime) + ' ' + str(memusage) + ' ' + str(memlimit) + ' ' + WMS['load'] + ' ' + str(loadcpulimit) + ' ' + WMS['sandbox'] + ' ' + str(disklimit) + ' ' + WMS['input_fl'] + ' ' + '1000' + ' ' + WMS['queue_fl'] + ' ' + '1000' + ' ' + WMS['dg20'] + ' ' + '3000'
        #f.write(strtest + '\n')
        f.close()
        cmd3 = 'rm -f submit-tracks_' + server_hostname + '.log'
        os.system(cmd3)
      
        return 0
