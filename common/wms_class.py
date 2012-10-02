#!/usr/bin/pyhton
import istance_class
import user_class
import time
UserPresent = 'User Already Present'
CEPresent = 'CE Already Present'
CENotPresent = 'CE Not Present'
null_str = 'Null'

class WMS(istance_class.Istance):
   def __init__(self,host):
      self.data_dict = {'wm_queue':null_str,'jc_queue':null_str,'lb_event':null_str,'loadb_fdrain':null_str,'loadb_ftraversaltime':null_str,'loadb_fload':null_str,'loadb_fmetric':null_str,'condor_running':null_str,'condor_idle':null_str,'condor_current':null_str,'ism_size':null_str,'ism_entries':null_str,'gftp_con':null_str,'FD_WM':null_str,'FD_LM':null_str,'FD_JC':null_str,'FD_LL':null_str,'loadb_memusage':null_str,'ice_running':null_str,'ice_idle':null_str,'ice_pending':null_str,'ice_held':null_str,'ice_queue':null_str,'cpu_load':null_str}

      istance_class.Istance.__init__(self,host,['disk_varlibmysql','disk_tmp','disk_varlog','disk_sandbox'],['daemon_LL','daemon_LBPX','daemon_PX','daemon_FTPD','daemon_JC','daemon_LM','daemon_WM','daemon_WMP','daemon_ICE','daemon_BDII','daemon_NTPD'])

      for key in self.daemons_dict:
         self.data_dict.setdefault(key,null_str)
      for key in self.fs_dict:
         self.data_dict.setdefault(key,null_str)

      self.userlist = {}
      self.ce_mm_dict = {}
      self.ce_dict = {}
      self.wmstotal_dict = {}
      self.globuserr_dict = {}
      self.creamerr_dict = {}
      self.lbhist_dict = {}
      self.wmsrate_dict = {'dn': null_str, 'JC_out': null_str, 'WMP_in_col_nodes': null_str, 'voms_group': null_str, 'WM_in_res': null_str, 'WMP_in_col_min_nodes': null_str, 'VO': null_str, 'WMP_in_col_max_nodes': null_str, 'JC_in': null_str, 'JOB_DONE': null_str, 'WMP_in_col': null_str, 'WMP_in': null_str, 'JOB_ABORTED': null_str, 'WM_in': null_str}

   def add_user(self,newdn):
      FOUND = False
      for user in self.userlist.keys():
         if user == newdn:
            FOUND = True
            raise UserPresent
      if not FOUND:
         newuser = user_class.user()
         newuser['dn'] = newdn
         self.userlist[newdn] = newuser


   def add_ce(self,cehost):
      if self.ce_dict.has_key(cehost):
         raise CEPresent
      else:
         self.ce_dict.setdefault(cehost,None)

   def add_ce_count(self,cehost,cecount):
      if not self.ce_dict.has_key(cehost):
         raise CENotPresent
      else:
         self.ce_dict[cehost] = cecount

   def aggregate_on_user(self):
      if len(self.userlist) > 0:
         self.wmstotal_dict = self.userlist[0].userdata.copy()
         self.wmstotal_dict['dn'] = self.host
      else:
         self.wmstotal_dict = {}
      for i in range(1,len(self.userlist)):
         for key in self.userlist[i].userdata:
            if key != 'dn' and key != 'voms_group' and key != 'role' and key != 'VO':
               if self.userlist[i].userdata[key] != None and self.userlist[i].userdata[key] != 'Null':
                  print key, ':', self.wmstotal_dict[key], ':' , self.userlist[i].userdata[key]
                  if self.wmstotal_dict[key] != None and self.wmstotal_dict[key] != 'Null':
                     self.wmstotal_dict[key] = str( int(self.wmstotal_dict[key]) + int(self.userlist[i].userdata[key]) )
                  else:
                     self.wmstotal_dict[key] = str( int(self.userlist[i].userdata[key]) )
   
   def add_globus_error(self,globuserr):
      if self.globuserr_dict.has_key(globuserr):
         print globuserr
         raise 'add_globus_error: GLOBUS ERROR Present'
      else:
         try:
             self.globuserr_dict.setdefault(globuserr,None)
         except Exception,e:
             print "ERROR ADDING GLOBUSERR TO GLOBUSERR_DICT: %s "%e
 

   def add_globus_error_count(self,globuserr,globuserrcount):
      if not self.globuserr_dict.has_key(globuserr):
         raise 'add_globus_error_count: GLOBUSERRNotPresent'
      else:
         try:
             self.globuserr_dict[globuserr] = globuserrcount
         except Exception,e:
             print "ERROR ADDING GLOBUSERR COUNT TO GLOBUSERR_DICT: %s "%e


   def add_cream_error(self,creamerr):
      if self.creamerr_dict.has_key(creamerr):
         print creamerr
         raise 'add_cream_error: CREAM ERROR Present'
      else:
         try:
             self.creamerr_dict.setdefault(creamerr,None)
         except Exception,e:
             print "ERROR ADDING CREAMERR TO CREAMERR_DICT: %s "%e


   def add_cream_error_count(self,creamerr,creamerrcount):
      if not self.creamerr_dict.has_key(creamerr):
         raise 'add_cream_error_count: CREAMERRNotPresent'
      else:
         try:
             self.creamerr_dict[creamerr] = creamerrcount
         except Exception,e:
             print "ERROR ADDING CREAMERR COUNT TO CREAMERR_DICT: %s "%e

   def get_val(self,val):  # used internally in make_status, if removed make_status - remove also this one
      if val:
         return val
      else:
         return 0 

   def __getitem__(self,item):
      if self.data_dict.has_key(item):
         return self.data_dict[item]
      else:
         raise IndexError

   def __setitem__(self,key,item):
      if self.data_dict.has_key(key):
         if item != None:
            self.data_dict[key] = str(item)
         else:
            self.data_dict[key] = null_str
      else:
         raise IndexError

   def __str__(self):
      ret = 'This is the wms object for host ' + self.host + ' , VO :' + str(self.VO) + '\n'
      ret = 'This is the wms data dictionary :\n'
      ret = ret + str(self.data_dict)
      ret = ret + '\n'
      ret = ret + 'This is the userlist dictionary\n'
      ii=[str(self.userlist[user]) for user in self.userlist]
      for i in ii:
         ret = ret + i
      ret = ret + '\n'
      ret = ret + 'This is the ce_mm dictionary\n'
      ret = ret + str(self.ce_mm_dict)
      ret = ret + '\n'
      ret = ret + 'This is the ce_dict dictionary\n'
      ret = ret + str(self.ce_dict)
      ret = ret + '\n'
      ret = ret + 'This is the wmstotal_dict dictionary\n'
      ret = ret + str(self.wmstotal_dict)
      ret = ret + '\n'
      ret = ret + 'This is the globuserr_dict dictionary\n'
      ret = ret + str(self.globuserr_dict)
      ret = ret + '\n'
      ret = ret + 'This is the wmsrate_dict dictionary\n'
      ret = ret + str(self.wmsrate_dict)
      ret = ret + '\n\n End of wms class data\n'
      return ret
   
   def make_lines(self):
      lines = '\nSTART: WMS DATA DICTIONARY\n'
      for key in self.data_dict:
         lines = lines + key + ' = ' + self.data_dict[key] + ' '
      lines = lines + '\nEND: WMS DATA DICTIONARY\n'
      return lines

   def write_to_file(self,filedesc):
      try:
         lines = self.make_lines()
         filedesc.write(lines)
         return 'FILE_WROTE'
      except IOError:
         return 'IOError'


