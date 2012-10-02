#!/usr/bin/python

import logging,os,time
import logpredef
import MySQLdb

def map_user(file_usermap,file_userstats,db):
   
   import user_class
   
   logger = logging.getLogger('map_user')
   MAP_FILE_ENABLED = True

   try:
      logger.info('Opening file for reading. File is ' + file_userstats)
      f_user = open(file_userstats,'r')
   except IOError:
      logger.error('Error opening file for reading. File is ' + file_userstats)
      logger.error('Returning None')
      return None

   try:
      logger.info('Opening file for reading. File is ' + file_usermap)
      f_map = open(file_usermap)
   except IOError:
      logger.error('Error opening file for reading. File is ' + file_usermap)
      logger.error('I will try to map using the db')
      MAP_FILE_ENABLED = False

   LEN_STATFILE = 10

   if MAP_FILE_ENABLED:
      usersmap = f_map.readlines()

   user_list = []

   for line in f_user:
      linesp = line.split('|')
      if len(linesp) != LEN_STATFILE:
         logger.warning('No user submitted or there are problems with the userstat file. Returning None')
         logger.info("linesp = " + str(linesp))
         logger.info("len(linesp) = " + str(len(linesp)))
         return None
      else:
         user_dn = linesp[0]
         user = user_class.WMSuser()
         user.dn = user_dn
         user.WMP_in = linesp[1]
         user.WMP_in_col = linesp[2]
         user.WMP_in_col_avg = linesp[3]
         user.WMP_in_col_std = linesp[4]
         user.WM_in_res = linesp[5]
         user.JC_out = linesp[6]
         user.JOB_DONE = linesp[7]
         user.JOB_ABORTED = linesp[8]


      MAP_FLAG = False

      if MAP_FILE_ENABLED:
         MAP_FLAG = False

         for line2  in usersmap:
            if line2.find(user.dn) != -1:
               MAP_FLAG = True
#               vo_role = line2[len(user.dn) + 1:]
#               vo_role_sp = vo_role.split()
#               user.VO = vo_role_sp[0]
               user.VO = line2[len(user.dn) + 1:].split()[len(line2[len(user.dn) + 1:].split())-2]
#               user.group = vo_role_sp[1]
               user.group = line2[len(user.dn) + 1:].split()[len(line2[len(user.dn) + 1:].split())-1]
               logger.info("User " + user.dn + " mapped into vo = " + user.VO + " role = " + user.group)

      if MAP_FLAG == False:
         logger.warning('It was not possible to map user using file: ' + user.dn)
         logger.info("Trying to use the db with past data")
         myquery = '''select dn,vo,role_group from map_users where dn = "''' + user.dn + '''" order by date desc;'''
         logger.info('Query is: ' + myquery)
         db.query(myquery)
         r = db.store_result()
         row = r.fetch_row(10000)
         if len(row) == 0:
            logger.info("It is impossible to map user. Using file and db. User will have null vo and group.")
         elif len(row) == 1:
            user.VO = row[0][1]
            user.group = row[0][2]
            logger.info('VO/GROUP found.  VO = ' + user.VO + '   GROUP = ' + user.group)
         else:
            logger.warning("User has many VO/role pair (exactly " + str(len(row)) + ". Using the most recent.")
            user.VO = row[0][1]
            user.group = row[0][2]               
            logger.info('VO/GROUP found.  VO = ' + user.VO + '   GROUP = ' + user.group)

      user_list.append(user)

   logger.info('All users were processed!!Returning function.')

   return user_list
