#!/usr/bin/python

# Python import
import os, commands, sys, fpformat
import MySQLdb,time,datetime
import logging
sys.path.append('../common')
import readconf_func
import istance_class
import wms_class
import logpredef_analyzer
import analyzer_utils
import vo_group_class


logger = logging.getLogger('db-analyzer')

logger.info('Reading wmsmon conf file')
confvar=readconf_func.readconf();

dbhost = confvar.get('WMSMON_DB_HOST')
dbuser = confvar.get('LB_DB_USER')
dbname = confvar.get('LB_DB_NAME')

logger.info("Starting db connection")
db = MySQLdb.connection(host=confvar.get('WMSMON_DB_HOST'),user=confvar.get('WMSMON_DB_USER'),passwd=confvar.get('WMSMON_DB_PWD'),db=confvar.get('WMSMON_DB_NAME'))

previous_date = 0
last_update = 0
WMS_OBJ_LIST = []
LB_OBJ_LIST = []
wms_known_host = []
lb_known_host = []
VO_GROUP_LIST = []

SLEEP_TIME = 10
SAFE_TIMEOUT = 360

while True:  # starting main loop

   #check existence of new data
   last_date = analyzer_utils.check_last_date(db)
   logger.info('Since last check = ' + str((time.time() - last_update)) + ' SAFE_TIMEOUT = ' + str(SAFE_TIMEOUT) )
   if last_date > previous_date and (time.time() - last_update) > SAFE_TIMEOUT:
      last_update = time.time()
      #if yes check if new wms are present
      logger.info("New DB data. Updating memory content.")
      wmslist = analyzer_utils.select_distinct_wms(db)
      lblist = analyzer_utils.select_distinct_lb(db)
      logger.info("WMS first.")
      for wms in wmslist:
         if wms_known_host.count(wms) == 0:
            wms_known_host.append(wms)
            #ohoh we have a new wms
            logger.info("New WMS found in the db. Collecting its data. wms is " + wms)
            newWMS = wms_class.WMS(wms,[],[],[])
            analyzer_utils.fill_WMS_data(newWMS,db)
            WMS_OBJ_LIST.append(newWMS)

         else: 
            #wms already known, updating...
            logger.info("WMS already in memory. Collecting its data. wms is " + wms)
            for WMSobj in  WMS_OBJ_LIST:
               if WMSobj.host == wms:
                  analyzer_utils.fill_WMS_data(WMSobj,db)

      # all wms are filled
      logger.info("All wms are filled")

      logger.info("Now the LB.")
      for lb in lblist:
         if lb_known_host.count(lb) == 0:
            lb_known_host.append(lb)
            #ohoh we have a new lb
            logger.info("New LB found in the db. Collecting its data. lb is " + lb)
            newLB = istance_class.Istance(lb,[],[])
            analyzer_utils.fill_LB_data(newLB,db)
            LB_OBJ_LIST.append(newLB)
         else:
            #lb already known, updating...
            logger.info("LB already in the db. Collecting its data. lb is " + lb)
            for LBobj in  LB_OBJ_LIST:
               if LBobj.host == lb:
                  analyzer_utils.fill_LB_data(LBobj,db)

      # all lb are filled
      logger.info("All LB are filled")

      logger.info("Associating LB to WMS.")
      for WMSobj in WMS_OBJ_LIST:
         for LBobj in LB_OBJ_LIST:
            if WMSobj.LB == LBobj.host:
               WMSobj.LBobj = LBobj

      for WMSobj in WMS_OBJ_LIST:
         print WMSobj.print_wms()
         WMSobj.make_wms_status()
         analyzer_utils.send_istance_status(WMSobj,'WMS')
         print LB_OBJ_LIST
      for LBobj in LB_OBJ_LIST:
         LBobj.make_ist_status()
         analyzer_utils.send_istance_status(LBobj,'LB')
         print LBobj.print_istance()

      # now create the vo/wms association using the vo_group class and the group file
      logger.info("Now create the vo/wms association.")
      vo_list = analyzer_utils.get_vo_list(db)
      if len(vo_list) < 1:
         logger.error("No VO found this is not possible. Doing nothing, waiting for next iteration")
         continue
 
      groupfile = '/root/groupfile'
      try:
         logger.info('Opening new file for searching groups.')
         fgr = open(groupfile,'r')
      except IOError:
         logger.error('Cannot open file for reading. Filename is : ' + groupfile)
         db.close()
         sys.exit(1)
      lines = fgr.readlines()
      fgr.close()

      vo_group_list = []

      logger.info("Looking for vo and groups in groupfile and db")
      for vo in vo_list:
         if vo:
            if analyzer_utils.vo_has_group(vo,lines):
               group_list = analyzer_utils.get_group_list(vo,lines)
               for group in group_list:
                  vo_group_list.append(group)
            else:
               vo_group_list.append(vo)
      logger.info("VO/GROUP list is " + str(vo_group_list))
    
      logger.info("Populating the GROUPS with WMS and LB")
      for vogr in vo_group_list:
         GROUP_present = False
         for VOGRobj in VO_GROUP_LIST:
            if VOGRobj.name == vogr:
               GROUP_present = True
         if GROUP_present == False:
            newVOGR = vo_group_class.vo_group(vogr)
            VO_GROUP_LIST.append(newVOGR)

      for VOGRobj in VO_GROUP_LIST:
         VOGRobj.wms_list = analyzer_utils.get_wms_per_group(VOGRobj.vo,VOGRobj.group,groupfile,db)

         lb_list = []
         lb_list_distinct = []

         for wms in VOGRobj.wms_list:
            lb = analyzer_utils.get_lb_per_wms(wms,db)
            lb_list.append(lb)
         VOGRobj.lb_list  = lb_list
        
         VOGRobj.wms_obj_list = []
         for wms in VOGRobj.wms_list:
            for WMSobj in WMS_OBJ_LIST:
               if WMSobj.host == wms:
                  VOGRobj.wms_obj_list.append(WMSobj)
     
         for lb in VOGRobj.lb_list:
            if lb_list_distinct.count(lb) == 0:
               lb_list_distinct.append(lb)

         VOGRobj.lb_obj_list = []
         for lb in lb_list_distinct:
            for LBobj in LB_OBJ_LIST:
               if LBobj.host == lb:
                  VOGRobj.lb_obj_list.append(LBobj)

      # now for any vo_group look for allarms
      # for any vo_group send allarms if any to nagios
      logger.info("Looking for allarms in any GROUP and sending the GROUP STATUS to NAGIOS")
      for VOGRobj in VO_GROUP_LIST:
         VOGRobj.make_status()
         VOGRobj.print_vo_group()
         analyzer_utils.send_group_status(VOGRobj)

      previous_date = last_date
         
   else:
      logger.info("DB data not change since last iteration.")
      logger.info("Or DB changed but the SAFE_TIMEOUT was not passed. Doing nothing for a while.")
      logger.info("Summary of memory content:")
      logger.info("Number of WMSobj = " + str(len(WMS_OBJ_LIST)))
      logger.info("Number of LBobj = " + str(len(LB_OBJ_LIST)))
      logger.info("Number of VO/GROUPS = " + str(len(VO_GROUP_LIST)))
      n_wms_avg = 0
      n_lb_avg = 0
      for VOGRobj in VO_GROUP_LIST:
         n_wms_avg = n_wms_avg + len(VOGRobj.wms_obj_list)
         n_lb_avg = n_lb_avg + len(VOGRobj.lb_obj_list)
      if len(VO_GROUP_LIST) > 0:
         n_wms_avg = float(n_wms_avg) / len(VO_GROUP_LIST)
         n_lb_avg = float(n_lb_avg) / len(VO_GROUP_LIST)
      logger.info("AVG number of WMS per VO/GROUPS = " + str(n_wms_avg))
      logger.info("AVG number of LB per VO/GROUPS = " + str(n_lb_avg))

   # sleep for a while and restart
   time.sleep(SLEEP_TIME)

db.close()
