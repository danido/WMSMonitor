#!/usr/bin/python

import os, commands, sys, fpformat
import MySQLdb,time,datetime
import logging
import logpredef
import readconf_func


logger = logging.getLogger('create_daily')

if len(sys.argv) < 2:
   print "\nUsage:\n"
   print "create_daily.py \PATH\wmsmon.conf\n"
   sys.exit(1)

conf_file = sys.argv[1]      #CONFIGURATION FILE REPORTING A LINE FOR EACH WMS TO MONITOR WITH
                             # WMS_HOST WMS_HOST_PORT LB_HOST DB_LB_USER DB_LB_PASSWD DB_LB_NAME
                             #EXAMPLE...
                             #wms002.cnaf.infn.it egee-rb-06.cnaf.infn.it multi 

logger.info('Reading wmsmon conf file')

#READ wmsmon.conf file
if (os.access(sys.argv[1],os.F_OK) == True):
      lsstr = open(sys.argv[1],'r')
      lines = lsstr.readlines()
      for line in lines:
         line_tmp = line.split()
         if len(line_tmp) < 3:
             logger.error("check data in lines of \PATH\wmsmon.conf file. Exiting...\n")
             sys.exit(1)
         #initializing some variables
	 logger.info('Reading wmsmon conf file')
	 confvar=readconf_func.readconf();
	 wmshost = line_tmp[0]
         wmshostport = confvar.get('PORT')
         lbhost = line_tmp[1]
         VO = line_tmp[2]
         dbhost = confvar.get('WMSMON_DB_HOST')
         dbuser = confvar.get('LB_DB_USER')
         dbname = confvar.get('LB_DB_NAME')
         STEPDATE = int(confvar.get('STEPDATE'))

         logger.info("Starting db connection")
         db = MySQLdb.connection(host=confvar.get('WMSMON_DB_HOST'),user=confvar.get('WMSMON_DB_USER'),passwd=confvar.get('WMSMON_DB_PWD'),db=confvar.get('WMSMON_DB_NAME'))
         
         logger.info("Determining start and date")
         # normally these would be the values .....

         STARTDATE = time.strftime("%Y-%m-%d 00:05:00", time.localtime())
         ENDDATE =   time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())
         DBDATE = ENDDATE

         # but if we are at the very beginning of the day (between midnight and 01:00:00  (this should be parametrized)
         # run the query for the whole day before, this is done to prevent loss of day near midnight of the same day
         # So....
         
         now = time.localtime()
         num_sec_day = 3600 * 24
         
         if now[3] == 0 :   # we are around midnight
            logger.info("Ehi, we're around midnight, querying for the whole yesterday.") 
            YESTERDAY_START_epoch = time.mktime(time.localtime()) - (num_sec_day - 150)
            STARTDATE = time.strftime("%Y-%m-%d 00:05:00", time.localtime(YESTERDAY_START_epoch))   #Adding 5 minutes to avoid first data
            ENDDATE = time.strftime("%Y-%m-%d 00:05:00", time.localtime()) #Adding 5 minutes to catch the first query of the day
            logger.info("STARTDATE = " + STARTDATE +  "   ENDDATE = " + ENDDATE)
            DBDATE = time.strftime("%Y-%m-%d 23:59:59", time.localtime(YESTERDAY_START_epoch))
         querystr="select sum(WMP_in), sum(WMP_in_col), sum(WM_in), sum(WM_in_res), sum(JC_in), sum(JC_out), sum(JOB_DONE), sum(JOB_ABORTED) from lbsensor where wms='" + wmshost + "' and lbserver = '" + lbhost + "' and date >= '" + STARTDATE + "' and date < '" + ENDDATE + "' limit 1;"

         logger.info("Launching query to sum data.  Query is:")
         logger.info(querystr)

         db.query(querystr)
         r = db.store_result()
         row = r.fetch_row()
         if len(row) > 0:
             wmp_in_sum  = row[0][0]
             wmp_in_col_sum = row[0][1]
             wm_in_sum = row[0][2]
             wm_in_res_sum  = row[0][3]
             jc_in_sum = row[0][4]
             jc_out_sum = row[0][5]
             job_done_sum = row[0][6]
             job_aborted_sum = row[0][7]

         querystr="select avg(WMP_in_col_avg), avg(WMP_in_col_std) from lbsensor where wms='" + wmshost + "' and lbserver = '" + lbhost + "' and date >= '" + STARTDATE + "' and date < '" + ENDDATE + "' limit 1;"

         logger.info("Launching query to find the avg and std of collection nodes .  Query is:")
         logger.info(querystr)

         db.query(querystr)
         r = db.store_result()
         row = r.fetch_row()
         if len(row) > 0:
             wmp_in_col_avg_sum  = row[0][0]
             wmp_in_col_std_sum  = row[0][1]

         logger.info("Filling WMSMON DATABASE with LBresult Data")
         
         myquery="INSERT INTO `wmsmon`.`lbsensor_daily` (`ID_Rec`, `date`, `wms`,`lbserver`,`WMP_in`, `WMP_in_col`,`WMP_in_col_avg`,`WMP_in_col_std`, `WM_in`, `WM_in_res`, `JC_in`, `JC_out`,`JOB_DONE`,`JOB_ABORTED`,`VO`) VALUES (NULL,'" + DBDATE + "', '" + wmshost + "', '" + lbhost + "', '" + wmp_in_sum +"', '" + wmp_in_col_sum +"', '" + wmp_in_col_avg_sum + "', '" + wmp_in_col_std_sum + "', '" + wm_in_sum + "', '" + wm_in_res_sum + "', '" + jc_in_sum +"', '" + jc_out_sum + "','" + job_done_sum + "','" + job_aborted_sum +  "','" + VO + "');"

         print myquery
         logger.info('Query is: ' + myquery)
         db.query(myquery)

         db.close()
