#!/usr/bin/python
import os

def ice_jobs(ENV_FILE):
   '''Returns a dict about the number of ice jobs in various states (i.e. pending, idle, running, really running, held)  
   state are in a dict so that we can use a loop and adding new state is easier'''

   try :
       version = 0
       cmdcheck = 'queryDb --help |grep -c REALLY-RUNNING'
       stri = os.popen(cmdcheck)
       line = stri.readline()
       stri.close()
       if line.find('1') != -1:
          dict_state = {'PENDING' : 'Null', 'IDLE' : 'Null', 'RUNNING' : 'Null', 'REALLY_RUNNING' : 'Null', 'HELD' : 'Null' }
       elif  line.find('0') != -1:
          dict_state = {'PENDING' : 'Null', 'IDLE' : 'Null', 'RUNNING' : 'Null', 'REALLY-RUNNING' : 'Null', 'HELD' : 'Null' }
          version = 1 
       else: 
           raise 'ERROR: Not able to find ICE queryDb version returning Null for ice jobs'
   except:
        print 'ERROR: Not able to find ICE queryDb version returning Null for ice jobs'
        dict_state = {'PENDING' : 'Null', 'IDLE' : 'Null', 'RUNNING' : 'Null', 'REALLY_RUNNING' : 'Null', 'HELD' : 'Null' }
        dict_state.pop('REALLY_RUNNING')
        return dict_state
   
   for state in dict_state:
        cmd = '/usr/bin/queryDb -s ' + state
        print cmd
        stri = os.popen(cmd)
        line = stri.readline()
        stri.close()
        if line.find('item(s) found') != -1:
             print line
             linesp = line.split()
             dict_state[state] = int(linesp[0])
        
   if version == 0 :
       #Summing running and really running and removing from the disct state the really_running
       if (dict_state['RUNNING'] != 'Null' ) and (dict_state['REALLY_RUNNING'] != 'Null'): 
           dict_state['RUNNING'] = dict_state['RUNNING'] + dict_state['REALLY_RUNNING']
           dict_state.pop('REALLY_RUNNING')
       else:
           dict_state.pop('REALLY_RUNNING')
   else :
       #Summing running and really running and removing from the disct state the really_running
       if (dict_state['RUNNING'] != 'Null' ) and (dict_state['REALLY-RUNNING'] != 'Null'):
           dict_state['RUNNING'] = dict_state['RUNNING'] + dict_state['REALLY-RUNNING']
           dict_state.pop('REALLY-RUNNING')
       else:
           dict_state.pop('REALLY-RUNNING')
   print dict_state
   return dict_state                                                              
