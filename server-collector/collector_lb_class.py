#!/usr/bin/pyhton
import sys
sys.path.append('../../common')
sys.path.append('../../common/classes/')
import lb_class
import time
import logging,logpredef
logger=logging.getLogger('collector_lb_class')


class collectorlb(lb_class.LB):
   "Class used from collector to load LB data from file and store them into database"

   def __init__(self,host):
      lb_class.LB.__init__(self,host)
   
   def load_lbdata_file(self,filedesc):
      try:
         filedesc.seek(0)
         lines = filedesc.readlines()
         for line in lines:
            if line.find('DATA COLLECTION COMPLETED ON:') != -1:
               self.date = line[line.find(':')+1:line.find('=')].strip()
            try:
                if (lines.index('START: LB DATA DICTIONARY\n')+1) != (lines.index('END: LB DATA DICTIONARY\n')):
                   exec('self.data_dict = ' + lines[lines.index('START: LB DATA DICTIONARY\n')+1])
                   for key in self.daemons_dict:
                       self.daemons_dict[key] = self.data_dict[key]
                   for key in self.fs_dict:
                       self.fs_dict[key] = self.data_dict[key]
                   self.connections= self.data_dict['LB_CON']
                   self.cpu = self.data_dict['cpu_load']
                else:
                   logger.info("NO DATA DICTIONARY FOUND FOR LB: " + self.host)
            except Exception,e:
                  logger.error("ERROR LOADING LB DICTIONARY FROM FILE: " + str(e))

      except Exception,e:
          logger.error("ERROR READING DATA FROM FILE: " + str(e))

   def store_lb_to_db(self,db):
      try:
         table = 'lb_sensor'
         dict_tmp = self.data_dict
         dict_tmp['measure_time'] = self.date
         dict_tmp['idhost'] = self.idhost
         keys = tuple(dict_tmp.keys())
         values = tuple(dict_tmp.values())
         querysql = "INSERT into " + table + " "  + str(keys).replace("'","`")
         querysql += " VALUES " + str(values).replace("'Null'","Null") + ";"
         logger.info(querysql)
         db.query(querysql)
         logger.info('LB DATA_STORED')
      except Exception,e:
          logger.error("ERROR STORING DATA TO DATABASE, TABLE "+ table + " : " + str(e))

