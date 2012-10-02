#! /usr/bin/python
# Main program to call sensor functions
import os, commands, sys, fpformat
sys.path.append('/opt/WMSMonitor/collector/bin/')
import logging
import logpredef
logger = logging.getLogger('wms_balancing_arbiter')
import readconf_func
conf=readconf_func.readconf()
def mail_notification(subject,body):     
      try:
           #sending mail....
           SENDMAIL = "/usr/sbin/sendmail" # sendmail location
           p = os.popen("%s -t" % SENDMAIL, "w")
           p.write("To: " + conf.get('LOAD_BALANCING_SITE_CONTACT') + "\n")
           p.write(subject)
           p.write("\n") # blank line separating headers from body
           p.write(body)
           sts = p.close()
           if sts != 0:
              logger.info("Sendmail exit status" + str(sts))
      except Exception,e:     
           logger.error("ERROR SENDING MAIL: " + str(e))


def wms_balancing_arbiter():
        '''wms_balancing_arbiter() -> updating wms instances available behind an alias
           depending on the load of the instances according to the load metric provided by
           wms_balancing_metric function 
           Return None if errors are raised during calculation.
        '''

        import os, commands, sys, fpformat
        sys.path.append('../common')
        import time
        import datetime
        import readconf_func
        import logging
        import socket
        import MySQLdb
        import logpredef

        logger = logging.getLogger('wms_balancing_arbiter')
        conf=readconf_func.readconf()

        #+++++++++++++++++++++++++++++
        #Opening myslq db connection        
        try:
              db = MySQLdb.connection(host=conf.get('WMSMON_DB_HOST'),user=conf.get('WMSMON_DB_USER'),passwd=conf.get('WMSMON_DB_PWD'),db=conf.get('WMSMON_DB_NAME'))
              logger.info("Starting db connection")
        except Exception,e:
              strxx= "ERROR CONNECTING TO WMSMonitor DB: " + str(e)
              logger.error(strxx)
              logger.error("ERROR: Please check mysql daemon is running and connection parameters are correct!")
              sys.exit(1)
        
        print '\n','*************************************************************\n',time.strftime("%Y-%m-%d %H:%M:%S",time.localtime()), '*************************************************************\n'
        
        #+++++++++++++++++++++++++++++
        #STARTING LOOP ON ALL DEFINED ALIAS
        # TABLE: admin_loadbalancing ->  idalias, enable_flag, numout, subtest_enable, alias_name
        # TABLE: HOST_USAGETEST -> idhostusagetest, idhost (fk), t_lastcheck, test_vo, test_result
        # TABLE: admin_wms_alias_list ->  idlist, idalias, idwms, spare_label    
        try:
              logger.info("Reading alias list from Database")
              querystr="select alias_name, numout, subtest_enable, idalias from admin_loadbalancing where enable_flag='1';"
              
              #INITIALIZATION
              aliases=[]
              numout=[]
              subtest_enable=[]
              idalias=[]
              
              logger.info(querystr)
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
              strxx= "ERROR READING ALIAS LIST FROM WMSMonitor DB: " + str(e)
              logger.error(strxx)
              logger.error("ERROR: Please check query and DB status")
              sys.exit(1)              
        
        for ik in range(len(aliases)):
            logger.info('Working on alias: ' + aliases[ik])
            alias = aliases[ik]
            
            #initialization of lists
            posmetriclist=[]
            negmetriclist=[]
            wmsmetriclist=[]
            aliasnewlist=[]
            host=[]
            download_err_flag = 0

            #which wms alredy in the alias?
            cmd = 'host ' + alias + '.' + conf.get('DNS_ZONE')
            std = os.popen(cmd)
            stdstr =  std.readlines()
            if std.close():
                 print "ERROR: no hosts in alias:", alias
            else:
            #( len(stdstr) > 0 ):
                for line in stdstr:
                    host.append(line.split()[len(line.split())-1])
            #initialization of metric lists
            posmetriclist=[]
            negmetriclist=[]
            wmsmetriclist=[]
            aliasnewlist=[]
            download_err_flag = 0  

            #++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
            #LOOP ON ALL WMS IN THE ALIAS 
            try: 
               idwmslist=[] 
               wmslist=[]        
               test_url=[]  
               querystr="select hostname,idwms,test_url from hosts join admin_wms_alias_list on hosts.idhost=admin_wms_alias_list.idwms where idalias=" + idalias[ik] +  " and spare_label='0';"
               logger.info(querystr)
               db.query(querystr) 
               r = db.store_result()
               row = r.fetch_row(10000)
               if len(row) > 0:
                  for line in row:
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
                 wms = wmslist[ij]
                 idwms = idwmslist[ij]
                 subtest = 1
                 subtest_err_flag = 0 

                 #################################################################
                 #Integrating submission test results in the load balancing metric                 
                 if subtest_enable[ik]=='1':                     
                      test_result = 'Null'
                      try: 
                          querystr="select t_lastcheck,test_result from host_usagetest where idhost='" + idwms + "' order by t_lastcheck desc limit 1;"
                          logger.debug(querystr)
                          db.query(querystr) 
                          r = db.store_result()
                          row = r.fetch_row(10000)
                          if len(row) > 0:
                             for line in row:
                                timestr = line[0]
                                test_result = line[1].strip()
                      except Exception,e:
                          logger.error("ERROR READING SUBMISSION TEST RESULT FROM WMSMonitor DB: " + str(e))
                          logger.error("query: " + querystr)

                      if test_result == "Null":
                          subtest_err_flag = 1
                          mail_notification("Subject: WARNING LOAD BALANCING SUBMISSION TEST:" + test_url[ij] + "\n" , "WARNING: NO TEST RESULTS FOUND FOR CONSIDERED WMS!\n FILE : " + test_url[ij] + "\n""For wmsserver: " + wms + "\n")                        
 
                      #checking date
                      deltatime = int(time.time())-int(time.mktime(time.strptime(timestr,"%Y-%m-%d %H:%M:%S")))
                      if (deltatime < 3600) :
                             logger.info("CURRENT STATUS SUBTEST: " + test_result )
                             if test_result !="0" :
                                logger.warning("SUBTEST fails for wms: " + wms)
                                subtest = -1
                      else:
                            subtest_err_flag = 1
                            mail_notification("Subject: WARNING LOAD BALANCING SUBMISSION TEST:" + test_url[ij]+ "\n" , "WARNING: SUBMISSION TEST TOO OLD!\n FILE : " +  test_url[ij] + "\n""For wmsserver: " + wms + "\n")
                            
                          
                 #GETTING WMS STATUS METRIC FROM WMSMON SERVER DB                 
                 querystr="select measure_time,loadb_fmetric from wms_sensor where idhost='" + idwms + "' and measure_time > '" +  time.strftime("%Y-%m-%d %H:%M:%S",time.localtime(time.time()-4000)) + "' order by measure_time desc limit 1;"
                 logger.info("Launching query to find the need step.  Query is:")
                 logger.info(querystr)
                 db.query(querystr)
                 r = db.store_result()
                 row = r.fetch_row(10000)
                 if len(row) > 0:
                    if row[0][0] != None : 
                       #checking whether time_stamp has been recently updated
                       timestr = row[0][0]
                       deltatime = int(time.time())-int(time.mktime(time.strptime(timestr,"%Y-%m-%d %H:%M:%S")))

                       try:
                             metric = float(row[0][1])
                       except:
                             try: 
                                 metric = float(row[1][1])
                                 timestr = row[1][0]
                                 deltatime = int(time.time())-int(time.mktime(time.strptime(timestr,"%Y-%m-%d %H:%M:%S")))
                             except:
                                 metric = -100
                                 mail_notification("Subject: ERROR LOAD BALANCING UNABLE TO DETERMINE METRIC\n" , "WARNING: UNABLE TO READ METRIC VALUE!\n TIMESTAMP : " +  timestr + "\n For wmsserver: " + wms + "\n")

                       #considering submission test in the metric just if it enabled and returning a valid result
                       if (subtest_enable[ik] == '1') and (subtest_err_flag == 0):
                          if metric > 0:
                             metric = metric * subtest
                        
                       #creating wms metric list for considered alias
                       logger.info("FINAL METRIC: " + str(wms) + "\t" + str(metric))
                       if (metric) > 0: 
                          posmetriclist.append([metric,str(wms)])
                          #wmsmetriclist.append(metric)
                       else:
                          negmetriclist.append([metric,str(wms)])
                          #wmsmetriclist.append(metric)
                    else:
                       negmetriclist.append([-100,str(wms)])
                       #wmsmetriclist.append(-100)

######################################################################################################### 
            #CALCULATING NEW WMS SET BEHIND THE ALIAS
            posmetriclist.sort()
            negmetriclist.sort()
            logger.debug("POSMETRIC: " + str(posmetriclist))
            logger.debug("NEGMETRIC: " + str(negmetriclist))
            logger.debug("WMSSMETRIC: " + str(wmsmetriclist))

            #Here we decide which wms to put in the alias
            if len(posmetriclist) < (len(wmslist) - float(numout[ik])):
                 #Here we have less WMS available than needed  
                 if len(posmetriclist) == 0:
                    #NO WMS WITH POSITIVE METRIC. WE CHOOSE THE WMS WITH HIGHER METRIC
                    logger.warning("No positive metric wms instances available")
                    #aliasnewlist.append(socket.gethostbyname(wmslist[wmsmetriclist.index(negmetriclist[len(negmetriclist)-1])].strip()))
                    aliasnewlist.append(socket.gethostbyname(negmetriclist[len(negmetriclist)-1][1].strip()))
                    logger.warning("alias new list is" + str(aliasnewlist))
                    # N.B. if all wms in the alias have NULL metric, the last in the
                    # list will be put in the alias anyway
                 else:
                    #we put in the alias all positive metric wms we have
                    for i in range(0,len(posmetriclist)):
                        #aliasnewlist.append(socket.gethostbyname(wmslist[wmsmetriclist.index(posmetriclist[i])].strip()))
                        aliasnewlist.append(socket.gethostbyname(posmetriclist[i][1].strip()))
                    logger.warning("Less pos wms than needed")
                    logger.warning("alias new list is" + str(aliasnewlist))


            else:
                 logger.debug("GOOD: More pos wms instances than needed")
                 for i in range(0,len(wmslist) - int(numout[ik])):
                    #aliasnewlist.append(socket.gethostbyname(wmslist[wmsmetriclist.index(posmetriclist[i])].strip()))
                    aliasnewlist.append(socket.gethostbyname(posmetriclist[i][1].strip()))
                 logger.debug("alias new list is" + str(aliasnewlist))

            #UPDATING DNS
            updateflag = 0
            f = open('filealiastmp.txt','w')
            f.write('server ' + conf.get('DNS_SERVER') + '\n')
            f.write('zone ' + conf.get('DNS_ZONE') + '\n')

            for ip in aliasnewlist:
                 print 'wms to add: ', socket.gethostbyaddr(ip)[0] 
                 if host.count(ip)==0:
                    f.write('update add ' + alias + '.' + conf.get('DNS_ZONE') + ' 60 A ' + ip + '\n')
                    updateflag = 1
            for ip in host:
                 print 'ip already in host: ', socket.gethostbyaddr(ip)[0] 
                 if aliasnewlist.count(ip)==0:
                    f.write('update delete ' + alias + '.' + conf.get('DNS_ZONE') + ' 60 A ' + ip + '\n')
                    updateflag = 1
            if updateflag:
                 f.write('show\n')
                 f.write('send\n')
            f.close()

            if updateflag:
                 if (os.system('nsupdate -y ' + conf.get('DNS_KEYSTRING') + ' filealiastmp.txt')):
                     logger.error('DNS UPDATE COMMAND: ' + 'nsupdate -y ' + conf.get('DNS_KEYSTRING') + ' filealiastmp.txt')
                     logger.error("DNS UPDATE COMMAND EXITED WITH ERROR")
#                print 'Updateflag is= ', updateflag, '\n'
#                s = input('press a key')
            os.system('rm -f filealiastmp.txt')


wms_balancing_arbiter()


