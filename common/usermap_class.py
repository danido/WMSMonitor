class usermap(object):
   def __init__(self):
      self.usermapdata = {'dn': None, 'ROLE_GROUP': None, 'VO': None}
      null_str = 'Null'

   def __getitem__(self,item):
      if self.usermapdata.has_key(item):
         return self.usermapdata[item]
      else:
         raise IndexError

   def __setitem__(self,key,item):
      if self.usermapdata.has_key(key):
         if item != None:
            self.usermapdata[key] = str(item)
         else:
            self.usermapdata[key] = null_str
      else:
         raise IndexError

   def __str__(self):
      ret = 'This is the usermapdata dictionary:\n'
      ret = ret + str(self.usermapdata)
      ret = ret + '\nEnd of dictionary\n'
      return ret

