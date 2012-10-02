#!/usr/bin/python

def query_to_insert_user(wmshost,lbhost,ENDDATE,step,user,db,ONLY_TMP):

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

   def SSum(value1,value2,type):

      if value1 == 'NULL':
         value1 = None
      if value2 == 'NULL':
         value2 = None

      if type == 'int':
         if value1 != None and value2 != None:
            sum = int(value1) + int(value2)
         if value1 == None and value2 != None:
            sum = int(value2)
         if value2 == None and value1 != None:
            sum = int(value1)
         if value1 == None and value2 == None:
            sum = None
      if type == 'float':
         if value1 != None and value2 != None:
            sum = float(value1) + float(value2)
         if value1 == None and value2 != None:
            sum = float(value2)
         if value2 == None and value1 != None:
            sum = float(value1)
         if value1 == None and value2 == None:
            sum = None
      
      return sum
      
   logger = logging.getLogger('query_to_insert_user')
   TODAY = ENDDATE[:10]
   
   ONE_WEEK_AGO = time.strftime("%Y-%m-%d %H:%M:%S",time.localtime(time.mktime(time.strptime(ENDDATE,"%Y-%m-%d %H:%M:%S")) - 604800))

   # We need to check in here if the user is already present with a NULL VO in the db, both users and users_tmp table
   # If so, a flag must control what to do.
   # If the flag is true the NULL vo jobs must be assigned to the user with the actual vo
   # Otherwise the NULL job vo must not be touched

   ENABLE_ASSIGN_NULL = True

   if create_null(user.VO) != 'NULL':
         logger.info("Looking if this user is present in the db with a NULL VO")
         myquery = "select ID_Rec, WMP_in, WMP_in_col, WMP_in_col_avg, WMP_in_col_std, WM_in_res, JC_out, JOB_DONE, JOB_ABORTED from users where wms='" + wmshost + "' and lbserver='" + lbhost + "' and dn=" + '''"''' + str(user.dn) + '''"''' + " and VO is NULL and `date` >= '" + ONE_WEEK_AGO  + "';"
         logger.info('Query is: ' + myquery)
         db.query(myquery)
         r_null = db.store_result()
         row_null = r_null.fetch_row(10000)
         if len(row_null) > 0:
            logger.warning("This user is present in the db with a NULL VO")
            if ENABLE_ASSIGN_NULL:
                     logger.info("ASSIGN_NULL flag is true. Let's assign NULL VO jobs to the mapped user")
                     #MP_in = 0
                     #WMP_in_col = 0
                     #WMP_in_col_avg = 0
                     #WMP_in_col_std = 0
                     #WM_in = 0
                     #WM_in_res = 0
                     #JC_in = 0
                     #JC_out = 0
                     #JOB_DONE = 0
                     #JOB_ABORTED = 0

                     for res in row_null:
                        #WMP_in = SSum(WMP_in,res[1],'int')
                        #WMP_in_col = SSum(WMP_in_col,res[2],'int')
                        #WMP_in_col_avg = SSum(WMP_in_col_avg,res[3],'float')
                        #WMP_in_col_std = SSum(WMP_in_col_std,res[4],'float')
                        #WM_in = SSum(WM_in,None,'int')
                        #WM_in_res = SSum(WM_in_res,res[5],'int')
                        #JC_in = SSum(JC_in,None,'int')
                        #JC_out = SSum(JC_out,res[6],'int')
                        #JOB_DONE = SSum(JOB_DONE,res[7],'int')
                        #JOB_ABORTED = SSum(JOB_ABORTED,res[8],'int')

                        # remove null entries from users table...
                        #logger.info("Removing old entries in user table, where the user was mapped to NULL VO")
                        #myquery =  "DELETE FROM users WHERE ID_Rec=" + res[0] + " LIMIT 1;"
                        #logger.info("Query is :" + myquery)
                        #db.query(myquery)

                        # For every row change the VO from NULL to VO
                        logger.info("Assign null job in the users_tmp table to the current VO.")
                        myquery =  "UPDATE users set vo = '" + str(user.VO) + "', role_group = '" + str(user.group) + "' where ID_Rec=" + res[0] + " LIMIT 1;"
                        logger.info("Query is :" + myquery)
                        db.query(myquery)

                     # yes, but now we need to do something also with the users_tmp table
                     # ALl we can do is to assign the NULL job to the brand new matched vo
                     logger.info("Assign null job in the users_tmp table to the current VO.")
                     myquery =  "UPDATE users_tmp set vo = '" + str(user.VO) + "', role_group = '" + str(user.group) + "' where wms='" + wmshost + "' and lbserver='" + lbhost + "' and dn=" + '''"''' + str(user.dn) + '''"''' + " and VO is NULL and `date` >= '" + ONE_WEEK_AGO + "';"
                     logger.info("Query is :" + myquery)
                     db.query(myquery)
                        

                        #user.WMP_in = SSum(user.WMP_in,WMP_in,'int')
                        #user.WMP_in_col = SSum(user.WMP_in_col,WMP_in_col,'float')       #this is buggy
                        #user.WMP_in_col_avg = SSum(user.WMP_in_col_avg,WMP_in_col_avg,'float')   #this is buggy
                        #user.WM_in = SSum(user.WM_in,WM_in,'int')
                        #user.WM_in_res = SSum(user.WM_in_res,WM_in_res,'int')
                        #user.JC_in = SSum(user.JC_in,JC_in,'int')
                        #user.JC_out = SSum(user.JC_out,JC_out,'int')
                        #user.JOB_DONE = SSum(user.JOB_DONE,JOB_DONE,'int')
                        #user.JOB_ABORTED = SSum(user.JOB_ABORTED,JOB_ABORTED,'int')

         else:
           logger.info("No. User was not present with the NULL VO")

   ############################################################
   #           END OF NULL CHECK                              #
   ############################################################

   query_tmp = "INSERT INTO `wmsmon`.`users_tmp` (`ID_Rec`, `date`, `wms`,`lbserver`,`dn`,`vo`,`role_group`,`WMP_in`, `WMP_in_col`,`WMP_in_col_avg`,`WMP_in_col_std`, `WM_in`, `WM_in_res`, `JC_in`, `JC_out`,`JOB_DONE`,`JOB_ABORTED`,`deltat`) VALUES (NULL,'" + ENDDATE + "', '" + wmshost + "', '" + lbhost + "'" + ''', "''' + user.dn +  '''"''' + ", " + create_null(user.VO) + ", " + create_null(user.group)  + ", " + create_null(user.WMP_in) +", " + create_null(user.WMP_in_col) +", " + create_null(user.WMP_in_col_avg) + ", " + create_null(user.WMP_in_col_std) + ", " + create_null(user.WM_in) + ", " + create_null(user.WM_in_res) + ", " + create_null(user.JC_in) +", " + create_null(user.JC_out) + ", " + create_null(user.JOB_DONE) + ", " + create_null(user.JOB_ABORTED) + ", " + "'" + step +"');"

   if ONLY_TMP:
      return None,query_tmp


   if create_null(user.VO) == 'NULL':
       vostring = vostring = "vo is NULL"
   else:
       vostring = "vo = " + create_null(user.VO)
   if create_null(user.group) == 'NULL':
         groupstring = "role_group is NULL"
   else:
         groupstring = "role_group = " + create_null(user.group)



   myquery = "select ID_Rec, WMP_in, WMP_in_col, WMP_in_col_avg, WMP_in_col_std, WM_in_res, JC_out, JOB_DONE, JOB_ABORTED from users where wms='" + wmshost + "' and lbserver='" + lbhost + "' and dn=" + '''"''' + str(user.dn) + '''"''' + " and " + vostring + " and " + groupstring + " and `date` like '" + TODAY + "%';"

   logger.info('Query is: ' + myquery)
   db.query(myquery)
   r = db.store_result()
   row = r.fetch_row(10000)

   QUERY = ''


   if len(row) == 0:
      # it's the first time the user is subtinng to this wms/lb pair with this vo and gruoup -> query to insert
      logger.info("Today it's the first time this user is submitting to this wms/lb pair using this vo and group -> query to insert")

      # Here we should check if the user is present but not mapped. i.e. with vo = NULL
      # in this case the job of the NULL vo could be assigned to the mapped user. This is not very precise so this behavior must be controlled by a bool flag


      QUERY = "INSERT INTO `wmsmon`.`users` (`ID_Rec`, `date`, `wms`,`lbserver`,`dn`,`vo`,`role_group`,`WMP_in`, `WMP_in_col`,`WMP_in_col_avg`,`WMP_in_col_std`, `WM_in`, `WM_in_res`, `JC_in`, `JC_out`,`JOB_DONE`,`JOB_ABORTED`) VALUES (NULL,'" + ENDDATE + "', '" + wmshost + "', '" + lbhost +  "'" + ''', "''' + user.dn +  '''"''' + ", " + create_null(user.VO) + ", " + create_null(user.group)  + ", " + create_null(user.WMP_in) +", " + create_null(user.WMP_in_col) +", " + create_null(user.WMP_in_col_avg) + ", " + create_null(user.WMP_in_col_std) + ", " + create_null(user.WM_in) + ", " + create_null(user.WM_in_res) + ", " + create_null(user.JC_in) +", " + create_null(user.JC_out) + ", " + create_null(user.JOB_DONE) + ", " + create_null(user.JOB_ABORTED) + ");"

   elif len(row) == 1 :

      logger.info("User already present in db today (Only once). Let's sum the values")

      WMP_in = SSum(user.WMP_in,row[0][1],'int')
      WMP_in_col = SSum(user.WMP_in_col,row[0][2],'int')
      WMP_in_col_avg = SSum(user.WMP_in_col_avg,row[0][3],'float') #this is buggy
      WMP_in_col_std = SSum(user.WMP_in_col_std,row[0][4],'float') #this is buggy
      WM_in = SSum(user.WM_in,None,'int')
      WM_in_res = SSum(user.WM_in_res,row[0][5],'int')
      JC_in = SSum(user.JC_in,None,'int')
      JC_out = SSum(user.JC_out,row[0][6],'int')
      JOB_DONE = SSum(user.JOB_DONE,row[0][7],'int')
      JOB_ABORTED = SSum(user.JOB_ABORTED,row[0][8],'int')

      QUERY = "UPDATE wmsmon.users SET `date`= '" + ENDDATE + "', WMP_in =" + create_null(WMP_in) +", WMP_in_col=" + create_null(WMP_in_col) +", WMP_in_col_avg=" + create_null(WMP_in_col_avg) + ", WMP_in_col_std=" + create_null(WMP_in_col_std) + ", WM_in=" + create_null(WM_in) + ", WM_in_res=" + create_null(WM_in_res) + ", JC_in=" + create_null(JC_in) +", JC_out=" + create_null(JC_out) + ", JOB_DONE=" + create_null(JOB_DONE) + ", JOB_ABORTED=" + create_null(JOB_ABORTED) + " WHERE ID_Rec=" + row[0][0] + " LIMIT 1;"

   elif len(row) > 1:

      logger.warning("User present today in db more than once with same vo/group ad wms/lb pair. This is a weird situation.")
      logger.warning("Something went wrong with previous data collection. Please check, len(row) = " + str(len(row)) + ".")
      logger.warning("Summing all data, removing old entries and inserting a new one. User is:" + user.dn)

      WMP_in = user.WMP_in
      WMP_in_col = user.WMP_in_col
      WMP_in_col_avg = user.WMP_in_col_avg
      WMP_in_col_std = user.WMP_in_col_std
      WM_in = user.WM_in
      WM_in_res = user.WM_in_res
      JC_in = user.JC_in
      JC_out = user.JC_out
      JOB_DONE = user.JOB_DONE
      JOB_ABORTED = user.JOB_ABORTED

      for res in row:
         WMP_in = SSum(WMP_in,res[1],'int')
         WMP_in_col = SSum(WMP_in_col,res[2],'int')
         WMP_in_col_avg = SSum(WMP_in_col_avg,res[3],'float')  #this is buggy
         WMP_in_col_std = SSum(WMP_in_col_std,res[4],'float')  #this is buggy
         WM_in = SSum(WM_in,None,'int')
         WM_in_res = SSum(WM_in_res,res[5],'int')
         JC_in = SSum(JC_in,None,'int')
         JC_out = SSum(JC_out,res[6],'int')
         JOB_DONE = SSum(JOB_DONE,res[7],'int')
         JOB_ABORTED = SSum(JOB_ABORTED,res[8],'int')

         logger.info("Removing old entries")
         myquery =  "DELETE FROM users WHERE ID_Rec=" + res[0] + " LIMIT 1;"
         logger.info("Query is :" + myquery)
         db.query(myquery)

      QUERY = "INSERT INTO `wmsmon`.`users` (`ID_Rec`, `date`, `wms`,`lbserver`,`dn`,`vo`,`role_group`,`WMP_in`, `WMP_in_col`,`WMP_in_col_avg`,`WMP_in_col_std`, `WM_in`, `WM_in_res`, `JC_in`, `JC_out`,`JOB_DONE`,`JOB_ABORTED`) VALUES (NULL,'" + ENDDATE + "', '" + wmshost + "', '" + lbhost + "'" + ''', "''' + user.dn +  '''"''' + ", " + create_null(user.VO) + ", " + create_null(user.group)  + ", " + create_null(WMP_in) +", " + create_null(WMP_in_col) +", " + create_null(WMP_in_col_avg) + ", " + create_null(WMP_in_col_std) + ", " + create_null(WM_in) + ", " + create_null(WM_in_res) + ", " + create_null(JC_in) +", " + create_null(JC_out) + ", " + create_null(JOB_DONE) + ", " + create_null(JOB_ABORTED) + ");"
 
   return QUERY,query_tmp
