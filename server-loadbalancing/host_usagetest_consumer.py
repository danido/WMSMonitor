#! /usr/bin/python
# Main program to call sensor functions
import os, commands, sys, fpformat
sys.path.append('/opt/WMSMonitor/common')
sys.path.append('/opt/WMSMonitor/collector/bin')
import logging
import logpredef

logger = logging.getLogger('host_usagetest_consumer')

def mail_notification(subject,body):     
      try:
           #sending mail....
           SENDMAIL = "/usr/sbin/sendmail" # sendmail location
           p = os.popen("%s -t" % SENDMAIL, "w")
           p.write("To: " + confvar.get('LOAD_BALANCING_SITE_CONTACT') + "\n")
           p.write(subject)
           p.write("\n") # blank line separating headers from body
           p.write(body)
           sts = p.close()
           if sts != 0:
              logger.info("Sendmail exit status" + str(sts))
      except Exception,e:     
           logger.error("ERROR SENDING MAIL: " + str(e))


def host_usagetest_consumer():
        '''host_usagetest_consumer() -> takes usage test results from producers of  
           such a metric ( 1-Nagios, 2-url of a UI) and populates WMSMonitor database
        '''

        import os, commands, sys, fpformat
        sys.path.append('../common')
        import time
        import datetime
        import readconf_func
        import logging
        import socket
        import MySQLdb
        import urllib

        confvar=readconf_func.readconf()

        #CONNECTING TO DB
        #Opening myslq db connection
        logger.info("Starting db connection")
        try:
            db = MySQLdb.connection(host=confvar.get('WMSMON_DB_HOST'),user=confvar.get('WMSMON_DB_USER'),passwd=confvar.get('WMSMON_DB_PWD'),db=confvar.get('WMSMON_DB_NAME'))

        except Exception,e:
            stri2= "ERROR CONNECTING TO WMSMonitor DB: " + str(e)
            logger.error(stri2)
            logger.error("ERROR: Please check mysql daemon is running and connection parameters are correct!")
            sys.exit(1)

        #+++++++++++++++++++++++++++++
        # GETTING SUBMISSION TEST RESULT FOR EACH ALIAS
        # subtest_enable==  1=> ulr with test result in agreed format
        # subtest_enable==  2=> nagios test result !! TBD!!!
        try:
              logger.info("Reading alias list from Database")
              querystr="select alias_name, numout, subtest_enable, idalias from admin_loadbalancing where enable_flag=1 and subtest_enable=1;"
              
              #INITIALIZATION
              aliases=[]
              numout=[]
              subtest_enable=[]
              idalias=[]
              
              logger.debug(querystr)
              db.query(querystr) 
              r = db.store_result()
              row = r.fetch_row(10000)
              host_vo_dict = {}
              if len(row) > 0:
                 for line in row:
                 #host_vo_dict[hostname]=[idhost,vo,service]
                    aliases.append(line[0])
                    numout.append(line[1])
                    subtest_enable.append(line[2])
                    idalias.append(line[3])          
        except Exception,e:
              str2= "ERROR READING ALIAS LIST FROM WMSMonitor DB: " + str(e)
              logger.error(str2)
              logger.error("ERROR: Please check query and DB status")
              sys.exit(1)              
        for ik in range(len(aliases)):
           logger.info('Working on alias: ' + aliases[ik])
           #+++++++++++++++++++++++++++++
           # GETTING SUBMISSION TEST RESULT FOR EACH wms in each ALIAS
           # GETTING wms in the alias
           logger.info("Reading wms list for considered alias")
           try: 
              idwmslist=[] 
              wmslist=[]        
              test_url=[]  
              querystr="select hostname,idwms,test_url from hosts join admin_wms_alias_list on hosts.idhost=admin_wms_alias_list.idwms where idalias=" + idalias[ik] +  " and spare_label='0';"
              logger.debug(querystr)
              db.query(querystr) 
              r = db.store_result()
              row = r.fetch_row(10000)
              host_vo_dict = {}
              if len(row) > 0:
                 for line in row:
                 #host_vo_dict[hostname]=[idhost,vo,service]
                    wmslist.append(line[0])
                    idwmslist.append(line[1])
                    test_url.append(line[2])
           except Exception,e:
              logger.error("ERROR READING WMS LIST FROM WMSMonitor DB: " + str(e))
              logger.error("ERROR: Please check query and DB status")
              sys.exit(1)      
              
           #++++++++++++++++++++++++++++++++
           #LOOP on wms in the alias
           for ij in range(len(wmslist)):
               # subtest_enable==  1=> ulr with test result in agreed format
               if   test_url[ij].find('wmsmon-submit-tracks.log'):          
                   try:
                       FOUND_FLAG=0 
                       f_input=urllib.urlopen(test_url[ij])
                       lines_test=f_input.readlines()
                       if len(lines_test) > 0:
                          for line1X in lines_test:
                             if line1X.split()[3]==wmslist[ij]:
                                FOUND_FLAG=1
                                try: 
                                    logger.debug("Working on wms: " + idwmslist[ij] + ", hostname: " + wmslist[ij])
                                    querystr="insert into host_usagetest(idhost, t_lastcheck, test_result) VALUES (" + idwmslist[ij] + ", '" + line1X.split()[0] + " " + line1X.split()[1] + "', " + line1X.split()[2] + ");"
                                    logger.debug(querystr)
                                    db.query(querystr) 
                                except Exception,e:
                                    logger.error("ERROR STORING TEST RESULT TO WMSMonitor DB: " + str(e))
                                    logger.error("query: " + querystr)
                          if FOUND_FLAG==0:
                             logger.error("WMS not found in test url provided: ")
                             raise  
                   except Exception,e:
                      logger.error("ERROR READING submission test result FROM " + test_url[ij] + ": " + str(e))
                      #sending mail....
                      mail_notification("Subject: WARNING LOAD BALANCING SUBMISSION TEST: " + test_url[ij] + " \n","WARNING: COULD NOT READ SUBMISSION TEST RESULTS!!!\n PROBLEMS WHILE DOWNLOADING FILE For wms alias: " +  aliases[ik] + "\n")                

               # subtest_enable==  2=> nagios test result 
               elif test_url[ij].find('nagios'):
                   pass
#                   try:
#                       logger.error("NAGIOS INPUT NOT HANDLED YET!")
#                       FOUND_FLAG=0 
#                       f_input=urllib.urlopen(test_url[ij])
#                       lines_test=f_input.readlines()
#                       if len(lines_test) > 0:
#                          for line1X in lines_test:
#                             if line1X.split()[3]==wmslist[ij]:
#                                FOUND_FLAG=1
#                                try: 
#                                    querystr="insert into host_usagetest(idhost, t_lastcheck, test_result) VALUES (" + idwmslist[ij] + ", '" + line1X.split()[0] + " " + line1X.split()[1] + "', " + line1X.split()[2] + ");"
#                                    db.query(querystr) 
#                                except Exception,e:
#                                    logger.error("ERROR STORING TEST RESULT TO WMSMonitor DB: " + str(e))
#                                    logger.error("query: " + querystr)
#                          if FOUND_FLAG==0:
#                             logger.error("WMS not found in test url provided: ")
#                             raise  
#                   except Exception,e:
#                      logger.error("ERROR READING submission test result FROM " + test_url[ij] + ": " + str(e))
#                      #sending mail....
#                      mail_notification("Subject: WARNING LOAD BALANCING SUBMISSION TEST: " + test_url[ij] + " \n","WARNING: COULD NOT READ SUBMISSION TEST RESULTS!!!\n PROBLEMS WHILE DOWNLOADING FILE For wms alias: " +  aliases[ik] + "\n")                

               else:
                  logger.error("ERROR SUBTEST URL NOT VALID: " + subtest_enable[ik])
                
                
host_usagetest_consumer()
