#!/usr/bin/pyhton
null_str = 'Null'
class user(object):
   def __init__(self):
      self.userdata = {'dn': None, 'JC_out': None, 'WMP_in_col_nodes': None, 'voms_group': None, 'role': None, 'WM_in_res': None, 'WMP_in_col_min_nodes': None, 'VO': None, 'WMP_in_col_max_nodes': None, 'JC_in': None, 'JOB_DONE': None, 'WMP_in_col': None, 'WMP_in': None, 'JOB_ABORTED': None, 'WM_in': None}
      null_str = 'Null'

   def __getitem__(self,item):
      if self.userdata.has_key(item):
         return self.userdata[item]
      else:
         raise IndexError

   def __setitem__(self,key,item):
      if self.userdata.has_key(key):
         if item != None:
            self.userdata[key] = str(item)
         else:
            self.userdata[key] = null_str
      else:
         raise IndexError

   def __str__(self):
      #ret = 'This is the userdata dictionary:\n'
      ret = str(self.userdata) + '\n'
      #ret = ret + '\nEnd of dictionary\n'
      return ret
