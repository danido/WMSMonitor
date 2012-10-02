#!/usr/bin/python

def update_CE_stats_table(wmshost,lbhost,ENDDATE,ce_name,ceocc,db,VOCE):
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

   logger = logging.getLogger('update_CE_stats_table')

   DAY_TO_UPDATE = ENDDATE[:10]

   myquery2 = "select sum(occ) from ce_stats_tmp where wms='" + wmshost + "' and lbserver='" + lbhost + "' and ce='" + ce_name + "' and ce_stats_tmp.date like '" + DAY_TO_UPDATE + "%' ;"

   logger.info('Query is: ' + myquery2)
   db.query(myquery2)
   r2 = db.store_result()
   row2 = r2.fetch_row(10000)

   myquery3 = "select sum(occ) from ce_stats where wms='" + wmshost + "' and lbserver='" + lbhost + "' and ce='" + ce_name + "' and ce_stats.date like '" + DAY_TO_UPDATE + "%' ;"
   logger.info('Query is: ' + myquery3)
   db.query(myquery3)
   r3 = db.store_result()
   row3 = r3.fetch_row(10000)

   if len(row3) == 0:

      logger.info("Found no line to be updated in ce_stats. But we have a CE to be added from autoupdate. Inserting.")
      myquery = "INSERT INTO `wmsmon`.`ce_stats` (`ID_Rec`, `date`, `wms`,`lbserver`,`ce`,`occ`,`VO`) VALUES (NULL,'" + ENDDATE + "', '" + wmshost + "', '" + lbhost + "', '" + ce_name +  "', " + str(occ) +  ", '" + VOCE + "');"
      logger.info('Query is: ' + myquery)
      db.query(myquery)

   elif len(row3) == 1 :

      logger.info("Found a line to be update in ce_stats")
      occ_sum  =  max_of_2_str(row2[0][0],row3[0][0])

      myquery="UPDATE wmsmon.ce_stats SET occ ='" + occ_sum + "' WHERE wms='" + wmshost + "' and lbserver='" + lbhost + "' and ce='" + ce_name + "' and ce_stats.date like '" + DAY_TO_UPDATE + "%' LIMIT 1;"
      logger.info('Query is: ' + myquery)
      db.query(myquery)

   else:

      logger.warning("CE appears more than one with the same wms/lb pair in ce_stats table.")
      logger.warning("This should not happen. Doing nothing, waiting for next iteration to repair the situation")
      logger.warning("CE is: " + ce_name)

   return 0
