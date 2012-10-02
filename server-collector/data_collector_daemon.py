#!/usr/bin/python
# Python import
import sys, time
from daemon_class import Daemon
import os, commands, sys, fpformat
import MySQLdb,time,datetime
import logging
import logpredef
import readconf_func
import collector_wms_class
import collector_lb_class


class MyDaemon(Daemon):
        #def __init__(self, pidfile, stdin='/tmp/WMSMonitor_data_collector.err', stdout='/tmp/WMSMonitor_data_collector.err', stderr='/tmp/WMSMonitor_data_collector.err'):
        def __init__(self, pidfile, stdin='/dev/null', stdout='/dev/null', stderr='/dev/null'):
                self.stdin = stdin
                self.stdout = stdout
                self.stderr = stderr
                self.pidfile = pidfile

        def run(self):
		#INIZIALIZATION
		logger = logging.getLogger('data_collector')
		TIME_AT_START = time.time()
                logger.info('THIS IS WMSMonitor data_collector_daemon')
		logger.info('Reading wmsmon conf file')
		confvar=readconf_func.readconf();

		#CONNECTING TO DB
		#Opening myslq db connection
		logger.info("Starting db connection")
		try:
		      db = MySQLdb.connection(host=confvar.get('WMSMON_DB_HOST'),user=confvar.get('WMSMON_DB_USER'),passwd=confvar.get('WMSMON_DB_PWD'),db=confvar.get('WMSMON_DB_NAME'))

		except Exception,e:
		      str= "ERROR CONNECTING TO WMSMonitor DB: " + str(e)
		      logger.error(str)
		      logger.error("ERROR: Please check mysql daemon is running and connection parameters are correct!")
                      sys.exit(1)
		#READING wms list from WMSMonitor DB
		querystr="select hostname,hosts.idhost,vo,service from admin_host_labels inner join hosts on hosts.idhost=admin_host_labels.idhost where admin_host_labels.active='1';"

		logger.info('READING wms list from WMSMonitor DB')
		logger.info(querystr)
		db.query(querystr) 
		r = db.store_result()
		row = r.fetch_row(10000)
		host_vo_dict = {}
		if len(row) > 0:
		   for line in row:
		       #host_vo_dict[hostname]=[idhost,vo,service]
		       host_vo_dict[line[0]]=line[1:]

		#CHECKING ACTIVEMQ MSG PATH
		if (os.access(confvar.get('ACTIVEMQ_MSGPATH'),os.F_OK) == False):
		    logger.error('NOT EXISTING DIRECTORY: ' + confvar.get('ACTIVEMQ_MSGPATH') + '. Please check wmsmon_defaults configuration file\n')
		    sys.exit(1)
                logger.info('CLOSING DB CONNECTION')
                db.close()
		#Starting daemon
		while True:
		      #Checking for new DATA Messages
		      list1=os.listdir(confvar.get('ACTIVEMQ_MSGPATH'))
                      if len(list1) == 0:
                          continue
                      logger.info("Starting db connection")
                      try:
                         db = MySQLdb.connection(host=confvar.get('WMSMON_DB_HOST'),user=confvar.get('WMSMON_DB_USER'),passwd=confvar.get('WMSMON_DB_PWD'),db=confvar.get('WMSMON_DB_NAME'))

                      except Exception,e:
                         str= "ERROR CONNECTING TO WMSMonitor DB: " + str(e)
                         logger.error(str)
                         logger.error("ERROR: Please check mysql daemon is running and connection parameters are correct!")
                         sys.exit(1)

		      for msg in list1:
			  wmsflag = 0
			  lbflag = 0
			  if ((os.access(confvar.get('ACTIVEMQ_MSGPATH') + '/' + msg,os.F_OK) == True) and (os.path.getsize(confvar.get('ACTIVEMQ_MSGPATH') + '/' + msg)>0)):
			      #ACCESSING ACTIVEMQ MSG FILE
			      logger.info('Working on file: ' + msg)
			      msghdl = open(confvar.get('ACTIVEMQ_MSGPATH') + '/' + msg,'r')
			      lines = msghdl.readlines()

			      #INITIALIZING MSG HOST VARIABLES
			      hostname = msg.split('_')[0]
			      line = lines[4]

			      #MESSAGE CHECKS: Is message from registered Instance?
			      if hostname not in host_vo_dict.keys():
				 #CHECKING WHETHER WMS IS REGISTERED
				 logger.debug('FOUND MSG FROM HOSTNAME NOT REGISTERED IN DB: ' + hostname)
                                 msghdl.close()
                                 #removing msg file to old                   
                                 os.system('rm -f ' + confvar.get('ACTIVEMQ_MSGPATH') + '/' + msg)
				 continue


			      msgepochtime = [line.split()[7].strip() for line in lines if line.startswith('DATA COLLECTION COMPLETED ON:')][0]
			      try:
				 logger.info('DATA COLLECTED ON:' + msgepochtime)
			      except:
				 logger.error('ERROR: could not read time of data collection in msg: ' + msg)
				 msghdl.close()
				 msgepochtime = 0
				 continue
			      msghdl.seek(0)

			      #TREATING WMS and LB data sources separately
			      if msg.find('WMS-SENSOR')>0:
				 #MSG IS FROM A WMS SERVICE
				 ###############################################
				 wmsflag = 1
                                 logger.info('THIS IS A WMS SERVER')

				 #DATA HANDLING
				 hostname_obj = collector_wms_class.collectorwms(hostname)
				 hostname_obj.VO = host_vo_dict[hostname_obj.host][1]
				 hostname_obj.idhost = host_vo_dict[hostname_obj.host][0]
				 hostname_obj.STARTDATE = [line.split('=')[1].strip() for line in lines if line.startswith('STARTDATE =')][0]
				 hostname_obj.ENDDATE = [line.split('=')[1].strip() for line in lines if line.startswith('ENDDATE =')][0] 
				 try:
				      logger.info('Loading wms values from file: ' + msg)
				      hostname_obj.load_wmsdata_file(msghdl)
				      logger.info('Storing wms values into database')
				      hostname_obj.store_wms_to_db(db)
				 except Exception,e:
				      logger.error("ERROR Loading wms values from file / Storing to db:" + e)
				 try:
				      logger.info('Loading user job data values from file: ' + msg)
				      hostname_obj.load_user(msghdl)
				      logger.info('Storing user mapping values into database')
				      hostname_obj.store_user_to_db(db)
				 except Exception,e:
				      logger.error("ERROR Loading user job data values from file / Storing to db::" + e)
				 try:
				      logger.info('Loading wms rate data values from file: ' + msg)
				      hostname_obj.load_wmsratedata_file(msghdl)
				      logger.info('Storing wms rate values into database')
				      hostname_obj.store_wmsratedata_to_db(db)
				 except Exception,e:
				      logger.error("ERROR Loading wmsratedata values from file / Storing to db:" + e)

				 try:
				      logger.info('Loading CE_MM values from file: ' + msg)
				      hostname_obj.load_ce_mm_dict(msghdl)
				      logger.info('Storing CE_MM values into database')
				      hostname_obj.store_cemm_to_db(db) 
				 except Exception,e:
				      logger.error("ERROR Loading CE_MM values from file / Storing to db:" + e)
				
				 try:
				      logger.info('Loading CE DATA values from file: ' + msg)
				      hostname_obj.load_ce_data(msghdl)
				      logger.info('Storing CE DATA values into database: ' + msg)
				      hostname_obj.store_ce_data_to_db(db)  
				 except Exception,e:
				      logger.error("ERROR Loading CE_MM values from file / Storing to db:" + e)

				 try:                
				      logger.info('Loading GLOBUS_ERROR_STATS values from file: ' + msg)
				      hostname_obj.load_globus_error_data(msghdl)
				      logger.info('Loading CREAM_ERROR_STATS values from file: ' + msg)
				      hostname_obj.load_cream_error_data(msghdl)
				      logger.info('Storing ERROR_STATS values into database: ' + msg)
				      hostname_obj.store_jss_error_data_to_db(db) 
				 except Exception,e:
				      logger.error("ERROR Loading ERROR_STATS values from file / Storing to db:" + e)

				 try:
				      logger.info('Loading lbhist values from file: ' + msg)
				      hostname_obj.load_lbhist(msghdl)
				      logger.info('Storing lbhist values into database')
				      hostname_obj.store_lbhist_to_db(db)
				 except Exception,e:
				      logger.error("ERROR Loading lbhist values from file / Storing to db:" + e)

				 logger.info('DATA Handling terminated for host: ' + hostname)
				 msghdl.close()
				 #moving msg file to old                   
				 os.system('mv -f ' + confvar.get('ACTIVEMQ_MSGPATH') + '/' + msg + ' ' +  confvar.get('OLDMQ_MSGPATH') + '/')

			      elif msg.find('LB-SENSOR')>0:
				 #MSG IS FROM A LB SERVICE
				 ################################################
                                 logger.info('THIS IS A LB SERVER')
				 lbflag = 1
				 #DATA HANDLING 
				 hostname_obj = collector_lb_class.collectorlb(hostname)
				 hostname_obj.VO = host_vo_dict[hostname_obj.host][1]
				 hostname_obj.idhost = host_vo_dict[hostname_obj.host][0]
#				 hostname_obj.STARTDATE = [line.split('=')[1].strip() for line in lines if line.startswith('STARTDATE =')][0]
#				 hostname_obj.ENDDATE = [line.split('=')[1].strip() for line in lines if line.startswith('ENDDATE =')][0]

				 try:
				     logger.info('Loading lb values from file: ' + msg)
				     hostname_obj.load_lbdata_file(msghdl)
				     logger.info('Storing lb values into database')
				     hostname_obj.store_lb_to_db(db)
				 except Exception,e:
				      logger.error("ERROR Loading lbdata values from file / Storing to db:" + e)

				 logger.info('DATA Handling terminated for host: ' + hostname)
				 msghdl.close()
				 #moving msg file to old                  
                                 os.system('mv -f ' + confvar.get('ACTIVEMQ_MSGPATH') + '/' + msg + ' ' +  confvar.get('OLDMQ_MSGPATH') + '/')
			      else: 
				 logger.error('ERROR: could not determine service nature in msg : ' + msg)
			      
			  else:
			      logger.error('PROBLEM ACCESSING FILE or ZERO SIZE FILE: ' + msg + '. MOVING  IT to OLDMSG directory\n')
			      os.system('mv -f ' + msg + ' ' +  confvar.get('OLDMQ_MSGPATH') + '/')

		      logger.info("Closing db connection")
		      db.close()
		      os.system('sleep 5')
		     
if __name__ == "__main__":
        daemon = MyDaemon('/tmp/data_collector.pid')
        if len(sys.argv) == 2:
                if 'start' == sys.argv[1]:
                        print "STARTING WMSMONITOR DATA COLLECTOR ..."
                        daemon.start()
                elif 'stop' == sys.argv[1]:
                        print "STOPPING WMSMONITOR DATA COLLECTOR ..."
                        daemon.stop()
                        print "STOP OK"
                elif 'restart' == sys.argv[1]:
                        print "RESTARTING WMSMONITOR DATA COLLECTOR ..."
                        daemon.restart()
                else:
                        print "Unknown command"
                        sys.exit(2)
                sys.exit(0)
        else:
                print "usage: %s start|stop|restart" % sys.argv[0]
                sys.exit(2)




