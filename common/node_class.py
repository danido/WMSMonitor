#!/usr/bin/pyhton

class Node:
   def __init__(self,host,fs_names):
      self.host = host
      self.date = ''
      self.fs_dict = {}
      self.cpu = None
      for name in fs_names:
         self.fs_dict.setdefault(name)

   def print_node(self):
      string = '\nhost = ' + str(self.host) + '\nfs_dict = ' + str(self.fs_dict) + '\n' 'load = ' + str(self.cpu)
      print string

   def __str__(self):
      ret = '\nThis is the wms file system dictionary for host ' + self.host + ':\n'
      ret = ret + str(self.fs_dict)
      ret = ret + '\nEnd of dictionary\n'
      return ret

