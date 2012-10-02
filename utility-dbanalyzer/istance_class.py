#!/usr/bin/pyhton

import node_class
import time

class Istance(node_class.Node):
   def __init__(self,host,fs_names,daemons_names):
      self.daemons_dict = {}
      self.VO = None
      self.STATUS = None #None= unkn, 0 = ok, 1 = warning, 2 = critical
      self.message = ''
      node_class.Node.__init__(self,host,fs_names)
      for name in daemons_names:
         self.daemons_dict.setdefault(name)
      self.last_update = '0000-00-00 00:00'

   def print_istance(self):
      node_class.Node.print_node(self)
      string = 'last_update = ' + self.last_update + '\ndaemons_dict = ' + str(self.daemons_dict)
      print string
      string = 'VO = ' + str(self.VO) + '\nSTATUS = ' + str(self.STATUS)
      print string

   def make_ist_status(self):
      self.STATUS = None
      self.message = ''
      datetmp = time.strptime(self.last_update,"%Y-%m-%d %H:%M:%S")
      lastd = int(time.mktime(datetmp))
      if time.time() - lastd > 1800:
         print 'OLD UPDATE STATUS UNKNOWN'
         self.STATUS = None
         self.message = 'Data are too old'
         return 0

      for key in self.daemons_dict:
         if self.daemons_dict[key] != '0':
            self.STATUS = 2
            self.message = 'At least daemon ' + key + ' is dead!'
            return 0

      for key in self.fs_dict:
         if self.fs_dict[key] == None : 
            self.fs_dict[key] = 0
         if int(self.fs_dict[key]) > 80 and int(self.fs_dict[key]) < 90 and self.STATUS != 2:
            self.STATUS = 1
            self.message = 'At least fs ' + key + ' occupancy is >80 and <90'
         elif int(self.fs_dict[key]) >= 90:
            self.STATUS = 2
            self.message = 'At least fs ' + key + ' occupancy is >90'
            return 0
      if self.STATUS and self.STATUS != 0:
         return 0
      else:
         self.STATUS = 0

      return 0
