#!/usr/bin/python

def update_user_stats_table(wmshost,lbhost,ENDDATE,user,db):
# Python import
   import os, commands, sys, fpformat
   import MySQLdb,time,datetime
   import logging
   import logpredef

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

   logger = logging.getLogger('update_user_stats_table')

   DAY_TO_UPDATE = ENDDATE[:10]

   myquery = "SELECT distinct(vo),role_group from (select distinct(users.role_group), users.vo FROM `users` where dn = " + '''"''' + user.dn + '''"''' + " and users.date like '" + DAY_TO_UPDATE + "%' ) as temp;"
   logger.info('Query is: ' + myquery)
   db.query(myquery)
   r = db.store_result()
   for row in r.fetch_row(10000):
      vo = create_null(row[0])
      if vo == 'NULL':
         logger.debug("DEBUG UPDATE: vo is " + vo)
         vostring = "vo is NULL"
         logger.debug("DEBUG UPDATE: vostring is " + vostring)
      else:
         logger.debug("DEBUG UPDATE: vo is " + vo)
         vostring = "vo = " + vo
         logger.debug("DEBUG UPDATE: vostring is " + vostring)
      group = create_null(row[1])
      if group == 'NULL':
         groupstring = "role_group is NULL"
      else:
         groupstring = "role_group = " + group

      myquery2 = "select sum(WMP_in), sum(WMP_in_col), avg(WMP_in_col_avg), avg(WMP_in_col_std), sum(WM_in), sum(WM_in_res), sum(JC_in), sum(JC_out), sum(JOB_DONE), sum(JOB_ABORTED) from users_tmp where wms='" + wmshost + "' and lbserver='" + lbhost + "' and dn=" + '''"''' + str(user.dn) + '''"''' + "  and " + vostring + " and " + groupstring + " and users_tmp.date like '" + DAY_TO_UPDATE + "%' ;"

      logger.info('Query is: ' + myquery2)
      db.query(myquery2)
      r2 = db.store_result()
      row2 = r2.fetch_row(10000)

      myquery3 = "select WMP_in, WMP_in_col, WMP_in_col_avg, WMP_in_col_std, WM_in, WM_in_res, JC_in, JC_out, JOB_DONE, JOB_ABORTED from users where wms='" + wmshost + "' and lbserver='" + lbhost + "' and dn=" + '''"''' + str(user.dn) + '''"''' + "  and " + vostring + " and " + groupstring + " and users.date like '" + DAY_TO_UPDATE + "%';"
      logger.info('Query is: ' + myquery3)
      db.query(myquery3)
      r3 = db.store_result()
      row3 = r3.fetch_row(10000)

      if len(row3) == 0:

         logger.info("Found no line to be updated in user. But we have a user to be added from autoupdate. Inserting")
         myquery = "INSERT INTO `wmsmon`.`users` (`ID_Rec`, `date`, `wms`,`lbserver`,`dn`,`vo`,`role_group`,`WMP_in`, `WMP_in_col`,`WMP_in_col_avg`,`WMP_in_col_std`, `WM_in`, `WM_in_res`, `JC_in`, `JC_out`,`JOB_DONE`,`JOB_ABORTED`) VALUES (NULL,'" + ENDDATE + "', '" + wmshost + "', '" + lbhost + "', " + '''"''' + user.dn + '''"''' + ", " + create_null(user.VO) + ", " + create_null(user.group)  + ", " + create_null(user.WMP_in) +", " + create_null(user.WMP_in_col) +", " + create_null(user.WMP_in_col_avg) + ", " + create_null(user.WMP_in_col_std) + ", " + create_null(user.WM_in) + ", " + create_null(user.WM_in_res) + ", " + create_null(user.JC_in) +", " + create_null(user.JC_out) + ", " + create_null(user.JOB_DONE) + ", " + create_null(user.JOB_ABORTED) + ");"

         logger.info('Query is: ' + myquery)
         db.query(myquery)

      elif len(row3) == 1 :

         logger.info("Found a line to be update in users")
         wmp_in_sum  =  max_of_2_str(row2[0][0],row3[0][0])
         wmp_in_col_sum =  max_of_2_str(row2[0][1],row3[0][1])
         wmp_in_col_avg_sum  =  max_of_2_str(row2[0][2],row3[0][2])
         wmp_in_col_std_sum  =  max_of_2_str(row2[0][3],row3[0][3])
         wm_in_sum =  max_of_2_str(row2[0][4],row3[0][4])
         wm_in_res_sum  =  max_of_2_str(row2[0][5],row3[0][5])
         jc_in_sum =  max_of_2_str(row2[0][6],row3[0][6])
         jc_out_sum = max_of_2_str(row2[0][7],row3[0][7])
         job_done_sum = max_of_2_str(row2[0][8],row3[0][8])
         job_aborted_sum = max_of_2_str(row2[0][9],row3[0][9])

         myquery="UPDATE wmsmon.users SET WMP_in ='" + wmp_in_sum + "',WMP_in_col ='" + wmp_in_col_sum +"', WMP_in_col_avg = '" + wmp_in_col_avg_sum + "', WMP_in_col_std = '" + wmp_in_col_std_sum + "', WM_in = '" + wm_in_sum + "', WM_in_res = '" + wm_in_res_sum + "', JC_in  = '" + jc_in_sum + "', JC_out = '" + jc_out_sum + "', JOB_DONE = '" + job_done_sum + "', JOB_ABORTED = '" + job_aborted_sum + "' WHERE wms='" + wmshost + "' and lbserver='" + lbhost + "' and dn=" + '''"''' + str(user.dn) + '''"''' + " and vo = " + vo + " and role_group = " + group + " and `date` like '" + DAY_TO_UPDATE + "%' LIMIT 1;"

         logger.info('Query is: ' + myquery)
         db.query(myquery)

      else:

         logger.warning("User appear more than one with the same vo/group pair in users table.")
         logger.warning("This should not happen. Doing nothing, waiting for next iteration to repair the situation")
         logger.warning("User is: " + user.dn + "vo = " + vo + " group = " + group)

   return 0
