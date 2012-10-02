#!/usr/bin/pyhton

class vo_group:
   def __init__(self,stri):
      self.name = stri
      self.vo = stri.split('-')[0]
      if len(stri.split('-')) > 1:
         self.group = stri.split('-')[1]
      else:
         self.group = None
      self.wms_list = []
      self.lb_list = []
      self.wms_obj_list = []
      self.lb_obj_list = []
      self.STATUS = None #it can be None (unknown) , 0 (ok), 1 (warning), 2 (critical)
      self.message = ''

   def print_obj_hosts(self):
      print "WMS PRESENT:"
      for WMSobj in self.wms_obj_list:
         print WMSobj.host, ' ST = ', WMSobj.STATUS
      print "LB PRESENT:"
      for LBobj in self.lb_obj_list:
         print LBobj.host, ' ST = ', LBobj.STATUS

   def print_vo_group(self):
      string = '\nname = ' + str(self.name) + '\nwms_list = ' + str(self.wms_list) + '\nlb_list = ' + str(self.lb_list) + '\nSTATUS = ' + str(self.STATUS)
      print string
      self.print_obj_hosts()

   def make_status(self):
      self.message = ''
      self.STATUS = 0

      n_wms_crit = 0
      #count the critical services
      for WMSobj in self.wms_obj_list:
         if WMSobj.STATUS == 2:
            n_wms_crit = n_wms_crit + 1
            self.message = self.message + "   " + WMSobj.host + " is CRITICAL  -  Message from WMS: " + WMSobj.message

      if n_wms_crit > len(self.wms_obj_list) / 2:
         self.STATUS = 2
      if n_wms_crit > 0 and self.STATUS != 2:
         self.STATUS = 1

      # count the unknown service
      n_wms_unk = 0
      for WMSobj in self.wms_obj_list:
         if WMSobj.STATUS == None:
            n_wms_unk = n_wms_unk + 1

      if n_wms_unk > len(self.wms_obj_list) / 2:
         print "n_wms_unk > 50 %. Group status becomes unknown"
         self.STATUS = None

