#/usr/bin/python

import os, sys
import os, commands, sys, fpformat
import time,datetime
import readconf_func
import wmsdata_class

def lb_query(rowhost,STARTDATE,ENDDATE):

   #Initializing logger
   import logging
   logger = logging.getLogger('lb_apiquery')

################ INITIALIZATION ######
   confvar = readconf_func.readconf();
   API_CMD_PATH = './'
   wmsdata_list = []
   users_stats = []

#######################################

#################  FUNCTION DEFINITION #########
   def put_into_wmsdata(wmsdata_list,wmshostname,userdn,fieldlist,valuelist):
      wmsFOUND = False
      for wmsdata in wmsdata_list:
         if wmsdata.host == wmshostname:
            wmsFOUND = True
            try:
               wmsdata.add_user(userdn)
            except wmsdata_class.UserPresent:
               pass
            for field in fieldlist:
               wmsdata[userdn][field] = valuelist[fieldlist.index(field)]
      if not wmsFOUND:
         wmsdata = wmsdata_class.wmsdata(wmshostname)
         wmsdata.add_user(userdn)
         for field in fieldlist:
            wmsdata[userdn][field] = valuelist[fieldlist.index(field)]
         wmsdata_list.append(wmsdata)

   def group_by_key(api_output_list,keyposition,CNPROXYFLAG):
      #INPUTS:
      # - api_output_list: the output of api query command execution
      # - keyposition: the position of the key of grouping (ex. user DN or CE queue) in the output_list lines                                    splitted by separator
      # - SET CNPROXYFLAG to TRUE/1 to group DN which differs only by a "/CN=proxy/CN=proxy" SUFFIX
      # OUTPUTS:
      # - dictionary of key and count of occurrences"
      dictionary={}
      l_key=[]
      for l in api_output_list:
         l_key.append(l.split('\t')[keyposition])
      for key in set(l_key):
                 dictionary[key]=l_key.count(key)
      if CNPROXYFLAG:
         #grouping users and proxies 
         for key in dictionary.keys():
            index = key.find('/CN=proxy/CN=proxy')
            if index != -1:
               dn = key[0:index]
               if dictionary.has_key(dn):
                  dictionary[dn]= dictionary[dn] + dictionary.pop(key)
               else:
                  dictionary[dn]= dictionary.pop(key)
      return dictionary

   def resolve_jobuser(jobid):
      #INPUTS:
      # - jobid for which we want to derive user
      # OUTPUTS:
      # - job USER DN
      # N.B. it explouts lbproxy socket if available"

      import os.path
      if os.path.exists('/tmp/lb_proxy_serve.sock'):
         stream= os.popen("./job_status -x /tmp/lb_proxy_serve.sock " + jobid + " |grep owner")
         output=stream.readlines()
         if output:
            return output[0].split(':')[1]
      else:
         return 'Null'

   def checkoutput_to_resolve_jobuser(apiqueryoutput):
      #INPUTS:
      # - output lines from apiquery
      # OUTPUTS:
      # - job USER DN in lines with (null) string where owner!=user
      # N.B. it explouts lbproxy socket if available"

     import os.path
     if os.path.exists('/tmp/lb_proxy_serve.sock'):
     #    usersoutput = []
         logger.debug('entering checkoutput_to_resolve_jobuser function')
         out=apiqueryoutput
         #print "out dentro funzioncina prima" ,out, '\n\n'
         for iji in range(0,len(out)):
            if out[iji].split('\t')[0].find('(null)')!=-1:
               logger.debug('found (null) DN, for jobid:' + out[iji].split('\t')[1])
          #     print 'found (null) DN, for jobid:' + out[iji].split('\t')[1]
               user=resolve_jobuser(out[iji].split('\t')[1])
               logger.debug('substituted with:' + user)
               user=user.strip().strip('\n').lstrip().strip()
           #    print 'substituted with:' + user
               tmp=out[iji].replace('(null)',user,1)
               logger.debug('new line tmp ' +tmp)
            #   print 'new line tmp ' +tmp
               out[iji]=tmp
               logger.debug('new line apioutput ' + out[iji])
             #  print 'new line apioutput ' + out[iji]
#         print "out dentro funzioncina dopo" , out,'\n\n'
         return out
     else:
         logger.warning('NO lb-proxy-socket-file found, unable to determine some jobs OWNER field')
         return apiqueryoutput


############################################
########## STARTING  QUERIES ################

   # Run a MySQL query to find the number of jobs and collections submitted in a given time interval PER USER 
   logger.info('Running a MySQL query to find the number of jobs submitted in a given time interval PER USER')
   stream= os.popen(API_CMD_PATH + "/submitted_jobs " + STARTDATE + " " + ENDDATE)
   output=stream.readlines()
   if output:
      #checkin jobs with null owner
      output=checkoutput_to_resolve_jobuser(output)
      l_single=[]
      l_collection_user=[]
      l_collection_values=[]
      #SEPARATING SINGLE JOBS FROM COLLECTIONS
      for l1 in output:
         if l1.split('\t')[2]=='0':
            l_single.append(l1)
         else:
            l_collection_user.append(l1.split('\t')[0])
            l_collection_values.append(l1.split('\t')[2])            
      dict_tmp=group_by_key(l_single,0,1)     
      #STORING SINGLE JOBS DATA       
      for dn in dict_tmp.keys():
         put_into_wmsdata(wmsdata_list,rowhost,dn,['WMP_in'],[dict_tmp[dn]])          
      
 # def put_into_wmsdata(wmsdata_list,wmshostname,userdn,fieldlist,valuelist):
      #EXTRACTING COLLECTIONS DATA, GROUPING SAME USERS DN & PROXY
      dict_tmp={}
      for user in set(l_collection_user):
         values=[]
         for count in range(0,len(l_collection_user)):
            if l_collection_user[count]==user:
               values.append(int(l_collection_values[count]))
         #GROUPING DN AND PROXY OF SAME USER
         index = user.find('/CN=proxy/CN=proxy')
         if index != -1:
            #CASE with PROXY
            dn = key[0:index]
            if dict_tmp.has_key(dn):
               dict_tmp[dn][0]= dict_tmp[dn][0] + len(values)
               dict_tmp[dn][1]= dict_tmp[dn][1] + sum(values)
               dict_tmp[dn][2]= min(dict_tmp[dn][2], min(values))
               dict_tmp[dn][3]= max(dict_tmp[dn][3], max(values))
            else:
               dict_tmp[dn]= [len(values),sum(values),min(values),max(values)]
         else: 
            #CASE without PROXY : checking whether same user was alredy inserted as proxy 
            if dict_tmp.has_key(user):
               dict_tmp[user][0]= dict_tmp[user][0] + len(values)
               dict_tmp[user][1]= dict_tmp[user][1] + sum(values)
               dict_tmp[user][2]= min(dict_tmp[user][2], min(values))
               dict_tmp[user][3]= max(dict_tmp[user][3], max(values))
            else:
               dict_tmp[user]= [len(values),sum(values),min(values),max(values)]
      #STORING COLLECTIONS DATA

      for dn in dict_tmp.keys():
         put_into_wmsdata(wmsdata_list,rowhost,user,['WMP_in_col','WMP_in_col_nodes','WMP_in_col_min_nodes','WMP_in_col_max_nodes'],[len(values),sum(values),min(values),max(values)])

      #ESPLOITING REGISTER EVENT JOBS TO EXTRACT THE SET OF LB SERVER USED BY CONSIDERED WMS HOST
      dict_tmp={}
      l_key=[]
      #Notice that in LBPROXY CASE JUST 1 WMSHOST is in wmsdata_list. We keep the list as legacy...
      for wmsdata in wmsdata_list:
         for l in output:
             wmsdata.add_lb(l.split('\t')[1].split('/')[2].strip(':9000'))
                
   #  Run a query to find PER USER and PER WMS the number of jobs enqued to WM from WMP in a given time interval
   logger.info("Run a query to find PER USER and PER WMS the number of jobs enqued to WM from WMP in a given time interval")
   stream= os.popen(API_CMD_PATH + "/enqueued_WM_jobs " + STARTDATE + " " + ENDDATE)
   output=stream.readlines()
   if output:
      #checkin jobs with null owner
      output=checkoutput_to_resolve_jobuser(output)
      dict_tmp=group_by_key(output,0,1)
      for dn in dict_tmp.keys():
          put_into_wmsdata(wmsdata_list,rowhost,dn,['WM_in'],[dict_tmp[dn]])

   # Run a MySQL query to find the number both collection and single jobs enqueued to WM in a given time interval from LogMonitor (i.e. Resubmitted)
   logger.info('Run a query to find the number both collection and single jobs enqueued to WM in a given time interval from LogMonitor (i.e. Resubmitted) PER USER and PER WMS')
   stream= os.popen(API_CMD_PATH + "/resubmitted_WM_jobs " + STARTDATE + " " + ENDDATE)
   output=stream.readlines()
   if output:
      #checkin jobs with null owner
      output=checkoutput_to_resolve_jobuser(output)
      dict_tmp=group_by_key(output,0,1)
      for dn in dict_tmp.keys():
         put_into_wmsdata(wmsdata_list,rowhost,dn,['WM_in_res'],[dict_tmp[dn]])

   # Run a MySQL query to find the number single jobs enqueued to Job Controller from WM in a given time interval PER WMS and PER USER
   logger.info('Run a query to find the number single jobs enqueued to Job Controller from WM in a given time interval per USER and PER WMS')
   stream= os.popen(API_CMD_PATH + "/enqueued_JSS_jobs " + STARTDATE + " " + ENDDATE)
   output=stream.readlines()
   if output:
      #checkin jobs with null owner
      output=checkoutput_to_resolve_jobuser(output)
      dict_tmp=group_by_key(output,0,1)
      for dn in dict_tmp.keys():
         put_into_wmsdata(wmsdata_list,rowhost,dn,['JC_in'],[dict_tmp[dn]])


   # Run a MySQL query to find the number single jobs enqueued to Condor from Job Controller in a given time interval PER USER and PER WMS
   logger.info('Run a query to find the number single jobs enqueued to Condor from Job Controller in a given time interval PER USER and PER WMS')
   stream= os.popen(API_CMD_PATH + "/transfer_CONDOR_jobs " + STARTDATE + " " + ENDDATE)
   output=stream.readlines()
   if output:
      #checkin jobs with null owner
      output=checkoutput_to_resolve_jobuser(output)
      dict_tmp=group_by_key(output,0,1)
      for dn in dict_tmp.keys():
          put_into_wmsdata(wmsdata_list,rowhost,dn,['JC_out'],[dict_tmp[dn]])

  # Run a MySQL query to find the number of jobs done in a given time interval PER USER and PER WMS
   logger.info('Run a query to find the number single jobs done successfully in a given time interval PER USER and PER WMS')
   stream= os.popen(API_CMD_PATH + "/done_events " + STARTDATE + " " + ENDDATE)
   output=stream.readlines()
   if output:
      #checkin jobs with null owner
   #   print 'ouput prima',output
      output=checkoutput_to_resolve_jobuser(output)
#      print 'tmpouput ',tmpoutput
#      output=tmpoutput
 #     print 'ouput dopo',output
      dict_tmp=group_by_key(output,0,1)
      for dn in dict_tmp.keys():
          put_into_wmsdata(wmsdata_list,rowhost,dn,['JOB_DONE'],[dict_tmp[dn]])

  # Run a MySQL query to find the number of jobs aborted in a given time interval PER USER and PER WMS
   logger.info('Run a query to find the number single jobs aborted in a given time interval PER USER and PER WMS')
   stream= os.popen(API_CMD_PATH + "/abort_events " + STARTDATE + " " + ENDDATE)
   output=stream.readlines()
   if output:
      #checkin jobs with null owner
      output=checkoutput_to_resolve_jobuser(output)
      dict_tmp=group_by_key(output,0,1)
      for dn in dict_tmp.keys():
          put_into_wmsdata(wmsdata_list,rowhost,dn,['JOB_ABORTED'],[dict_tmp[dn]])

   # Run a query to find the DEST_CE of jobs in a given time interval PER WMS
   logger.info('Run a MySQL query to find  DEST_CE of jobs in a given time interval PER WMS')
   stream= os.popen(API_CMD_PATH + "/CE_histogram " + STARTDATE + " " + ENDDATE)
   output=stream.readlines()
   if output:
      #checkin jobs with null owner
      output=checkoutput_to_resolve_jobuser(output)
      dict_tmp=group_by_key(output,2,0)
      for CE in dict_tmp.keys():
            rowCE      = CE
            rowCEcount = dict_tmp[CE]
            wmsFOUND = False
            for wmsdata in wmsdata_list:
               if wmsdata.host == rowhost:
                  wmsFOUND = True
                  try:
                     wmsdata.add_ce(rowCE)
                     wmsdata.add_ce_count(rowCE,rowCEcount)
                  except wmsdata_class.CEPresent:
                    wmsdata.add_CE_count(rowCEcount)
            if not wmsFOUND:
               wmsdata = wmsdata_class.wmsdata(rowhost)
               wmsdata.add_ce(rowCE)
               wmsdata.add_ce_count(rowCE,rowCEcount)
               wmsdata_list.append(wmsdata)

   return wmsdata_list
