#!/usr/bin/python

import os, sys
import os, commands, sys, fpformat
import MySQLdb,time,datetime
import lb_sensor_func
import readconf_func

def lb_query(dbhost,dbuser,dbname,lbhost,wmshost,STARTDATE,ENDDATE):
   ''' lb_query(dbhost,dbuser,dbname,lbhost,wmshost,STARTDATE,ENDDATE) -> runs query on lb server for a specified wms server
       Returns a list of string'''

   #Initializing logger
   import logging
   logger = logging.getLogger('lb_query')

   confvar=readconf_func.readconf();

   users_stats=[]   
   # Establish a connection
   logger.info('Establishing a connection with mysql DB')
   db = MySQLdb.connection(host=dbhost,user=dbuser,db=dbname)
   # Run a MySQL query to find the number of single jobs submitted in a given time interval
   logger.info('Running a MySQL query to find the number of single jobs submitted in a given time interval')
#   querystr="select COUNT(DISTINCT(events.jobid)) from events,short_fields where events.event=short_fields.event and code='17' and time_stamp >'" + STARTDATE + "' and time_stamp <='" + ENDDATE + "' and host='" + wmshost + "' and events.jobid=short_fields.jobid and name='NSUBJOBS'  and value='0';"
   querystr="select  users.cert_subj,COUNT(DISTINCT(events.jobid)) from events,short_fields inner join users on events.userid=users.userid where events.event=short_fields.event and code='17' and time_stamp >'" + STARTDATE + "' and time_stamp <='" + ENDDATE + "' and host='" + wmshost + "' and events.jobid=short_fields.jobid and name='NSUBJOBS'  and value='0' group by users.cert_subj;"


   logger.info('Query is : ' + querystr)   
   db.query(querystr)
   r = db.store_result()
   # Iterate through the result set
   # Example calls back up to 100 rows
   WMP_in = 0
   if r:
      for row in r.fetch_row():
          users_stats.append([row[0],row[1],0,0,0,0,0,0,0)
          WMP_in = WMP_in + int(row[1])
   

   # Run a MySQL query to find the number of collection jobs submitted in a given time interval, thei mean number of subnodes and the STD 
   logger.info(' Running a MySQL query to find the number of collection jobs submitted in a given time interval, thei mean number of subnodes and the STD')
   querystr="select COUNT(value),AVG(value),STD(value) from events,short_fields where events.event='0' and code='17' and time_stamp >'" + STARTDATE + "' and time_stamp <='" + ENDDATE + "' and host='" + wmshost + "' and events.jobid=short_fields.jobid and name='NSUBJOBS' and short_fields.event='0' and value>'0';"

   logger.info('Query is : ' + querystr)   
   db.query(querystr)
   r = db.store_result()
   # Iterate through the result set
   # Example calls back up to 100 rows
   if r:
      for row in r.fetch_row():
          WMP_in_col = row[0]
          WMP_in_col_avg = row[1]
          WMP_in_col_std = row[2]

   # Run a MySQL query to find the number of collection jobs submitted in a given time interval, thei mean number of subnodes and the STD
   logger.info(' Running a MySQL query to find the number of collection jobs submitted in a given time interval, thei mean number of subnodes and the STD')
   querystr="select  users.cert_subj,COUNT(value),AVG(value),STD(value) from events,short_fields inner join users on events.userid=users.userid where events.event=short_fields.event and code='17' and time_stamp >'" + STARTDATE + "' and time_stamp <='" + ENDDATE + "' and host='" + wmshost + "' and events.jobid=short_fields.jobid and name='NSUBJOBS'  and short_fields.event='0' and value>'0' group by users.cert_subj;"

   logger.info('Query is : ' + querystr)
   db.query(querystr)
   r = db.store_result()
   # Iterate through the result set
   # Example calls back up to 100 rows
   
   if r:
      for row in r.fetch_row():
          flaguserfound=0
          for i in range(0,len(users_stats)):
              if users_stats[i][0]==row[0]:
                 users_stats[i][2]=row[1]
                 users_stats[i][3]=row[2]
                 users_stats[i][4]=row[3]
                 flaguserfound = 1
          if flaguserfound == 0:
             users_stats.append(row[0],0,row[1],row[2],row[3],0,0,0,0)
                 
   # Run a MySQL query to find the number of jobs enqueued to WM from WMPROXY in a given time interval
   logger.info('Run a MySQL query to find the number both collection and single jobs submitted in a given time interval')
   querystr="select COUNT(events.jobid) from events,short_fields where  code='4' and time_stamp >'" + STARTDATE + "' and time_stamp <='" + ENDDATE + "' and host='" + wmshost + "' and events.jobid=short_fields.jobid and events.event=short_fields.event and  prog='NetworkServer' and name='RESULT' and value='OK';"
   logger.info('Query is : ' + querystr)   
   db.query(querystr)
   r = db.store_result()
   # Iterate through the result set
   # Example calls back up to 100 rows
   if r:
     for row in r.fetch_row():
         WM_in = row[0]

   # Run a MySQL query to find the number both collection and single jobs enqueued to WM in a given time interval from LogMonitor (i.e. Resubmitted)
   logger.info('Run a MySQL query to find the number both collection and single jobs enqueued to WM in a given time interval from LogMonitor (i.e. Resubmitted)')
   querystr="select users.cert_subj,COUNT(DISTINCT(events.jobid)) from events,short_fields inner join users on events.userid=users.userid from events,short_fields where code='4' and time_stamp >'" + STARTDATE + "' and time_stamp <='" + ENDDATE + "' and host='" + wmshost + "' and events.jobid=short_fields.jobid and events.event=short_fields.event and name='RESULT' and value='OK' and prog='LogMonitor' group by users.cert_subj;"
   logger.info('Query is : ' + querystr)   

   db.query(querystr)
   r = db.store_result()
   # Iterate through the result set
   # Example calls back up to 100 rows

   WM_in_res = 0 
   if r:
      for row in r.fetch_row():
          flaguserfound=0
          for i in range(0,len(users_stats)):
              if users_stats[i][0]==row[0]:
                 users_stats[i][5]=row[1]
                 WMP_in_res = WMP_in_res + int(row[1])
                 flaguserfound = 1
          if flaguserfound == 0:
              users_stats.append(row[0],0,0,0,0,row[1],0,0,0)
              WMP_in_res = WMP_in_res + int(row[1])

   # Run a MySQL query to find the number single jobs enqueued to Job Controller from WM in a given time interval
   logger.info('# Run a MySQL query to find the number single jobs enqueued to Job Controller from WM in a given time interval')
   querystr="select users.cert_subj,COUNT(DISTINCT(events.jobid)) from events,short_fields inner join users on events.userid=users.userid from events,short_fields where code='4' and time_stamp >'" + STARTDATE + "' and time_stamp <='" + ENDDATE + "' and host='" + wmshost + "' and events.jobid=short_fields.jobid and events.event=short_fields.event and name='RESULT' and value='OK' and prog='WorkloadManager' group by users.cert_subj;"
   logger.info('Query is : ' + querystr)   

   db.query(querystr)
   r = db.store_result()
   # Iterate through the result set
   # Example calls back up to 100 rows
   if r:
      for row in r.fetch_row():
          JC_in = row[0]

   # Run a MySQL query to find the number single jobs enqueued to Condor from Job Controller in a given time interval
   logger.info('Run a MySQL query to find the number single jobs enqueued to Condor from Job Controller in a given time interval')
   querystr="select users.cert_subj,COUNT(DISTINCT(events.jobid)) from events,short_fields inner join users on events.userid=users.userid from events,short_fields where code='1' and time_stamp >'" + STARTDATE + "' and time_stamp <='" + ENDDATE + "' and host='" + wmshost + "' and events.jobid=short_fields.jobid and events.event=short_fields.event and name='RESULT' and value='OK' and prog='JobController' group by users.cert_subj;"

   logger.info('Query is : ' + querystr)   
   db.query(querystr)
   r = db.store_result()
   # Iterate through the result set
   # Example calls back up to 100 rows

   JC_out = 0
   if r:
      for row in r.fetch_row():
          flaguserfound=0
          for i in range(0,len(users_stats)):
              if users_stats[i][0]==row[0]:
                 users_stats[i][6]=row[1]
                 JC_out = JC_out + int(row[1])
                 flaguserfound = 1
          if flaguserfound == 0:
              users_stats.append(row[0],0,0,0,0,0,row[1],0,0)
              JC_out = JC_out + int(row[1])

   #NB mettere un try except per possibili fallimenti query

  # Run a MySQL query to find the number of jobs done in a given time interval
   logger.info('Run a MySQL query to find the number single jobs done successfully since 00:00 of same day')
   querystr="select users.cert_subj,COUNT(DISTINCT(events.jobid)) from events,short_fields inner join users on events.userid=users.userid where events.jobid=short_fields.jobid and code='10' and time_stamp >'" + STARTDATE + "' and time_stamp <='" + ENDDATE + "' and host='" + wmshost + "'and prog='LogMonitor' and name='REASON' and value='Job terminated successfully' group by users.cert_subj;"


   #print querystr
   logger.info('Query is : ' + querystr)
   db.query(querystr)
   r = db.store_result()
   # Iterate through the result set
   # Example calls back up to 100 rows

   JOB_DONE = 0
   if r:
      for row in r.fetch_row():
          flaguserfound=0
          for i in range(0,len(users_stats)):
              if users_stats[i][0]==row[0]:
                 users_stats[i][7]=row[1]
                 JOB_DONE = JOB_DONE + int(row[1])
                 flaguserfound = 1
          if flaguserfound == 0:
              users_stats.append(row[0],0,0,0,0,0,0,row[1],0)
              JOB_DONE = JOB_DONE + int(row[1])

  # Run a MySQL query to find the number of jobs aborted in a given time interval
   logger.info('Run a MySQL query to find the number single jobs aborted since 00:00 of same day')
   querystr="select users.cert_subj,COUNT(DISTINCT(events.jobid)) from events,short_fields inner join users on events.userid=users.userid events where code='12' and time_stamp >'" + STARTDATE + "' and time_stamp <='" + ENDDATE + "' and host='" + wmshost + "' group by users.cert_subj;"

   logger.info('Query is : ' + querystr)
   db.query(querystr)
   r = db.store_result()
   # Iterate through the result set
   # Example calls back up to 100 rows
   JOB_ABORTED = 0
   if r:
      for row in r.fetch_row():
          flaguserfound=0
          for i in range(0,len(users_stats)):
              if users_stats[i][0]==row[0]:
                 users_stats[i][8]=row[1]
                 JOB_ABORTED = JOB_ABORTED + int(row[1])
                 flaguserfound = 1
          if flaguserfound == 0:
              users_stats.append(row[0],0,0,0,0,0,0,0,row[1])
              JOB_ABORTED = JOB_ABORTED + int(row[1])

   db.close()
  
   #COLLECTING DATA ABOUT LB MACHINE STATUS
   output_tmp=lb_sensor_func.lb_sensor(confvar)
   if output_tmp[0] != None:
      load = output_tmp[0]
   else:
      load = 'Null'
   if output_tmp[1] != None:
      lb_disk = output_tmp[1]
   else:
      lb_disk = 'Null'
   if output_tmp[2]!=None:
      LB_CON = output_tmp[2]
   else:
      LB_CON = 'Null'
   if output_tmp[3]!=None:
      LB = output_tmp[3]
   else:
      LB = 'Null'
   if output_tmp[4]!=None:
      LL = output_tmp[4]
   else:
      LL = 'Null'
   if output_tmp[5]!=None:
      lib_mysql_disk = output_tmp[5]
   else:
      lib_mysql_disk = 'Null'

   #Logging fields
   outputstr="WMP_in="+ str(WMP_in) + "WMP_in_col=" + str(WMP_in_col) + "WMP_in_col_avg=" + str(WMP_in_col_avg) + "WMP_in_col_std=" + str(WMP_in_col_std) + "WM_in=" + str(WM_in) +  "WM_in_res=" + str(WM_in_res) + "JC_in=" + str(JC_in) +"JC_out=" + str(JC_out) + ", load=" + str(load) + ", lb_disk=" + str(lb_disk) + ",LB_CON=" + str(LB_CON) +", LB=" +  str(LB) + ", LL=" + str(LL) + ", Done=" + str(JOB_DONE) + ", Aborted=" + str(JOB_ABORTED) + ", lib_mysql_disk=" + str(lib_mysql_disk)
   logger.debug("LB values collected are:")
   logger.debug(outputstr)

   

   output=[]
   output.append(WMP_in)
   output.append(WMP_in_col)
   output.append(WMP_in_col_avg)
   output.append(WMP_in_col_std)
   output.append(WM_in)
   output.append(WM_in_res)
   output.append(JC_in)
   output.append(JC_out)
   output.append(load)
   output.append(lb_disk)
   output.append(LB_CON)
   output.append(LB)
   output.append(LL)
   output.append(JOB_DONE)
   output.append(JOB_ABORTED)
   output.append(lib_mysql_disk)
   
   fileusersstats = open(confvar['INSTALL_PATH'] + '/sensors/tmp/users_stats.txt','w')
   for i in range(0,len(users_stats)):
      fileusersstats.write(str(users_stats[i][0]) + ' ' + str(users_stats[i][1]) + ' ' + str(users_stats[i][2]) + ' ' + str(users_stats[i][3]) + ' ' + str(users_stats[i][4]) + ' ' + str(users_stats[i][5]) + ' ' + str(users_stats[i][6]) + ' ' + str(users_stats[i][7]) + ' ' + str(users_stats[i][8]) + '\n')

   fileusersstats.close()

   return output
