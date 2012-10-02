#!/usr/bin/pyhton

import istance_class

class LB(istance_class.Istance):
   def __init__(self,host,fs_names,daemons_names):
      self.connections = None
      self.LB = None
      istance_class.Istance.__init__(self,host,fs_names,daemons_names)

   def get_val(self,val):
      if val:
         return val
      else:
         return 0

   def print_lb(self):
      istance_class.Istance.print_istance(self)
      string = 'connections = ' + str(self.connections)
      print string
