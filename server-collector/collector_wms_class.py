#!/usr/bin/pyhton
import sys
sys.path.append('../../common')
sys.path.append('../../common/classes/')
import wms_class
import user_class
import time
import logging,logpredef
UserPresent = 'User Already Present'
CEPresent = 'CE Already Present'
CENotPresent = 'CE Not Present'

logger=logging.getLogger('collector_wms_class')

class collectorwms(wms_class.WMS):
   "Class used from collector to load WMS data from file and store them into database"

   def __init__(self,host):
      wms_class.WMS.__init__(self,host)

   def load_user(self,filedesc):	 
      try:
          filedesc.seek(0)
          lines = filedesc.readlines()	 
          start = lines.index('START: USERDATA DICTIONARY\n') + 1
          end = lines.index('END: USERDATA DICTIONARY\n')
          if (end-start)>0:
              for line in lines[start:end]:	 
                 linedict=eval(line)	 
                 self.add_user(linedict['dn'])
                 for userkey in linedict.keys():
                     if userkey == 'dn': continue
                     self.userlist[linedict['dn']][userkey] = linedict[userkey]
              logger.info('USER LOADED')
          else: logger.info("NO USER DATA IN FILE")
      except Exception,e:	 
           logger.error("ERROR READING USER DATA FROM FILE: " + str(e))


   def load_ce_data(self,filedesc):
      try:
          filedesc.seek(0)
          lines = filedesc.readlines()
          start = lines.index('START: CE DATA\n')+1
          end = lines.index('END: CE DATA\n')
          if (end-start)>0:
		  for line in lines[start:end]:
# The following lines (realted to the 'cream' CEs) break. I use the 'general' case also for cream CEs. - Enrico 
#		      if line.find('cream')!=-1:
#			 self.add_ce(line.split("|")[0].split('/')[2].strip(':8443'))
#			 self.add_ce_count(line.split("|")[0].split('/')[2].strip(':8443'),line.split("|")[1].strip())
#		      else:
# end - Enrico
			 self.add_ce(line.split("|")[0].strip())
			 self.add_ce_count(line.split("|")[0].strip(),line.split("|")[1].strip())
		  logger.info('CE DATA LOADED')
          else: logger.info("NO CE DATA IN FILE")
      except Exception,e:
           logger.error("ERROR READING CE DATA FROM FILE: " + str(e))

   def load_globus_error_data(self,filedesc):
      try:
          filedesc.seek(0)
          lines = filedesc.readlines()
          start = lines.index('START: GLOBUS ERROR STATS\n')+1
          end = lines.index('END: GLOBUS ERROR STATS\n')
          if (end-start)>0:
		  for line in lines[start:end]:
			 self.add_globus_error(line.split("Globus error ")[1].strip())
			 self.add_globus_error_count(line.split("Globus error ")[1].strip(),line.split("Globus error ")[0].strip())
		  logger.info('GLOBUS ERROR STATS DATA LOADED')
          else: logger.info("NO GLOBUS ERROR STATS IN FILE")
      except Exception,e:
           logger.error("ERROR READING GLOBUS ERROR STATS FROM FILE: " + str(e))

   def load_cream_error_data(self,filedesc):
      try:
          filedesc.seek(0)
          lines = filedesc.readlines()
          start = lines.index('START: CREAM ERROR STATS\n') + 1 
          end = lines.index('END: CREAM ERROR STATS\n')
          if (end-start)>0:
		  for line in lines[start:end]:
			 self.add_cream_error(line.split("|")[1].strip())
			 self.add_cream_error_count(line.split("|")[1].strip(),line.split("|")[0].strip())
		  logger.info('CREAM ERROR STATS DATA LOADED')
          else: logger.info("NO CREAM ERROR STATS IN FILE")
      except Exception,e:
           logger.error("ERROR READING CREAM ERROR STATS FROM FILE: "+ str(e))

   def load_ce_mm_dict(self,filedesc):
      try:
         filedesc.seek(0)
         lines = filedesc.readlines()
         start = lines.index('START: CE_MM HIST\n')+1
         end = lines.index('END: CE_MM HIST\n')
         if (end-start)>0:
            exec('self.ce_mm_dict = ' + lines[start])
            logger.info('CE_MM LOADED')
         else: logger.info("NO CE_MM DATA IN FILE")
      except Exception,e:
          logger.error("ERROR READING CE_MM DATA FROM FILE: "+ str(e))
   
   def load_wmsdata_file(self,filedesc):
      try:
         filedesc.seek(0)
         lines = filedesc.readlines()
         for line in lines:
            if line.find('DATA COLLECTION COMPLETED ON:') != -1:
               self.date = line[line.find(':')+1:line.find('=')].strip()

         line = lines[lines.index('START: WMS DATA DICTIONARY\n')+1]
         for i in range( 3, len(line.split()) + 3 ,3):
             self.data_dict[line.split()[i-3]]=line.split()[i-1]
         if (lines.index('END: WMS DATA DICTIONARY\n')+1):
            logger.info('FILE_READ')
         else:
            logger.error('COULD NOT FIND END OF SECTION FOR WMS DATA')

      except Exception,e:
          logger.error("ERROR READING DATA FROM FILE:  "+ str(e))

   def store_wms_to_db(self,db):
      try:
         table = 'wms_sensor'
         dict_tmp = self.data_dict
         dict_tmp['measure_time'] = self.date
         dict_tmp['idhost'] = self.idhost
         keys = tuple(dict_tmp.keys())
         values = tuple(dict_tmp.values())
         querysql = "INSERT into " + table + " "  + str(keys).replace("'","`")
         querysql += " VALUES " + str(values).replace("'Null'","Null") + ";"
         logger.debug(querysql)
         db.query(querysql)
         logger.info('WMS DATA_STORED')
      except Exception,e:
         logger.error("ERROR STORING DATA TO DATABASE, TABLE "+ table + " : "+ str(e))

   
   def store_jss_error_data_to_db(self,db):
      try:
         #checking for date..
         table='err_stats'
         if self.globuserr_dict :
            day = self.STARTDATE.split()[0]
            querysql = "DELETE FROM " + table + " WHERE day LIKE '%" + day + "%' AND idhost = '" + self.idhost + "';"
            db.query(querysql)
            for key in self.globuserr_dict.keys():
                   dict_tmp = {}
                   dict_tmp['day'] = self.date
                   dict_tmp['idhost'] = self.idhost
                   dict_tmp['error_string'] = key
                   dict_tmp['occurrences'] = self.globuserr_dict[key]
                   dict_tmp['err_type'] = 'globus'
                   keys = tuple(dict_tmp.keys())
                   values = tuple(dict_tmp.values())
                   querysql = "INSERT into " + table + " "  + str(keys).replace("'","`")
                   querysql += " VALUES " + str(values) + ";"
                   logger.debug(querysql)
                   db.query(querysql)
            logger.info('GLOBUS ERR DATA STORED')
      except Exception,e:
         logger.error("ERROR STORING DATA TO DATABASE, TABLE ERR_STATS, GLOBUS ERR: "+str(e))

      try:
         #checking for date..
         if self.creamerr_dict :
            day = self.STARTDATE.split()[0]
            querysql = "DELETE FROM " + table + " WHERE date LIKE '" + day + "%' AND wms = '" + self.idhost + "';"
            db.query(querysql)
            for key in self.creamerr_dict.keys():
                   dict_tmp = {}
                   dict_tmp['day'] = self.date
                   dict_tmp['idhost'] = self.idhost
                   dict_tmp['error_string'] = key
                   dict_tmp['occurrences'] = self.creamerr_dict[key]
                   dict_tmp['err_type'] = 'cream'
                   keys = tuple(dict_tmp.keys())
                   values = tuple(dict_tmp.values())
                   querysql = "INSERT into " + table + " "  + str(keys).replace("'","`")
                   querysql += " VALUES " + str(values) + ";"
                   logger.debug(querysql)
                   db.query(querysql)
            logger.info('CREAM ERR DATA STORED')
      except Exception,e:
         logger.error("ERROR STORING DATA TO DATABASE, TABLE ERR_STATS, CREAM ERR : "+str(e))

   def load_lbhist(self,filedesc):
      try:
         filedesc.seek(0)
         lines = filedesc.readlines()
         for line in lines[lines.index('START: LBSERVER HIST\n')+1:lines.index('END: LBSERVER HIST\n')]:
             self.lbhist_dict[line.split("|")[0].strip()]=line.split("|")[1].strip()
         logger.info('LB STATS DATA LOADED')
      except Exception,e:
         logger.info("ERROR READING LB STATS FROM FILE: "+str(e))

   def store_lbhist_to_db(self,db):
#CORRECTED ON CLIENT SIDE
# self.ENDDATE is wrong. I add 2 hours to it - Enrico
#      end_d = time.strptime(self.ENDDATE,"%Y-%m-%d:%H:%M:%S")
#      unix_end_d = time.mktime(end_d)
#      new_unix_end_d = unix_end_d+7200
#      self.ENDDATE = time.strftime("%Y-%m-%d:%H:%M:%S",time.localtime(new_unix_end_d))
#end - Enrico

      try:
         for key in self.lbhist_dict.keys():
             querysql = "call insertLB_hist('"
             querysql += self.ENDDATE + "','"
             querysql += self.host + "','"
             querysql += key + "','"
             querysql += self.lbhist_dict[key] + "');"
             tt=querysql.replace("'Null'","Null")
             querysql=tt
             logger.debug(querysql)
             db.query(querysql)
         logger.info('LB_HIST stored')

         try:
             for key in self.lbhist_dict.keys():
                querysql = "call insertLB_histDaily('"
                querysql += self.date.split()[0] + "','"
                querysql += key + "','"
                querysql += self.host + "');"
                tt=querysql.replace("'Null'","Null")
                querysql=tt
                logger.debug(querysql)
                db.query(querysql)
             logger.info('LB STATS DATA STORED and daily rate updated')
         except Exception,e:
             logger.error("ERROR UPDATING LB HIST DAILY DATA IN DATABASE: " + str(e))

      except Exception,e:
          logger.error("ERROR STORING LBHIST DATA TO DATABASE: " +str(e))
 
   def load_wmsratedata_file(self,filedesc):
      try:
         filedesc.seek(0)
         lines = filedesc.readlines()
         start = lines.index('START: WMS RATE DATA\n')+1
         end = lines.index('END: WMS RATE DATA\n')
         if (end-start)>0:
            line = eval(lines[start])
            for i in line.keys():
                if line[i] is None:
                    self.wmsrate_dict[i]= 'Null'           
                else:
                    self.wmsrate_dict[i]=line[i]
            logger.info('FILE_READ')
         else:
            logger.warning('NO WMS RATE DATA FOUND')

      except Exception,e:        
         logger.error("ERROR READING WMS RATE DATA FROM FILE: " + str(e))

   def store_wmsratedata_to_db(self,db):
     try:
         table = 'wms_rates'
         dict_tmp = self.wmsrate_dict
         logger.info(str(dict_tmp))
         del dict_tmp['dn'];
         del dict_tmp['voms_group'];
         if dict_tmp.has_key('role'):
            del dict_tmp['role'];
         del dict_tmp['VO'];

#CORRECTED ON CLIENT SIDE
# start_date and end_date are wrong. I add 2 hours to each of them - Enrico
#	 start_d = time.strptime(self.STARTDATE,"%Y-%m-%d:%H:%M:%S")
#	 unix_start_d = time.mktime(start_d)
#	 new_unix_start_d = unix_start_d+7200
#	 dict_tmp['start_date'] = time.strftime("%Y-%m-%d:%H:%M:%S",time.localtime(new_unix_start_d))
#	 end_d = time.strptime(self.ENDDATE,"%Y-%m-%d:%H:%M:%S")
#         unix_end_d = time.mktime(end_d)
#         new_unix_end_d = unix_end_d+7200
#         dict_tmp['end_date'] = time.strftime("%Y-%m-%d:%H:%M:%S",time.localtime(new_unix_end_d))
# end - Enrico

         dict_tmp['start_date'] = self.STARTDATE
	 dict_tmp['end_date'] = self.ENDDATE

         dict_tmp['idhost'] = self.idhost
         keys = tuple(dict_tmp.keys())
         values = tuple(dict_tmp.values())
         querysql = "INSERT into " + table + " "  + str(keys).replace("'","`")
         querysql += " VALUES " + str(values).replace("'Null'","Null") + ";"
         logger.debug(querysql)
         db.query(querysql)

         try:
             day = self.date.split()[0]
             idhost = self.idhost
             querysql = "INSERT into " + table + "_daily (idwmsratesdaily,idhost,day,WMP_in,WMP_in_col,WMP_in_col_nodes,WMP_in_col_min_nodes,WMP_in_col_max_nodes,WM_in,WM_in_res,JC_in,JC_out,JOB_DONE,JOB_ABORTED) VALUES ('','"
             querysql += idhost + "','"
             querysql += day + "',"
             querysql += "(select SUM(WMP_in) from " + table + " where start_date > '" + day + "' and idhost ='" + idhost + "'),"
             querysql += "(select SUM(wmp_in_col) from " + table + " where start_date > '" + day + "' and idhost ='" + idhost + "'),"
             querysql += "(select SUM(wmp_in_col_nodes) from " + table + " where start_date > '" + day + "' and idhost ='" + idhost + "'),"
             querysql += "(select MIN(wmp_in_col_min_nodes) from " + table + " where start_date > '" + day + "' and idhost ='" + idhost + "'),"
             querysql += "(select MAX(wmp_in_col_max_nodes) from " + table + " where start_date > '" + day + "' and idhost ='" + idhost + "'),"
             querysql += "(select SUM(wm_in) from " + table + " where start_date > '" + day + "' and idhost ='" + idhost + "'),"
             querysql += "(select SUM(wm_in_res) from " + table + " where start_date > '" + day + "' and idhost ='" + idhost + "'),"
             querysql += "(select SUM(jc_in) from " + table + " where start_date > '" + day + "' and idhost ='" + idhost + "'),"
             querysql += "(select SUM(jc_out) from " + table + " where start_date > '" + day + "' and idhost ='" + idhost + "'),"
             querysql += "(select SUM(job_done) from " + table + " where start_date > '" + day + "' and idhost ='" + idhost + "'),"
             querysql += "(select SUM(job_aborted) from " + table + " where start_date > '" + day + "' and idhost ='" + idhost + "'))  "
             querysql += " ON DUPLICATE KEY UPDATE "
             querysql += "WMP_in = (select SUM(WMP_in) from " + table + " where start_date > '" + day + "' and idhost ='" + idhost + "'),"
             querysql += "wmp_in_col = (select SUM(wmp_in_col) from " + table + " where start_date > '" + day + "' and idhost ='" + idhost + "'),"
             querysql += "wmp_in_col_nodes = (select SUM(wmp_in_col_nodes) from " + table + " where start_date > '" + day + "' and idhost ='" + idhost + "'),"
             querysql += "wmp_in_col_min_nodes = (select MIN(wmp_in_col_min_nodes) from " + table + " where start_date > '" + day + "' and idhost ='" + idhost + "'),"
             querysql += "wmp_in_col_max_nodes = (select MAX(wmp_in_col_max_nodes) from " + table + " where start_date > '" + day + "' and idhost ='" + idhost + "'),"
             querysql += "wm_in = (select SUM(wm_in) from " + table + " where start_date > '" + day + "' and idhost ='" + idhost + "'),"
             querysql += "wm_in_res = (select SUM(wm_in_res) from " + table + " where start_date > '" + day + "' and idhost ='" + idhost + "'),"
             querysql += "jc_in = (select SUM(jc_in) from " + table + " where start_date > '" + day + "' and idhost ='" + idhost + "'),"
             querysql += "jc_out = (select SUM(jc_out) from " + table + " where start_date > '" + day + "' and idhost ='" + idhost + "'),"
             querysql += "job_done = (select SUM(job_done) from " + table + " where start_date > '" + day + "' and idhost ='" + idhost + "'),"
             querysql += "job_aborted = (select SUM(job_aborted) from " + table + " where start_date > '" + day + "' and idhost ='" + idhost + "'); "
             tt=querysql.replace("'Null'","Null")
             querysql=tt
             logger.debug(querysql)
             db.query(querysql)
             logger.info('WMS RATE DATA STORED and daily rate updated')
         except Exception,e:
             logger.error("ERROR UPDATING WMS DAILY RATE DATA IN DATABASE: " + str(e))

     except Exception,e:
          logger.error("ERROR STORING DATA TO DATABASE, TABLE "+ table + " : " + str(e))

   def store_cemm_to_db(self,db):
      try:
         table = 'ce_mm'
         #checking for date..
         if self.ce_mm_dict :
            day = self.STARTDATE.split()[0]
            querysql = "DELETE FROM " + table + " WHERE day LIKE '" + day + "%' AND idhost = '" + self.idhost + "';"
            logger.info("Deleting ce_mm for today. Query is :" + querysql)
            db.query(querysql)
            for key in self.ce_mm_dict.keys():
                   dict_tmp = {}
                   dict_tmp['day'] = self.date
                   dict_tmp['idhost'] = self.idhost
                   dict_tmp['num_ce'] = key
                   dict_tmp['occurrences'] = self.ce_mm_dict[key]
                  ## dict_tmp['vo'] = self.VO
                   keys = tuple(dict_tmp.keys())
                   values = tuple(dict_tmp.values())
                   querysql = "INSERT into " + table + " "  + str(keys).replace("'","`")
                   querysql += " VALUES " + str(values) + ";"
                   logger.debug(querysql)
                   db.query(querysql)

            logger.info('CE MM DATA_STORED')
      except Exception,e:
         logger.error("ERROR STORING DATA TO DATABASE, TABLE "+ table + " : " + str(e))


   def store_ce_data_to_db(self,db):
      try:
         for key in self.ce_dict.keys():
# The insertCE_Stats procedure insert data with the 'vo' field. This field is deprecated and no more present in the ce_stats table. There is the 'idusermap' field in the table but the sensor is not yet able to retrieve info about the user. We adopt a workaround: we insert the idusermap corresponding to the 'dummy' user of the VO (taken as self.VO from the admin_host_label table). I change the procedure to call; the new one is 'insertCEStatsWithCEHostWithDummyUser' - Enrico
#             querysql = "call insertCE_Stats('"
	     querysql = "call insertCEStatsWithCEHostWithDummyUser('"
# end - Enrico
	     querysql += self.date + "','"
             querysql += key + "','"
             querysql += self.host + "','"
             querysql += self.ce_dict[key] + "','"
             querysql += self.VO + "');"
             tt=querysql.replace("'Null'","Null")
             querysql=tt
             logger.debug(querysql)
             db.query(querysql)
         logger.info('CE_STATS stored')

         try:
             for key in self.ce_dict.keys():
#                querysql = "call insertCE_StatsDaily('"
		querysql = "call insertCEStatsDailyWithCEHostWithDummyUser('"
                querysql += self.date.split()[0] + "','"
                querysql += key + "','"
                querysql += self.host + "','"             
                querysql += self.VO + "');"
                tt=querysql.replace("'Null'","Null")
                querysql=tt
                logger.debug(querysql)
                db.query(querysql)
             logger.info('CE STATS DATA STORED and daily rate updated')
         except Exception,e:
             logger.error("ERROR UPDATING CESTATS DAILY DATA IN DATABASE: " + str(e))

      except Exception,e:
          logger.error("ERROR STORING CESTATS DATA TO DATABASE: " + str(e))

   def store_user_to_db(self,db):
      try:
         table = 'USER_RATES'
         for user in self.userlist:
#CORRECTED ON CLIENT SIDE
# start_date and end_date are wrong. I add 2 hours to each of them - Enrico
#	     start_d = time.strptime(self.STARTDATE,"%Y-%m-%d:%H:%M:%S")
#             unix_start_d = time.mktime(start_d)
#             new_unix_start_d = unix_start_d+7200
#             start_date = time.strftime("%Y-%m-%d:%H:%M:%S",time.localtime(new_unix_start_d))
#             end_d = time.strptime(self.ENDDATE,"%Y-%m-%d:%H:%M:%S")
#             unix_end_d = time.mktime(end_d)
#             new_unix_end_d = unix_end_d+7200
#             end_date = time.strftime("%Y-%m-%d:%H:%M:%S",time.localtime(new_unix_end_d))
#end - Enrico

             querysql = "call insertUserRateWithMap('" 
             querysql += user + "','"
             querysql += self.userlist[user].userdata['VO'] + "','"
             querysql += self.userlist[user].userdata['voms_group'] + "','"
             querysql += self.userlist[user].userdata['role'] + "','"

# start_date and end_date substituted with new values - Enrico
             querysql += self.STARTDATE  + "','"
             querysql += self.ENDDATE  + "','"
#	     querysql += start_date  + "','"
#             querysql += end_date  + "','"
#end - Enrico

             querysql += self.host  + "','"
             querysql += self.userlist[user].userdata['WMP_in'] + "','"
             querysql += self.userlist[user].userdata['WMP_in_col'] + "','"
             querysql += self.userlist[user].userdata['WMP_in_col_nodes'] + "','"
             querysql += self.userlist[user].userdata['WMP_in_col_min_nodes'] + "','"
             querysql += self.userlist[user].userdata['WMP_in_col_max_nodes'] + "','"
             querysql += self.userlist[user].userdata['WM_in'] + "','"
             querysql += self.userlist[user].userdata['WM_in_res'] + "','"
             querysql += self.userlist[user].userdata['JC_in'] + "','"
             querysql += self.userlist[user].userdata['JC_out'] + "','"
             querysql += self.userlist[user].userdata['JOB_DONE'] + "','"
             querysql += self.userlist[user].userdata['JOB_ABORTED'] + "');"
             tt=querysql.replace("'Null'","Null") 
             querysql=tt
             logger.debug(querysql)
             db.query(querysql)
             try:
		querysql = "call insertUserRateDailyWithMap('"
		querysql += self.date.split()[0] + "','"
		querysql += user + "','"
		querysql += self.userlist[user].userdata['VO'] + "','"
		querysql += self.userlist[user].userdata['voms_group'] + "','"
		querysql += self.userlist[user].userdata['role'] + "','"
#		querysql += self.host + "','"
#		querysql += self.userlist[user].userdata['WMP_in'] + "','"
#		querysql += self.userlist[user].userdata['WMP_in_col'] + "','"
#		querysql += self.userlist[user].userdata['WMP_in_col_nodes'] + "','"
#		querysql += self.userlist[user].userdata['WMP_in_col_min_nodes'] + "','"
#		querysql += self.userlist[user].userdata['WMP_in_col_max_nodes'] + "','"
#		querysql += self.userlist[user].userdata['WM_in'] + "','"
#		querysql += self.userlist[user].userdata['WM_in_res'] + "','"
#		querysql += self.userlist[user].userdata['JC_in'] + "','"
#		querysql += self.userlist[user].userdata['JC_out'] + "','"
#		querysql += self.userlist[user].userdata['JOB_DONE'] + "','"
#		querysql += self.userlist[user].userdata['JOB_ABORTED'] + "');"
		querysql += self.host + "');"
		tt=querysql.replace("'Null'","Null")
                querysql=tt
                logger.debug(querysql)
                db.query(querysql)
             except Exception,e:
                logger.error("ERROR UPDATING USER DAILY RATE DATA IN DATABASE: " + str(e))
         logger.info('USER MAP DATA STORED and daily rate updated')

      except Exception,e:
          logger.error("ERROR STORING DATA TO DATABASE, TABLE "+ table + " : " + str(e))


