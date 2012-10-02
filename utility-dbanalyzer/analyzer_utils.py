#!/usr/bin/python

# Python import
import os, commands, sys, fpformat
import MySQLdb,time,datetime
import logging
sys.path.append('../common')
import readconf_func
import wms_class
import logpredef_analyzer


logger = logging.getLogger('analyzer-utils')


def get_value(val):
   if val:
      return val
   else:
      return 0

def check_last_date(db):
   myquery = "select date from lbsensor order by date desc limit 1;"
   logger.info("Launching query to find the last date.  Query is: " + myquery)
   db.query(myquery)
   r = db.store_result()
   row = r.fetch_row()
   if len(row) > 0:
      LASTDATE = row[0][0]
      logger.info("LASTDATE = " + LASTDATE)
   else:
      logger.waring("No date found into db. Returning None")
      return None
   datetmp = time.strptime(LASTDATE,"%Y-%m-%d %H:%M:%S")
   lastd = int(time.mktime(datetmp))
   return lastd


def select_distinct_wms(db):
   wmslist = []
   #TODAY = time.strftime("%Y-%m-%d",time.localtime())
   ENDDATE = time.strftime("%Y-%m-%d %H:%M:%S",time.localtime())
   STARTDATE = time.strftime("%Y-%m-%d %H:%M:%S",time.localtime((time.time() - 3600*24)))
   myquery = "select distinct(wms) from lbsensor_daily where date > '" + STARTDATE + "' and date < '" + ENDDATE + "';"
   logger.info("Launching query to find the wms list.  Query is: " + myquery)
   db.query(myquery)
   r = db.store_result()
   row = r.fetch_row(10000)
   if len(row) > 0:
      logger.info("WMS found into db")
      for line  in row:
         wms = line[0]
         wmslist.append(wms)
   else:
      logger.warning("No wms found into db. Returning None")
   return wmslist

def select_distinct_lb(db):
   lblist = []
   #TODAY = time.strftime("%Y-%m-%d",time.localtime())
   ENDDATE = time.strftime("%Y-%m-%d %H:%M:%S",time.localtime())
   STARTDATE = time.strftime("%Y-%m-%d %H:%M:%S",time.localtime((time.time() - 3600*24)))
   myquery = "select distinct(lbserver) from lbsensor_daily where date > '" + STARTDATE + "' and date < '" + ENDDATE + "';"
   logger.info("Launching query to find the lb list.  Query is: " + myquery)
   db.query(myquery)
   r = db.store_result()
   row = r.fetch_row(10000)
   if len(row) > 0:
      logger.info("LB found into db")
      for line  in row:
         lb = line[0]
         lblist.append(lb)
   else:
      logger.warning("No lb found into db. Returning Empty List")

   return lblist


def fill_WMS_data(newWMS,db):
   wmshost = newWMS.host
   myquery = "select date, `load`, sandbox, tmp, varlog, varlibmysql, WMP, WM, LM, JC, LL, PX, LBPX, FTPD, input_fl, queue_fl, dg20 from wmssensor where wms = '" + wmshost + "' order by date desc limit 1;"
   logger.info("Launching query to find wms data from wmsensor. Query is:" + myquery)
   db.query(myquery)
   r = db.store_result()
   row = r.fetch_row(10000)
   if len(row) > 0:
      logger.info("Data found into wmssensor table for wms = " + wmshost)
      for line  in row:
         newWMS.last_update = line[0]
         newWMS.cpu = line[1]
         newWMS.fs_dict['sandbox'] = line[2]
         newWMS.fs_dict['tmp'] = line[3]
         newWMS.fs_dict['varlog'] = line[4]
         newWMS.fs_dict['varlibmysql'] = line[5]
         newWMS.daemons_dict['WMP'] = line[6]
         newWMS.daemons_dict['WM'] = line[7]
         newWMS.daemons_dict['LM'] = line[8]
         newWMS.daemons_dict['JC'] = line[9]
         newWMS.daemons_dict['LL'] = line[10]
         newWMS.daemons_dict['PX'] = line[11]
         newWMS.daemons_dict['LBPX'] = line[12]
         newWMS.daemons_dict['FTPD'] = line[13]
         newWMS.queue_dict['input_fl'] = line[14]
         newWMS.queue_dict['queue_fl'] = line[15]
         newWMS.queue_dict['dg20'] = line[16]
   else:
      logger.warning("No data found for wms = " + wmshost)
      return 1

   myquery = "select fdrain, fload, ftraversaltime from wmsloadbalance where wms = '" + wmshost + "' order by date desc limit 1;"
   logger.info("Launching query to find the wms data from loadbalance.  Query is: " + myquery)
   db.query(myquery)
   r = db.store_result()
   row = r.fetch_row(10000)
   if len(row) > 0:
      logger.info("Data found into loadbalance table for wms = " + wmshost)
      for line  in row:
         newWMS.fdrain = line[0]
         newWMS.fload = line[1]
         newWMS.ftraversaltime = line[2]
      if newWMS.fload != 'NULL' and newWMS.fdrain != 'NULL' and newWMS.ftraversaltime != 'NULL':
         newWMS.metric = int(get_value(newWMS.fdrain)) * (float(get_value(newWMS.fload)) + float(get_value(newWMS.ftraversaltime)))
      else:
         newWMS.metric = None
   else:
      logger.warning("No data found for wms = " + wmshost)
      return 1

# now searching the VO

   myquery = "select VO from lbsensor_daily where wms = '" + wmshost + "' order by date desc limit 1;"
   logger.info("Launching query to find the VO.  Query is: " + myquery)
   db.query(myquery)
   r = db.store_result()
   row = r.fetch_row(10000)
   if len(row) > 0:
      logger.info("Data found into lbsensor_daily table for wms = " + wmshost)
      for line  in row:
         newWMS.VO = line[0]
   else:
      logger.warning("No VO found for wms = " + wmshost)
      return 1

# now searching the associated LB

   myquery = "select lbserver from lbsensor where wms = '" + wmshost + "' order by date desc limit 1;"
   logger.info("Launching query to find the LB.  Query is: " + myquery)
   db.query(myquery)
   r = db.store_result()
   row = r.fetch_row(10000)
   if len(row) > 0:
      logger.info("Data found into lbsensor table for wms = " + wmshost)
      for line  in row:
         newWMS.LB = line[0]
   else:
      logger.warning("No LB found for wms = " + wmshost)
      return 1


   return 0

def fill_LB_data(newLB,db):
   lbhost = newLB.host
   myquery = "select date, `load`, lb_disk, lib_mysql_disk, LB_CON, LB_LB from lbsensor where lbserver = '" + lbhost + "' order by date desc limit 1;"
   logger.info("Launching query to find wms data from lbsensor. Query is:" + myquery)
   db.query(myquery)
   r = db.store_result()
   row = r.fetch_row(10000)
   if len(row) > 0:
      logger.info("Data found into lbsensor table for lb = " + lbhost)
      for line  in row:
         newLB.last_update = line[0]
         newLB.cpu = line[1]
         newLB.fs_dict['lb_disk'] = line[2]
         newLB.fs_dict['lib_mysql_disk'] = line[3]
         newLB.daemons_dict['LB'] = line[5]
   else:
      logger.warning("No data found for lb = " + lbhost)
      return 1
   return 0


def get_vo_list(db):

   vo_list = []
   #TODAY = time.strftime("%Y-%m-%d",time.localtime()) 
   ENDDATE = time.strftime("%Y-%m-%d %H:%M:%S",time.localtime())
   STARTDATE = time.strftime("%Y-%m-%d %H:%M:%S",time.localtime((time.time() - 3600*24)))
   myquery = "select distinct(vo) from lbsensor_daily where date > '" + STARTDATE + "' and date < '" + ENDDATE + "';"
   logger.info("Launching query to find distinct VO.  Query is: " + myquery)
   db.query(myquery)
   r = db.store_result()
   row = r.fetch_row(10000)
   if len(row) > 0:
      logger.info("VOs found.")
      for line  in row:
         vo_list.append(line[0])
   else:
      logger.warning("No VO found. Returning Empty list.")
      return []

   return vo_list

def vo_has_group(vo,lines):
  
   for line in lines:
      linesp = line.split()
      if linesp[1] == vo:
         return True
   return False
 
def get_group_list(vo,lines):
   group_list = []

   for line in lines:
      linesp = line.split()
      if linesp[1] == vo:
         group = linesp[2]
         vogroup = vo + '-' + group
         if group_list.count(vogroup) == 0:
            group_list.append(vo + '-' + group)

   return group_list


def get_wms_per_group(vo,group,groupfile,db):

   wms_list = []

   if group:
      #use the file
      cmd = 'grep ' + vo +  ' ' + groupfile + ' | grep ' + group
      stream = os.popen(cmd)
      lines = stream.readlines()
      for line in lines:
         if len(line.split()) > 0:
            wms = line.split()[0]
            wms_list.append(wms)
   else:
      #use the db
      #TODAY = time.strftime("%Y-%m-%d",time.localtime())
      ENDDATE = time.strftime("%Y-%m-%d %H:%M:%S",time.localtime())
      STARTDATE = time.strftime("%Y-%m-%d %H:%M:%S",time.localtime((time.time() - 3600*24)))
      myquery = "select distinct(wms) from lbsensor_daily where vo = '" + vo + "' and date > '" + STARTDATE + "' and date < '" + ENDDATE + "';"
      logger.info("Launching query to find distinct WMS.  Query is: " + myquery)
      db.query(myquery)
      r = db.store_result()
      row = r.fetch_row(10000)
      if len(row) > 0:
         logger.info("WMS found.")
         for line  in row:
            wms_list.append(line[0])

   return wms_list

def get_lb_per_wms(wms,db):
   lb = None
   myquery = "select lbserver from lbsensor_daily where wms = '" + wms + "' order by date desc limit 1;"
   logger.info("Launching query to find LB associated to wms = " + wms + ".  Query is: " + myquery)
   db.query(myquery)
   r = db.store_result()
   row = r.fetch_row(10000)
   if len(row) > 0:
      logger.info("LB found.")
      for line  in row:
         lb = line[0]
   return lb

def send_group_status(VOGRobj):
   if VOGRobj.STATUS == 0:
      status_to_send = 0 
      nagios_service = VOGRobj.name + '-WMS'
      message_str = VOGRobj.name + '-WMS' + " STATUS is OK"
   elif VOGRobj.STATUS == 1:
      status_to_send = 1
      nagios_service = VOGRobj.name + '-WMS'
      message_str = VOGRobj.name + '-WMS' + " STATUS is WARNING - " + VOGRobj.message
   elif VOGRobj.STATUS == 2:
      status_to_send = 2
      nagios_service = VOGRobj.name + '-WMS'
      message_str = VOGRobj.name + '-WMS' + " STATUS is CRITICAL - " + VOGRobj.message
   elif VOGRobj.STATUS == None:
      status_to_send = 3
      nagios_service = VOGRobj.name + '-WMS'
      message_str = VOGRobj.name + '-WMS' + " STATUS is UNKNOWN"

   cmd = '''echo "cert-wms-01;''' + nagios_service.upper() + ''';''' + str(status_to_send) + ''';''' + message_str + '''" | send_nsca -H gstore.cnaf.infn.it -d ';' -c /etc/nagios/send_nsca.cfg'''
   logger.info("Launching command cmd = " + cmd)
   status = os.system(cmd)
   if status == 0:
      logger.info("Command sent successfully")
   else:
      logger.warning("Command failed. Exit code = " + str(status))
   return status

def send_istance_status(ISTobj,serv):
   nagios_service = 'MON-' + serv
   if ISTobj.STATUS == 0:
      status_to_send = 0
      message_str = ISTobj.host + " STATUS is OK - " + ISTobj.message
   elif ISTobj.STATUS == 1:
      status_to_send = 1
      message_str = ISTobj.host + " STATUS is WARNING - " + ISTobj.message
   elif ISTobj.STATUS == 2:
      status_to_send = 2
      message_str = ISTobj.host + " STATUS is CRITICAL - " + ISTobj.message
   elif ISTobj.STATUS == None:
      status_to_send = 3
      message_str = ISTobj.host + " STATUS is UNKNOWN - " + ISTobj.message

   cmd = '''echo "''' + ISTobj.host.split('.')[0] + ''';''' + nagios_service.upper() + ''';''' + str(status_to_send) + ''';''' + message_str + '''" | send_nsca -H gstore.cnaf.infn.it -d ';' -c /etc/nagios/send_nsca.cfg'''
   logger.info("Launching command cmd = " + cmd)
   status = os.system(cmd)
   if status == 0:
      logger.info("Command sent successfully")
   else:
      logger.warning("Command failed. Exit code = " + str(status))
   return status
