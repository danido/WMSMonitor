#!/usr/bin/pyhton

class Node:
   def __init__(self,host,fs_names):
      self.host = host
      self.fs_dict = {}
      self.cpu = None
      for name in fs_names:
         self.fs_dict.setdefault(name)

   def print_node(self):
      string = '\nhost = ' + str(self.host) + '\nfs_dict = ' + str(self.fs_dict) + '\n' 'load = ' + str(self.cpu)
      print string
