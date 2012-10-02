#!/usr/bin/python

import logging,os,time
import long_file_collector_func,logpredef
import MySQLdb

def get_WMS_usermap(host,send_file_OID,db,port):

   logger = logging.getLogger('get_WMS_usermap')


# SNMPv2-SMI::enterprises.10403.94.101.1 = STRING: "FILE CREATED = /root/wmsmon/bin/CE_MM.txt"

   filename = 'out_usermap_' + host + '_' + str(time.time()) + '.txt'

   logger.info('Opening file ' + filename + ' for writing')
   try:
      f = open(filename,'w')
   except IOError:
      logger.info('Cannot open file ' + filename + ' for writing.  Returning None')
      return None    

   logger.info('We can now try to get the usermap file')
   # We need here the long file collector function becaus we do not know a priori how long the file can be
   dataline = long_file_collector_func.long_file_collector(host,send_file_OID,port)

   datalinesp = dataline.split(';') 
   for line in datalinesp:
      line = line.strip().rstrip()
      if line != 'START' and line != 'END' and line != 'EOF':

         f.write(line + '\n')
         if len(line) > 1:
            print line
            vo_role = line[line[:line.rfind(' ')].rfind(' ') + 1:]
            print vo_role
            vo_role = vo_role.strip()
            vo_role = vo_role.rstrip()
            vo_rolesp = vo_role.split(' ')
            vo = vo_rolesp[0]
            role = vo_rolesp[1]
            user_dn = line[0:line.find(vo_role) - 1]
            user_dn = user_dn.strip()
            user_dn = user_dn.rstrip()
            logger.info("I found the following user: dn = " + user_dn + "VO = " + vo + "group/role = " + role)
            logger.info("Let's see if it is the case to isert it into the db for future mapping.") 
            myquery = '''select dn,vo,role_group from map_users where dn = "''' + user_dn + '''";'''
            logger.info('Query is: ' + myquery)
            db.query(myquery)
            r = db.store_result()
            row = r.fetch_row(10000)
            DATENOW = time.strftime("%Y-%m-%d %H:%M:%S",time.localtime())
            if len(row) == 0:
               # it's the first time the user is subtinng to this wms/lb pair with this vo and gruoup -> query to insert
               logger.info("It's the first time this user is seen by the monitor inserting into the map_users table")
               myquery = "insert into map_users (ID_REC, date, dn, vo, role_group) values ('NULL', '" + DATENOW +  "'," + ''' "''' + user_dn + '''"''' + ", '" + vo + "', '" + role + "');"
               logger.info('Query is: ' + myquery)
               db.query(myquery) 
            else:
               logger.info("User already present in map_users table. Let's check if VO/group is the same")
               INSERT = True
               for result in row:
                  if result[1] == vo and result[2] == role:
                     logger.info("Ok, same VO/group. Not inserting")
                     INSERT = False
                     break

               if INSERT:
                  logger.info("This VO/group are not present inserting")
                  myquery = "insert into map_users (ID_REC, date, dn, vo, role_group) values ('NULL', '" + DATENOW +  "'," + ''' "''' + user_dn + '''"''' + ", '" + vo + "', '" + role + "');"
                  logger.info('Query is: ' + myquery)
                  db.query(myquery)


   logger.info('Data got and written to file')

   f.close()

   return filename
