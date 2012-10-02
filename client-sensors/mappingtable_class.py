import os,time

AlreadyPresent = 'User Already Present'
EntryExpired = 'EntryExpired'

class mappingtable(object):

   def __init__(self,exptime):
      self.maplist = []
      self.EXPIRATION_TIME = exptime
      # = {'dn': None, 'group': None, 'VO': None, 'timestamp':None}
      null_str = 'Null'

   def has_dn(self,dn):
      for d1 in self.maplist:
         if d1['dn'] == dn: return True
      return False

   def index(self,user):
      for d1 in self.maplist:
         if d1['dn'] == user['dn']: return self.maplist.index(d1)
         #print 'IN INDEX:::::::', 'd1=\n', d1['dn'], '\ndn=\n', dn, '\nmapidx=\n',self.maplist.index(d1)
      return -1

   def entry_expired(self,d1):
      d1expirytmp = time.strptime(d1['timestamp'],"%Y-%m-%d %H:%M:%S") 
      d1expirytmp_epoch=int(time.mktime(d1expirytmp))
      timenow = time.time()
      if timenow - d1expirytmp_epoch > self.EXPIRATION_TIME :
         return True
      else:
         return False

   def addmap(self,d1):
      if len(d1) < 4:
         raise IndexError
      else:
         if self.has_dn(d1['dn']): 
            raise AlreadyPresent
         else:
            if self.entry_expired(d1):
               raise EntryExpired
            else:
               self.maplist.append(d1)
               return 0

   def load(self,filename):
      d1 = {}
      try:
         fm = open(filename,'r')
      except IOError:
         return 1 
      lines = fm.readlines()
      for line in lines:
         linesp = line.split('||')
         if len(linesp) >= 4:
            d1['dn'] = linesp[0].strip().rstrip()
            d1['VO'] = linesp[1].strip().rstrip()
            d1['voms_group'] = linesp[2].strip().rstrip()
            d1['timestamp'] = linesp[3].strip().rstrip()
            try:
               self.addmap(d1)
            except AlreadyPresent:
               continue
            except EntryExpired:
               continue
            except IndexError:
               continue
      fm.close()
      #print 'INLOAD:',  self.maplist
      return 0

   def __getitem__(self,item):
      for d1 in self.maplist:
         if d1['dn'] == item:
            return d1
      return None

#   def __setitem__(self,key,item):
#      if self.usermapdata.has_key(key):
#         if item != None:
#            self.usermapdata[key] = str(item)
#         else:
#            self.usermapdata[key] = null_str
#      else:
#         raise IndexError

   def __str__(self):
      ret = 'This is the mapping table:\n'
      for d1 in self.maplist:
         for key in d1:
            ret = ret + ' || ' + d1[key]
      ret = ret + '\nEnd of dictionary\n'
      return ret

   def save(self,filename):
      keys = ('dn','VO','voms_group','timestamp')
      try:
         fm = open(filename,'w')
      except IOError:
         return 1
      for d1 in self.maplist:
         line = ''
         for key in keys:
            line = line + d1[key] + ' || '
         line = line + '\n'
         fm.write(line)
      fm.close()
      return 0

   def mapuser(self,user):
      idx = self.index(user)
      #print 'USERRRRRRRRRRRR = \n', user['dn'], '\n idx ====', idx
      #print  self.maplist
      if idx != -1:
         user['VO'] = self.maplist[idx]['VO']
         user['voms_group'] = self.maplist[idx]['voms_group']
         return 0
      else:
         return 1

   def get_map_from_file(self,filename,max_rotated,cmd,user):
      newcmd = cmd.replace('USER_DN','"' + user['dn'] + '"')
      for i in range(0,int(max_rotated) + 1 ):
         if i == 0 :
            fname = filename
         else:
            fname = filename + '.' + str(i) 
         newcmd = newcmd.replace('LOG_FILE',fname)

         #print 'NEWCOMMAND ===========', newcmd
         if  (os.access(fname,os.F_OK) == True):
            stream = os.popen(newcmd)
            lines = stream.readlines()
            if ( len(lines) > 0 ):
               istr = lines[0]
               for l in istr.split(' '):
                  #print 'llllllllllllllllllll ======================== ' , l
                  if l.find('Role') != -1:
                     VO = l.split('/')[1]
                     VO_SUB = l[(l.find(VO)+len(VO)):-1]
#                           CAPABILITY = l.split('/')[3].split('=')[1]
#                           print 'USER: ' + user.rstrip() + '\nVO = ' + VO + '\nRole = ' + ROLE + '\nCapability = ' + CAPABILITY 
#                           print line.rstrip(),' ',user.rstrip(), ' ', VO , ' ', VO_SUB
                     timestamp = time.strftime("%Y-%m-%d %H:%M:%S",time.localtime(time.time()))
                     dnew = {'dn': user['dn'],'VO' : VO, 'voms_group' : VO_SUB, 'timestamp' : timestamp }
                     #print 'dnew = ', dnew
                     try:
                        self.addmap(dnew)
                        return 0
                     except:
                        continue
      return 1
