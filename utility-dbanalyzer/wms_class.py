#!/usr/bin/pyhton

import istance_class

class WMS(istance_class.Istance):
   def __init__(self,host,fs_names,daemons_names,queue_names):
      self.queue_dict = {}
      self.fdrain= None
      self.ftraversaltime = None
      self.fload = None
      self.metric = None
      self.LB = None
      self.LBobj = None
      istance_class.Istance.__init__(self,host,fs_names,daemons_names)
      for name in queue_names:
         self.queue_dict.setdefault(name)

   def get_val(self,val):
      if val:
         return val
      else:
         return 0

   def print_wms(self):
      istance_class.Istance.print_istance(self)
      string = 'queue_dict = ' + str(self.queue_dict)
      print string
      string = 'fdrain = ' + str(self.fdrain) + '\nftraversaltime = ' + str(self.ftraversaltime) + '\nfload = ' + str(self.fload)
      print string
      string = 'metric = ' + str(self.metric)
      print string
      print 'LB = ', str(self.LB)
      print 'LBhost = ', str(self.LBobj.host)

   def make_wms_status(self):
      self.STATUS = None
      input_lower = 1000
      input_higher = 3000
      queue_lower = 1000
      queue_higher = 3000
      dg_lower = 1000
      dg_higher = 3000
      #calculating status based on daemons and fs (from istance_class)
      self.make_ist_status()
      #calculating lb_status (from istance_class)
      if self.LBobj != None:
         self.LBobj.make_ist_status()
 
      # calculation of status from queues
      aho = self.queue_dict['input_fl']
      input_val = int(self.get_val(aho))
      if self.STATUS != 2:
         if input_val > input_lower and input_val < input_higher:
            self.STATUS = 1
            self.message = self.message + '  Because at least input_fl  is gt ' + str(input_lower) + ' and lt ' + str(input_higher)
         elif input_val >= input_higher:
            self.STATUS = 2
            self.message = self.message + '  Because input_fl is gt ' + str(input_higher)
      queue_val = int(self.get_val(self.queue_dict['queue_fl']))
      if self.STATUS != 2:
         if queue_val > queue_lower and queue_val < queue_higher:
            self.STATUS = 1
            self.message = self.message + '  At least queue_fl  is gt ' + str(queue_lower) + ' and lt ' + str(queue_higher)
         elif queue_val >= queue_higher:
            self.STATUS = 2
            self.message = self.message + '  Because queue_fl is gt ' + str(queue_higher)
      dg20_val = int(self.get_val(self.queue_dict['dg20']))
      if self.STATUS != 2:
         if dg20_val > dg_lower and dg20_val < dg_higher:
            self.STATUS = 1
            self.message = self.message + '  At least dg20 value  is gt ' + str(dg_lower) + ' and lt ' + str(dg_higher)
         elif dg20_val >= dg_higher:
            self.STATUS = 2
            self.message = self.message + '  Because dg20 is gt ' + str(dg_higher)

      #calculating status combining the LB status
      if self.STATUS and self.LBobj.STATUS:
         self.STATUS = max(self.STATUS,self.LBobj.STATUS)

      if self.STATUS == None and self.LBobj.STATUS != 2:
         self.STATUS = None
         self.message = self.message + '  It was not possible to determine WMS status and LB status is not CRITICAL'
      if self.STATUS == None and self.LBobj.STATUS == 2:
         self.STATUS = 2
         self.message = self.message + '  It was not possible to determine WMS status but LB status is CRITICAL'

      if self.STATUS != 2 and self.LBobj.STATUS == None:
         self.STATUS = None
         self.message = self.message + '  Because it was not possible to determine LB status and WMS status is not CRITICAL'

      if self.STATUS == 2 and self.LBobj.STATUS == None:
         self.STATUS = 2
         self.message = self.message + '  Because it was not possible to determine LB status but WMS status is CRITICAL'
      return 0
