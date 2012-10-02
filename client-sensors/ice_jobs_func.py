#!/usr/bin/python


# Returna dict about the number of ice jobs in various states (i.e. pending, idle, running, really running, held)
# state are in a dict so that we can use a loop and adding new state is easier


import os

def ice_jobs(ENV_FILE):
   '''Returns a dict about the number of ice jobs in various states (i.e. pending, idle, running, really running, held)  
   state are in a dict so that we can use a loop and adding new state is easier'''

   dict_state = {'PENDING' : 'Null', 'IDLE' : 'Null', 'RUNNING' : 'Null', 'REALLY_RUNNING' : 'Null', 'HELD' : 'Null'}

   stri = os.popen(". " + ENV_FILE + "; echo $GLITE_LOCATION")
   GLITE_LOCATION = stri.readline()
   stri.close()

   for state in dict_state:

      cmd = GLITE_LOCATION.strip() + '/bin/queryDb -s ' + state
      stri = os.popen(cmd)
      line = stri.readline()
      stri.close()
      if line.find('item(s) found') != -1:
         linesp = line.split()
         dict_state[state] = int(linesp[0])

   #Summing running and really running and removing from the disct state the really_running
   dict_state['RUNNING'] = dict_state['RUNNING'] + dict_state['REALLY_RUNNING']
   dict_state.pop('REALLY_RUNNING')
   
   #returnign the dictionary

   return dict_state
