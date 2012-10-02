#!/usr/bin/pyhton

class WMSuser(object):
   def __init__(self):
      WMSuser.dn = None
      WMSuser.VO = None
      WMSuser.group = None
      WMSuser.WMP_in = None
      WMSuser.WMP_in_col = None
      WMSuser.WMP_in_col_avg = None
      WMSuser.WMP_in_col_std = None
      WMSuser.WM_in = None
      WMSuser.WM_in_res = None
      WMSuser.JC_in = None
      WMSuser.JC_out = None
      WMSuser.JOB_DONE = None
      WMSuser.JOB_ABORTED = None

   def print_user(self):
      string = 'dn = ' + str(self.dn) + '\nVO = ' + str(self.VO) + '\ngroup = ' + str(self.group) + '\nWMP_in = ' + str(self.WMP_in) + '\nWMP_in_col = ' + str(self.WMP_in_col) + '\nWMP_in_col_avg = ' + str(self.WMP_in_col_avg) + '\nWM_in = ' + str(self.WM_in) + '\nWM_in_res = ' + str(self.WM_in_res) + '\nJC_in = ' + str(self.JC_in) + '\nJC_out = ' + str(self.JC_out) + '\nJOB_DONE = ' + str(self.JOB_DONE) + '\nJOB_ABORTED = ' + str(self.JOB_ABORTED) + '\n'
      print string
