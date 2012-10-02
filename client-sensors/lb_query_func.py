#/usr/bin/python

import os, sys
import os, commands, sys, fpformat
import MySQLdb,time,datetime
import lb_sensor_func
import readconf_func
import wmsdata_class

def lb_query(lbhost,STARTDATE,ENDDATE,DBTYPE):

   #Initializing logger
   import logging
   logger = logging.getLogger('lb_query')

   confvar = readconf_func.readconf();

   users_stats = []   
   # Establish a connection

   if DBTYPE == 'LBPROXY':
      lbhost = confvar['LBPROXY_DB_HOST']
      dbuser = confvar['LBPROXY_DB_USER']
      dbname = confvar['LBPROXY_DB_NAME']
   elif DBTYPE == 'LBSERVER':
      lbhost = confvar['LB_DB_HOST']
      dbuser = confvar['LB_DB_USER']
      dbname = confvar['LB_DB_NAME']

   logger.info('Establishing a connection with mysql DB')
   db = MySQLdb.connection(host = lbhost , user = dbuser , db = dbname, passwd = confvar['SERVER_MYSQL_PASSWORD'][1:-1])

################ MAIN DATA CONTAINER LIST INITIALIZATION ######
   wmsdata_list = []
###############################################################

   def put_into_wmsdata(wmsdata_list,wmshostname,userdn,fieldlist,valuelist):
      wmsFOUND = False
      for wmsdata in wmsdata_list:
         if wmsdata.host == wmshostname:
            wmsFOUND = True
            try:
               wmsdata.add_user(userdn)
            except wmsdata_class.UserPresent:
#              logger.warning('User Already present in wmdata for host: ' + wmsdata.host)
               for field in fieldlist:
                  wmsdata[userdn][field] = valuelist[fieldlist.index(field)]
      if not wmsFOUND:
         wmsdata = wmsdata_class.wmsdata(wmshostname)
         wmsdata.add_user(userdn)
         for field in fieldlist:
            wmsdata[userdn][field] = valuelist[fieldlist.index(field)]
         wmsdata_list.append(wmsdata)


   # Run a MySQL query to find the number of single jobs submitted in a given time interval PER USER and PER WMS
   logger.info('Running a MySQL query to find the number of single jobs submitted in a given time interval PER USER and PER WMS')
   querystr = "select users.cert_subj,host,COUNT(DISTINCT(events.jobid)) from events,short_fields inner join users on events.userid=users.userid where events.event=short_fields.event and code='17' and time_stamp>'" + STARTDATE + "' and time_stamp <='" + ENDDATE + "' and events.jobid=short_fields.jobid and name='NSUBJOBS' and value='0' group by users.cert_subj,host;"
   logger.info('Query is : ' + querystr)   
   db.query(querystr)
   r = db.store_result()
   # Iterate through the result set
   WMP_in = 0
   if r:
      for i in range(1,r.num_rows() + 1):
        row = r.fetch_row()
      #  logger.debug('FOUND ROW: ' + row )
        if row:
          dn = row[0][0]
          rowhost = row[0][1]
          rowWMP_in = row[0][2]

          put_into_wmsdata(wmsdata_list,rowhost,dn,['WMP_in'],[rowWMP_in])          

######################################################################################################################
### We decided to take anymore the avg and the std of nodes per collection because they are not summable on more lb   
### WHat we do is to take PER USER the total number of jobs in collection, the min and max of nodes per collection
### This are summable and avg calculation can be done on collector side
### Anyway we sum over user on sensors side and we return alse the total number of jobs per collection, min and max of nodes PER WMS
### Summing over wmsdata data will be done at the end of this function ore on the wrapper if the wmsdata_list is returned
##########################################################################################################################

# Run a query to find per user and per host the number of collection, the total number of nodes in collection the min and max of nodes per collection

   logger.info('Running a query to find per user and per host the number of collection, the total number of nodes in collection the min and max of nodes per collection')
   querystr = "select users.cert_subj, host, COUNT(value), sum(value), min(value),max(value) from events,short_fields inner join users on events.userid=users.userid where events.event=short_fields.event and code='17' and time_stamp>'" + STARTDATE + "' and time_stamp <='" + ENDDATE + "' and events.jobid=short_fields.jobid and name='NSUBJOBS' and short_fields.event='0' and value>'0' group by users.cert_subj,host"
   logger.info('Query is : ' + querystr)
   db.query(querystr)
   r = db.store_result()
   # Iterate through the result set
   if r:
      for i in range(1,r.num_rows() + 1):
         row = r.fetch_row()
         if row:
            dn = row[0][0]
            rowhost = row[0][1]
            rowWMP_in_col = row[0][2]
            rowWMP_in_col_nodes = row[0][3]
            rowWMP_in_col_min_nodes = row[0][4]
            rowWMP_in_col_max_nodes = row[0][5]

            put_into_wmsdata(wmsdata_list,rowhost,dn,['WMP_in_col','WMP_in_col_nodes','WMP_in_col_min_nodes','WMP_in_col_max_nodes'],[rowWMP_in_col,rowWMP_in_col_nodes,rowWMP_in_col_min_nodes,rowWMP_in_col_max_nodes])
                 
#  Run a query to find PER USER and PER WMS the number of jobs enqued to WM from WMP in a given time interval
   logger.info("Run a query to find PER USER and PER WMS the number of jobs enqued to WM from WMP in a given time interval")
   querystr = "select  users.cert_subj, host, COUNT(events.jobid) from events,short_fields inner join users on events.userid=users.userid where events.event=short_fields.event and code='4' and time_stamp >'" + STARTDATE + "' and time_stamp <='" + ENDDATE + "' and events.jobid=short_fields.jobid and events.event=short_fields.event and  prog='NetworkServer' and name='RESULT' and value='OK' group by users.cert_subj,host;"
   logger.info('Query is : ' + querystr)
   db.query(querystr)
   r = db.store_result()
   if r:
      for i in range(1,r.num_rows() + 1):
        row = r.fetch_row()
        if row:
          dn = row[0][0]
          rowhost = row[0][1]
          rowWM_in = row[0][2]

          put_into_wmsdata(wmsdata_list,rowhost,dn,['WM_in'],[rowWM_in])

   # Run a MySQL query to find the number both collection and single jobs enqueued to WM in a given time interval from LogMonitor (i.e. Resubmitted)
   logger.info('Run a MySQL query to find the number both collection and single jobs enqueued to WM in a given time interval from LogMonitor (i.e. Resubmitted) PER USER and PER WMS')
   querystr="select users.cert_subj,host,COUNT(DISTINCT(events.jobid)) from events,short_fields inner join users on events.userid=users.userid where code='4' and time_stamp >'" + STARTDATE + "' and time_stamp <='" + ENDDATE + "' and events.jobid=short_fields.jobid and events.event=short_fields.event and name='RESULT' and value='OK' and prog='LogMonitor' group by users.cert_subj, host;"
   logger.info('Query is : ' + querystr)   
   db.query(querystr)
   r = db.store_result()
   # Iterate through the result set
   if r:
      for i in range(1,r.num_rows() + 1):
        row = r.fetch_row()
        if row:
          usernew = row[0][0]
          index = row[0][0].find('/CN=proxy/CN=proxy')
          if index != -1:
             usernew=row[0][0][0:index]
          dn = usernew
          rowhost = row[0][1]
          rowWM_in_res = row[0][2]
          
          put_into_wmsdata(wmsdata_list,rowhost,dn,['WM_in_res'],[rowWM_in_res])

   # Run a MySQL query to find the number single jobs enqueued to Job Controller from WM in a given time interval PER WMS and PER USER
   logger.info('Run a MySQL query to find the number single jobs enqueued to Job Controller from WM in a given time interval per USER and PER WMS')
   querystr="select users.cert_subj,host,COUNT(DISTINCT(events.jobid)) from events,short_fields inner join users on events.userid=users.userid where code='4' and time_stamp >'" + STARTDATE + "' and time_stamp <='" + ENDDATE + "' and events.jobid=short_fields.jobid and events.event=short_fields.event and name='RESULT' and value='OK' and prog='WorkloadManager' group by users.cert_subj,host;"
   logger.info('Query is : ' + querystr)   
   db.query(querystr)
   r = db.store_result()
   # Iterate through the result set
   if r:
      for i in range(1,r.num_rows() + 1):
        row = r.fetch_row()
        if row:
          usernew = row[0][0]
          index = row[0][0].find('/CN=proxy/CN=proxy')
          if index != -1:
             usernew=row[0][0][0:index]
          dn = usernew
          rowhost = row[0][1]
          rowJC_in = row[0][2]

          put_into_wmsdata(wmsdata_list,rowhost,dn,['JC_in'],[rowJC_in])

   # Run a MySQL query to find the number single jobs enqueued to Condor from Job Controller in a given time interval PER USER and PER WMS
   logger.info('Run a MySQL query to find the number single jobs enqueued to Condor from Job Controller in a given time interval PER USER and PER WMS')
   querystr="select users.cert_subj,host,COUNT(DISTINCT(events.jobid)) from events,short_fields inner join users on events.userid=users.userid where code='1' and time_stamp >'" + STARTDATE + "' and time_stamp <='" + ENDDATE + "' and events.jobid=short_fields.jobid and events.event=short_fields.event and name='RESULT' and value='OK' and prog='JobController' group by users.cert_subj,host;"
   logger.info('Query is : ' + querystr)   
   db.query(querystr)
   r = db.store_result()
   # Iterate through the result set
   if r:
      for i in range(1,r.num_rows() + 1):
        row = r.fetch_row()
        if row:
          usernew = row[0][0]
          index = row[0][0].find('/CN=proxy/CN=proxy')
          if index != -1:
             usernew=row[0][0][0:index]
          dn = usernew
          rowhost = row[0][1]
          rowJC_out = row[0][2]

          put_into_wmsdata(wmsdata_list,rowhost,dn,['JC_out'],[rowJC_out])

  # Run a MySQL query to find the number of jobs done in a given time interval PER USER and PER WMS
   logger.info('Run a MySQL query to find the number single jobs done successfully in a given time interval PER USER and PER WMS')
   querystr="select users.cert_subj,host,COUNT(DISTINCT(events.jobid)) from events,short_fields inner join users on events.userid=users.userid where events.jobid=short_fields.jobid and code='10' and time_stamp >'" + STARTDATE + "' and time_stamp <='" + ENDDATE + "' and prog='LogMonitor' and name='REASON' and (value='Job terminated successfully' or value='Job Terminated Successfully') group by users.cert_subj,host;"
   logger.info('Query is : ' + querystr)
   db.query(querystr)
   r = db.store_result()
   # Iterate through the result set
   if r:
      for i in range(1,r.num_rows() + 1):
        row = r.fetch_row()
        if row:
          usernew = row[0][0]
          index = row[0][0].find('/CN=proxy/CN=proxy')
          if index != -1:
             usernew=row[0][0][0:index]
          dn = usernew
          rowhost = row[0][1]
          rowJOB_DONE = row[0][2]

          put_into_wmsdata(wmsdata_list,rowhost,dn,['JOB_DONE'],[rowJOB_DONE])

  # Run a MySQL query to find the number of jobs aborted in a given time interval PER USER and PER WMS
   logger.info('Run a MySQL query to find the number single jobs aborted in a given time interval PER USER and PER WMS')
   querystr="select users.cert_subj,host,COUNT(DISTINCT(events.jobid)) from events inner join users on events.userid=users.userid where code='12' and time_stamp >'" + STARTDATE + "' and time_stamp <='" + ENDDATE + "' group by users.cert_subj,host;"

   logger.info('Query is : ' + querystr)
   db.query(querystr)
   r = db.store_result()
   # Iterate through the result set
   if r:
      for i in range(1,r.num_rows() + 1):
        row = r.fetch_row()
        if row:
          usernew = row[0][0]
          index = row[0][0].find('/CN=proxy/CN=proxy')
          if index != -1:
             usernew=row[0][0][0:index]
          dn = usernew
          rowhost = row[0][1]
          rowJOB_ABORTED = row[0][2]

          put_into_wmsdata(wmsdata_list,rowhost,dn,['JOB_ABORTED'],[rowJOB_ABORTED])

# Run a MySQL query to find the DEST_CE of jobs in a given time interval PER WMS
   logger.info('Run a MySQL query to find  DEST_CE of jobs in a given time interval PER WMS')

##### old ce query - this double counts ce for jobs landed onto cream ce

   #querystr="select value, host, COUNT(value) from (select DISTINCT(short_fields.event),events.jobid, short_fields.value, host from events,short_fields where events.jobid=short_fields.jobid  and time_stamp >'" + STARTDATE + "' and time_stamp <='" + ENDDATE + "' and prog='WorkloadManager' and name='DEST_HOST' and value!='localhost' and value!='unavailable' and code='15') as temp group by value, host;"
##################################################

##### New query not to double counting ce for jobs landed onto cream ce
   querystr="select value,host,  count(value) from (select distinct(short_fields.jobid), value, host from short_fields inner join events where events.code='15' and events.prog = 'WorkloadManager' and name='DEST_HOST' and time_stamp > '" + STARTDATE + "' and time_stamp <='" + ENDDATE + "' and value!='localhost' and value!='unavailable' and events.jobid=short_fields.jobid) as temp group by value, host;"
##################################################

   logger.info('Query is : ' + querystr)
   db.query(querystr)
   r = db.store_result()
   # Iterate through the result set
   if r:
      for i in range(1,r.num_rows() + 1):
         row = r.fetch_row()
         if row:
            rowCE      = row[0][0]
            rowhost    = row[0][1]
            rowCEcount = row[0][2]
            wmsFOUND = False
            for wmsdata in wmsdata_list:
               if wmsdata.host == rowhost:
                  wmsFOUND = True
                  try:
                     wmsdata.add_ce(rowCE)
                     wmsdata.add_ce_count(rowCE,rowCEcount)
                  except wmsdata_class.CEPresent:
#                   logger.warning('User Already present in wmdata for host: ' + wmsdata.host)
                    wmsdata.add_CE_count(rowCEcount)
            if not wmsFOUND:
               wmsdata = wmsdata_class.wmsdata(rowhost)
               wmsdata.add_ce(rowCE)
               wmsdata.add_ce_count(rowCE,rowCEcount)
               wmsdata_list.append(wmsdata)



# Run a MySQL query to find the LB used to store the jobs in a given time interval 
# Available only if DBTYPE = LBPROXY
 
   if DBTYPE == 'LBPROXY':
      logger.info('Run a MySQL query to find the LB used to store the jobs in a given time interval')
      querystr="select distinct dg_jobid from jobs inner join events on jobs.jobid=events.jobid where events.code = '17' and time_stamp > '" + STARTDATE + "' and time_stamp < '" + ENDDATE + "';"
      logger.info('Query is : ' + querystr)
      db.query(querystr)
      r = db.store_result()
   # Iterate through the result set
      if r:
         for i in range(1,r.num_rows() + 1):
            row = r.fetch_row()
            if row:
               rowLB      = row[0][0]
               LBstr = LBstr = rowLB[rowLB.find('//') + 2 : rowLB.find(':9000') ]
               for wmsdata in wmsdata_list:
                  wmsdata.add_lb(LBstr)

   db.close()
  
#   filename= confvar['INSTALL_PATH'] +'/sensors//tmp/USERSTATS_' +  lbhost + '_' + wmshost + '.txt'

#   fileusersstats = open(filename,'w')
#   fileusersstats.write('START OF FILE\n')
#   for i in range(0,len(users_stats)):
#      fileusersstats.write(str(users_stats[i][0]) + '|' + str(users_stats[i][1]) + '|' + str(users_stats[i][2]) + '|' + str(users_stats[i][3]) + '|' + str(users_stats[i][4]) + '|' + str(users_stats[i][5]) + '|' + str(users_stats[i][6]) + '|' + str(users_stats[i][7]) + '|' + str(users_stats[i][8]) + '|\n')

#   fileusersstats.write('END OF FILE\n')
#   fileusersstats.close()

   return wmsdata_list
