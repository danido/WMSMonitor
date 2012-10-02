#!/usr/bin/python

import user_class

UserPresent = 'User Already Present'
CEPresent = 'CE Already Present'
CENotPresent = 'CE Not Present'

class wmsdata:
   def __init__(self,hostname):
      self.host = hostname
      self.userlist = []
      self.ce_dict = {}
      self.lb_dict = {}
      self.wmstotal_dict = {}

   def add_user(self,newdn):
      FOUND = False
      for user in self.userlist:
         if user['dn'] == newdn:
            FOUND = True
            raise UserPresent
      if not FOUND:
         newuser = user_class.user()
         newuser['dn'] = newdn
         self.userlist.append(newuser)

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

   def add_lb(self,used_lb):
      if self.lb_dict.has_key(used_lb): self.lb_dict[used_lb] = self.lb_dict[used_lb] + 1
      else: self.lb_dict[used_lb] = 1

   def __getitem__(self,item):
      for user in self.userlist:
         if user['dn'] == item:
            return user
      raise IndexError


   def aggregate_on_user(self):
      if len(self.userlist) > 0:
         self.wmstotal_dict = self.userlist[0].userdata.copy()
         self.wmstotal_dict['dn'] = self.host
         self.wmstotal_dict['VO'] = 'Null'
         self.wmstotal_dict['voms_group'] = 'Null'
      else:
         self.wmstotal_dict = {}
         self.wmstotal_dict['VO'] = 'Null'
         self.wmstotal_dict['voms_group'] = 'Null'
      for i in range(1,len(self.userlist)):
         for key in self.userlist[i].userdata:
            if key != 'dn' and key != 'voms_group' and key != 'role' and key != 'VO':
               if self.userlist[i].userdata[key] != None and self.userlist[i].userdata[key] != 'Null':
                  print key, ':', self.wmstotal_dict[key], ':' , self.userlist[i].userdata[key]
                  if self.wmstotal_dict[key] != None and self.wmstotal_dict[key] != 'Null':
                     self.wmstotal_dict[key] = str( int(self.wmstotal_dict[key]) + int(self.userlist[i].userdata[key]) )
                  else:
                     self.wmstotal_dict[key] = str( int(self.userlist[i].userdata[key]) )


   def __str__(self):
      ret = 'START: USERDATA DICTIONARY\n'
      for user in self.userlist:
         ret = ret + str(user)
      ret = ret + 'END: USERDATA DICTIONARY\n'
      ret = ret + '\nSTART: CE DATA\n'
      for ce in self.ce_dict:
         ret = ret + ce + ' | ' + str(self.ce_dict[ce]) + '\n'
      ret = ret + 'END: CE DATA\n'
      ret = ret + '\nSTART: WMS RATE DATA\n'
      ret = ret + str(self.wmstotal_dict) + '\n'
      ret = ret + 'END: WMS RATE DATA\n'

      ret = ret + '\nSTART: LBSERVER HIST\n'
      for lb in self.lb_dict:
         ret = ret + lb + ' | ' + str(self.lb_dict[lb]) + '\n' 
      ret = ret + 'END: LBSERVER HIST\n\n'

      return ret    
