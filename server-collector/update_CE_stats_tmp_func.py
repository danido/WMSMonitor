#!/usr/bin/python

def update_CE_stats_tmp(wmshost,lbhost,ENDDATE,deltat,ce_name,ceocc,db):
# Python import
   import os, commands, sys, fpformat
   import MySQLdb,time,datetime
   import logging
   import logpredef
   import query_to_insert_CE_func

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

   logger = logging.getLogger('update_CE_stats_tmp')


   myquery = "select ID_Rec, occ,  deltat from ce_stats_tmp where wms='" + wmshost + "' and lbserver='" + lbhost + "' and ce='" +  ce_name +"' and `date` = '" + ENDDATE + "' LIMIT 1;"

   logger.info('Query is: ' + myquery)
   db.query(myquery)
   r = db.store_result()
   row = r.fetch_row(10000)
   if len(row) > 0 :
      row_to_be_changed = ' occ = ' +  str(row[0][1]) + ' deltat = ' +  str(row[0][2]) + ' ce = ' +  ce_name + ' wms = ' +  wmshost + ' lb = ' +  lbhost + ' ENDDATE = ' +  ENDDATE
      logger.info("Row to be changed = " + row_to_be_changed)

      ceocc_max =  max_of_2_str(ceocc,row[0][1])

      update_query = "UPDATE ce_stats_tmp SET occ = '" + ceocc_max + "' WHERE `date` = '" + ENDDATE + "' AND wms='" + wmshost + "' and lbserver = '" + lbhost + "' and ce = '" + ce_name + "' LIMIT 1;"

      logger.info('Query is: ' + update_query)
      db.query(update_query)

   else:
      logger.warning("I found NO row to be updated!!! Inserting a new one")
      ce = ce_name + '|' + str(ceocc)
      myquery,myquery_tmp = query_to_insert_CE_func.query_to_insert_CE(wmshost,lbhost,ENDDATE,str(deltat),ce,db,True,'Null')
      logger.info('Query is: ' + myquery_tmp)
      db.query(myquery_tmp)

   return 0
