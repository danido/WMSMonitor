#!/usr/bin/pyhton
import istance_class
null_str = 'Null'

class LB(istance_class.Istance):
   def __init__(self,host):
      self.connections = None
      self.LB = None
      istance_class.Istance.__init__(self,host,['disk_varlibmysql','disk_lb'],['daemon_LB','daemon_LL','daemon_NTPD'])
      for key in self.daemons_dict:
         self.daemons_dict.setdefault(key,null_str)
      for key in self.fs_dict:
         self.fs_dict.setdefault(key,null_str)

   def get_val(self,val):
      if val:
         return val
      else:
         return 0

   def print_lb(self):
      istance_class.Istance.print_istance(self)
      string = 'connections = ' + str(self.connections)
      print string

