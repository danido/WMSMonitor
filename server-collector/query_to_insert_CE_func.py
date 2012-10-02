#!/usr/bin/python

def query_to_insert_CE(wmshost,lbhost,ENDDATE,deltat,ce,db,ONLY_TMP,VOCElist):
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
      
   logger = logging.getLogger('query_to_insert_CE')

   logger.info('ce is : ' + ce)

   cesp = ce.split('|')
   if len(cesp) >=2 :
      ce_name = cesp[0]
      ceocc = cesp[1]
   else:
      logger.warning("No CE returned by cestat or problems with the ce stat file.")
      logger.info("Returning None")
      return None,None


   myquery_tmp = "INSERT INTO `wmsmon`.`ce_stats_tmp` (`ID_Rec`, `date`, `wms`,`lbserver`,`ce`,`occ`,`deltat`) VALUES (NULL,'" + ENDDATE + "', '" + wmshost + "', '" + lbhost + "', '" + ce_name +  "', " + create_null(ceocc) + ", '" + deltat + "');"

   if ONLY_TMP:
      return None,myquery_tmp


   TODAY = ENDDATE[:10]
   myquery = "select ID_Rec, ce, occ from ce_stats where wms='" + wmshost + "' and lbserver='" + lbhost + "' and ce='" + ce_name + "' and `date` like '" + TODAY + "%';"

   logger.info('Query is: ' + myquery)
   db.query(myquery)
   r = db.store_result()
   row = r.fetch_row(10000)

   QUERY = ''

   if len(row) == 0:
      # it's the first time the user is subtinng to this wms/lb pair with this vo and gruoup -> query to insert
      logger.info("It's the first time CE is accessed by this wms/lb pair -> query to insert")

      QUERY = "INSERT INTO `wmsmon`.`ce_stats` (`ID_Rec`, `date`, `wms`,`lbserver`,`ce`,`occ`,`VO`) VALUES (NULL,'" + ENDDATE + "', '" + wmshost + "', '" + lbhost + "', '" + ce_name +  "', " + create_null(ceocc) + ", '" + VOCElist +"' );"

   elif len(row) == 1 :

      logger.info("CE already present in db today (Only once). Let's sum the values")

      occ_sum = SSum(ceocc,row[0][2],'int')

      QUERY = "UPDATE wmsmon.ce_stats SET `date`= '" + ENDDATE + "', occ =" + create_null(occ_sum) + " WHERE ID_Rec=" + row[0][0] + " LIMIT 1;"

   elif len(row) > 1:

      logger.warning("CE present today in db more than once with same wms/lb pair. This is a weird situation.")
      logger.warning("Something went wrong with previous data collection. Please check, len(row) = " + str(len(row)) + ".")
      logger.warning("Summing all data, removing old entries and inserting a new one. User is:" + user.dn)

      occ_sum = ceocc

      for res in row:
         occ_sum = SSum(occ_sum,res[2],'int')

         logger.info("Removing old entries")
         myquery =  "DELETE FROM ce_stats WHERE ID_Rec=" + res[0] + " LIMIT 1;"
         logger.info("Query is :" + myquery)
         db.query(myquery)

      QUERY = "INSERT INTO `wmsmon`.`ce_stats` (`ID_Rec`, `date`, `wms`,`lbserver`,`ce`,`occ`,`VO`) VALUES (NULL,'" + ENDDATE + "', '" + wmshost + "', '" + lbhost + "', '" + ce_name +  "', " + create_null(occ_sum) + ", '" + VOCElist +"' );"
 
   return QUERY, myquery_tmp
