#!/usr/bin/python

def update_user_tmp(wmshost,lbhost,ENDDATE,deltat,user,db):
# Python import
   import os, commands, sys, fpformat
   import MySQLdb,time,datetime
   import logging
   import logpredef
   import query_to_insert_user_func

   def create_null(value):
      if value == None:
         return 'NULL'
      else:
         return "'" + str(value) + "'"

   def max_of_2_str(str1,str2):
      if str(str1).isdigit():
         val1 = float(str(str1))
      else:
         val1 = 'Null'
      if str(str2).isdigit():
         val2 = float(str(str2))
      else:
         val2 = 'Null'

      if val1 != 'Null' and  val2 != 'Null':
         return str(max(val1,val2))
      elif val1 != 'Null' and  val2 == 'Null':
         return str(val1)
      elif val1 == 'Null' and  val2 != 'Null':
         return str(val2)
      else:
         return 'Null'

   logger = logging.getLogger('update_user_tmp')

   myquery = "select ID_Rec, WMP_in, WMP_in_col, WMP_in_col_avg, WMP_in_col_std, WM_in, WM_in_res, JC_in, JC_out, JOB_DONE, JOB_ABORTED, deltat from users_tmp where wms='" + wmshost + "' and lbserver='" + lbhost + "' and dn=" + '''"''' + str(user.dn) + '''"''' + " and `date` = '" + ENDDATE + "' LIMIT 1;"

   logger.info('Query is: ' + myquery)
   db.query(myquery)
   r = db.store_result()
   row = r.fetch_row(10000)
   #print len(row)
   if len(row) > 0 :
      row_to_be_changed = ' WMP_in = ' +  str(row[0][1]) + ' WMP_in_col = ' +  str(row[0][2]) + ' WMP_in_col_avd = ' +  str(row[0][3]) + ' WMP_in_col_std = ' +  str(row[0][4])  + ' WM_in = ' +  str(row[0][5]) + ' WM_in_res = ' +  str(row[0][6]) + ' JC_in = ' +  str(row[0][7]) + ' JC_out = ' +  str(row[0][8]) + ' JOB_DONE = ' +  str(row[0][9]) + ' JOB_ABORTED = ' +  str(row[0][10]) + ' deltat = ' +  str(row[0][11]) + ' user = ' +  user.dn + ' wms = ' +  wmshost + ' lb = ' +  lbhost + ' ENDDATE = ' +  ENDDATE
      logger.info("Row to be changed = " + row_to_be_changed)

      WMP_in =  max_of_2_str(str(user.WMP_in),row[0][1])
      WMP_in_col = max_of_2_str(str(user.WMP_in_col),row[0][2])
      WMP_in_col_avg = max_of_2_str(str(user.WMP_in_col_avg),row[0][3])
      WMP_in_col_std = max_of_2_str(str(user.WMP_in_col_std),row[0][4])
      WM_in = max_of_2_str(str(user.WM_in),row[0][5])
      WM_in_res = max_of_2_str(str(user.WM_in_res),row[0][6])
      JC_in = max_of_2_str(str(user.JC_in),row[0][7])
      JC_out = max_of_2_str(str(user.JC_out),row[0][8])
      job_done  = max_of_2_str(str(user.JOB_DONE),row[0][9])
      job_aborted  = max_of_2_str(str(user.JOB_ABORTED),row[0][10])


      update_query = "UPDATE users_tmp SET WMP_in = '" + WMP_in + "',WMP_in_col = '" + WMP_in_col + "', WMP_in_col_avg = '" + WMP_in_col_avg + "', WMP_in_col_std = '" + WMP_in_col_std + "', WM_in = '" + WM_in + "', WM_in_res = '" + WM_in_res + "', JC_in  = '" + JC_in + "', JC_out = '" + JC_out + "', JOB_DONE = '" + job_done + "', JOB_ABORTED = '" + job_aborted + "', deltat = '" + str(deltat) + "' WHERE `date` = '" + ENDDATE + "' AND wms='" + wmshost + "' and lbserver = '" + lbhost + "' and dn = " + '''"''' + user.dn + '''"''' + " LIMIT 1;"

      logger.info('Query is: ' + update_query)
      db.query(update_query)

   else:
      logger.warning("I found NO row to be updated!!! Inserting a new one")
      myquery,myquery_tmp = query_to_insert_user_func.query_to_insert_user(wmshost,lbhost,ENDDATE,str(deltat),user,db,True)
      logger.info('Query is: ' + myquery_tmp)
      db.query(myquery_tmp)

   return 0
