#! /usr/bin/python
import time,sys,os
if len(sys.argv) < 3:
   print "\nUsage:\n"
   print "globus_error_detector.py NDAYAGO SENSORFLAG\n"
   print "Ex. globus_error_detector.py 0 [-1] 0\n"
   print "..will detect today's [yesterday's] errors and produce normal data report for administrators\n"
   print "Ex. globus_error_detector.py 0 [-1] 1\n"
   print "..will detect today's [yesterday's] errors and produce data just for WMSMonitor server\n"

   sys.exit(1)
timestart=time.time()
#calculating date
nday=int(sys.argv[1])
if nday > 0:
   print "\nUsage:\n"
   print "globus_error_detector.py NDAYAGO\n"
   print "ERROR: NDAYAGO must be <=0 "
   sys.exit(1)

SENSORFLAG=int(sys.argv[2])
if ((SENSORFLAG != 0) and (SENSORFLAG != 1)):
   print "\nUsage:\n"
   print "globus_error_detector.py NDAYAGO SENSORFLAG\n"
   print "ERROR: SENSORFLAG must be either 0 or 1 "
   sys.exit(1)

import readconf_func
confvar=readconf_func.readconf();

if SENSORFLAG:

        #JUST PRODUCING DATA FOR WMSMonitor SENSOR
        data = "\"" + time.strftime("%d %b",time.localtime(time.time()+nday*84600)) + "\""
#        datafile=time.strftime("%d%b",time.localtime(time.time()+nday*84600))
        datacalc=time.localtime(time.time()+nday*84600)[1:3]
        print "Globus error detector starts on date: " + data + "\""
#        confvar={'GLITE_LOG_DIR':'/var/log/glite','SITE_CONTACT': 'danilo.dongiovanni@cnaf.infn.it,daniele.cesini@cnaf.infn.it,marco.cecchi@cnaf.infn.it'}

        logfile = '' 
        if ((os.access(confvar.get('GLITE_LOG_DIR') + '/logmonitor_events.log',os.F_OK) == True ) and
            (os.access(confvar.get('GLITE_LOG_DIR') + '/logmonitor_events.log.1',os.F_OK) == False)):
           logfile = confvar.get('GLITE_LOG_DIR') + '/logmonitor_events.log'

        elif  (os.access(confvar.get('GLITE_LOG_DIR') + '/logmonitor_events.log',os.F_OK) == True):
           lines = os.popen("tail -2 /var/log/glite/logmonitor_events.log.*|grep -v 'file rotation'|grep -v '==>'").readlines()
           dateslogmaj = []
           dateslogmin = []
           for line in lines:
               if line == '\n':
                  continue
               else:
                  dateslogmaj.append( datacalc > time.strptime(line.strip().split(',')[0],"%d %b")[1:3] )
                  dateslogmin.append( datacalc < time.strptime(line.strip().split(',')[0],"%d %b")[1:3] )
           if len(lines): 
              try:
                  dateslogmaj.index(True) 
              except:
                  print 'ERROR: Date too far in the past'
                  sys.exit(-1)
             
              if dateslogmaj.index(True) == 0 :
                 logfile = confvar.get('GLITE_LOG_DIR') + '/logmonitor_events.log'
              elif dateslogmaj.index(True)==dateslogmin.index(False):
                 logfile = confvar.get('GLITE_LOG_DIR') + '/logmonitor_events.log.' + str(dateslogmaj.index(True))
              else:
                 if dateslogmin.index(False) == 0:
                     logfile = logfile + confvar.get('GLITE_LOG_DIR') + '/logmonitor_events.log'
                 for l in range(max(dateslogmin.index(False)-1,0),dateslogmaj.index(True)):
                     logfile = logfile + ' ' + confvar.get('GLITE_LOG_DIR') + '/logmonitor_events.log.' + str(l+1)
           else:
              print "ERROR:Could not find logmonitor log files\n"
              sys.exit(-1)

        else:
           print "ERROR: Could not find logmonitor log files\n"
           sys.exit(-1)

        #Reducing log file to use
        cmdreducelog = "grep " + data + " " + logfile + "> " + confvar.get('INSTALL_PATH') + "/sensors/tmp/logmonitor.logtmp"
        if (os.system(cmdreducelog) == 0):
           print "reducing file to operate search on: " + cmdreducelog
        else:
           print "Error while reducing logmonitorfile"
           sys.exit(-1)
        if ( os.access(confvar.get('INSTALL_PATH') + "/sensors/tmp/logmonitor.logtmp",os.F_OK) == True ):
           logfile =  confvar.get('INSTALL_PATH') + "/sensors/tmp/logmonitor.logtmp"

        #Extracting JOBIDS of failing jobs
        cmd_jobid_extract = "grep -A 2 'Globus error' "  + logfile + " | grep 'Job id'|awk '{print $9}' | sort | uniq > " + confvar.get('INSTALL_PATH') + "/sensors/tmp/broken_jobids_uniq.txt"
        print "Extracting jobid with cmd: ", cmd_jobid_extract
        if (os.system(cmd_jobid_extract) == 0):
           print 'jobids of failing jobs stored in file: ' + confvar.get('INSTALL_PATH') + "/sensors/tmp/broken_jobids_uniq.txt"

        else:
           print "Error while extracting jobids of failing jobs"
           sys.exit(-1)

        #Extracting global stats
        cmd_stats_extract = "for a in `cat " + confvar.get('INSTALL_PATH') + "/sensors/tmp/broken_jobids_uniq.txt`; do grep -B 3 $a " + logfile + " |grep -m 1 'Globus error' |awk '{ print substr($0, index($0,$8))}' ;done |sort|uniq -c |sort -gr > " + confvar.get('INSTALL_PATH') + "/sensors/tmp/globus_error_stats"
        print "Extracting globus statistics with cmd: " + cmd_stats_extract
        if (os.system(cmd_stats_extract) == 0):
           print 'Globus error messages stats of failing jobs stored in file: ' + confvar.get('INSTALL_PATH') + "/sensors/tmp/globus_error_stats"
        else:
           print "Error while extracting Globus error messages stats of failing jobs"
           sys.exit(-1)

else :
        #PRODUCING DATA IN LOCAL FILE AND MAIL FOR ADMINISTRATORS
	data = "\"" + time.strftime("%d %b",time.localtime(time.time()+nday*84600)) + "\""
	datafile=time.strftime("%d%b",time.localtime(time.time()+nday*84600))
	datacalc=time.localtime(time.time()+nday*84600)[1:3]
	print "Globus error detector starts on date: " + data + "\""

	#deciding whether to use rotated log or not
#	confvar={'GLITE_LOG_DIR':'/var/log/glite','SITE_CONTACT': 'danilo.dongiovanni@cnaf.infn.it,daniele.cesini@cnaf.infn.it,marco.cecchi@cnaf.infn.it'}
	logfile = ''
	if ((os.access(confvar.get('GLITE_LOG_DIR') + '/logmonitor_events.log',os.F_OK) == True ) and 
	    (os.access(confvar.get('GLITE_LOG_DIR') + '/logmonitor_events.log.1',os.F_OK) == False)):
	   logfile = confvar.get('GLITE_LOG_DIR') + '/logmonitor_events.log'

	elif  (os.access(confvar.get('GLITE_LOG_DIR') + '/logmonitor_events.log',os.F_OK) == True):
	   lines = os.popen("tail -2 /var/log/glite/logmonitor_events.log.*|grep -v 'file rotation'|grep -v '==>'").readlines()
	   dateslogmaj = []
	   dateslogmin = []
	   for line in lines:
	       if line == '\n':
		  continue
	       else:
		  dateslogmaj.append( datacalc > time.strptime(line.strip().split(',')[0],"%d %b")[1:3] )
		  dateslogmin.append( datacalc < time.strptime(line.strip().split(',')[0],"%d %b")[1:3] )
	   if len(lines):
	      try:
		  dateslogmaj.index(True)
	      except:
		  print 'ERROR: Date too far in the past'
		  sys.exit(-1)
	     
	      if dateslogmaj.index(True) == 0 :
		 logfile = confvar.get('GLITE_LOG_DIR') + '/logmonitor_events.log'
	      elif dateslogmaj.index(True)==dateslogmin.index(False):
		 logfile = confvar.get('GLITE_LOG_DIR') + '/logmonitor_events.log.' + str(dateslogmaj.index(True))
	      else:
		 if dateslogmin.index(False) == 0:
		     logfile = logfile + confvar.get('GLITE_LOG_DIR') + '/logmonitor_events.log'
		 for l in range(max(dateslogmin.index(False)-1,0),dateslogmaj.index(True)):
		     logfile = logfile + ' ' + confvar.get('GLITE_LOG_DIR') + '/logmonitor_events.log.' + str(l+1)
	   else:
	      print "ERROR:Could not find logmonitor log files\n"
	      sys.exit(-1)
		    
	else:
	   print "ERROR: Could not find logmonitor log files\n"
	   sys.exit(-1)

	 
	#Reducing log file to use
	cmdreducelog = "grep " + data + " " + logfile + ">/tmp/logmonitor" + datafile + ".logtmp" 
	if (os.system(cmdreducelog) == 0):
	   print "reducing file to operate search on: " + cmdreducelog
	else:
	   print "Error while reducing logmonitorfile"
	   sys.exit(-1)
	if ( os.access("/tmp/logmonitor" + datafile + ".logtmp",os.F_OK) == True ):
	   logfile = "/tmp/logmonitor" + datafile + ".logtmp"


	#Extracting JOBIDS of failing jobs
	cmd_jobid_extract = "grep -A 2 'Globus error' "  + logfile + " | grep 'Job id'|awk '{print $9}' | sort | uniq > /tmp/broken_jobids_" + datafile + "_uniq.txt"
	print "Extracting jobid with cmd: ", cmd_jobid_extract
	if (os.system(cmd_jobid_extract) == 0):
	   print 'jobids of failing jobs stored in file: ' + '/tmp/broken_jobids_' + datafile + '_uniq.txt'
	   
	else:
	   print "Error while extracting jobids of failing jobs"
	   sys.exit(-1)

	#Extracting global stats
	cmd_stats_extract = "for a in `cat /tmp/broken_jobids_" + datafile + "_uniq.txt`; do echo \"$a  $(grep -B 3 $a " + logfile + " |grep -m 1 'Globus error' |awk '{ print substr($0, index($0,$8))}')  $(grep -B 3 $a " + logfile + "|grep -A 1 executing |grep -v -m 1 'Got job executing event' |awk '{print $12}') \" >>/tmp/globus_error_summaryfile_" + datafile + ";done"
	print "Extracting globus statistics with cmd: " + cmd_stats_extract
	if (os.system(cmd_stats_extract) == 0):
	   print 'Globus error messages stats of failing jobs stored in file: ' + '/tmp/globus_error_summaryfile_' + datafile 
	else:
	   print "Error while extracting Globus error messages stats of failing jobs"
	   sys.exit(-1)


	#Extracting Globus error messages stats of failing jobs   
	cmd_hist_error_messages_extract = " cat /tmp/globus_error_summaryfile_" + datafile + "|sed -e " + " \'s/\\\"/$/\'" +  " -e " + " \'s/\\\"./$/\' " + " -e " +  "\'s/^[^$]*$\\(.*\\)\\$.*/\\1/\' " + "|sort|uniq -c |sort -gr"
	print "Extracting globus error histogram with cmd:",cmd_hist_error_messages_extract
	stream = os.popen(cmd_hist_error_messages_extract)
	if (stream):
	   histerr= stream.readlines()
	else:
	   print "Error while calculating histogram of Globus error messages of failing jobs"
	   sys.exit(-1)


	#Extracting CE Stats of failing jobs
	cmd_destination_ce_extract = " cat /tmp/globus_error_summaryfile_" + datafile + " |awk '{print $NF}'|grep -v '\".'|sort|uniq -c |sort -gr"
	print "Extracting CE with cmd: ",cmd_destination_ce_extract
	stream = os.popen(cmd_destination_ce_extract)
	if (stream):
	   histce= stream.readlines()
	else:
	   print "Error while extracting CE destination of failing jobs"
	   sys.exit(-1)

	#Extracting summary file of jobid, globus error and CE involved
	print "Extracting summary stats"
	summaryfilename= '/var/log/globus_error_summaryfile_' + datafile
	summaryfile = open(summaryfilename,'w')
	stream = os.popen('cat /tmp/globus_error_summaryfile_' + datafile + '|wc -l')
	if (stream):
	   totalfail=stream.readlines()
	summaryfile.write("\nTOTAL FAILURES DETECTED: " + totalfail[0].strip() + "\n")
	summaryfile.write("\nHISTOGRAM OF GLOBUS ERROR MESSAGES:\n")
	for line in histerr:
	    summaryfile.write(line)
	summaryfile.write("\n\nHISTOGRAM OF DESTINATION CE:\n")
	for line in histce:
	    summaryfile.write(line)
	summaryfile.write("\n\n")
	summaryfile.write("STATS CALCULATION TIME: " + str(time.time()-timestart))
	summaryfile.close()
	#if (os.system(" cat /tmp/globus_error_summaryfile_" + datafile + ">> " + summaryfilename)==0):
	#   print "FINAL SUMMARY FILE CREATED: ", " /var/log/globus_error_summaryfile_" + datafile
	#else:
	#   print "ERROR creating SUMMARY FILE: ", " /var/log/globus_error_summaryfile_" + datafile
	#sending stats results by mail
	str1 = 'GLOBUS_ERRORS_STATS: ' + time.strftime("%d %b",time.localtime(time.time()+nday*84600))
	mail_cmd = '''mail -s "WMS `/bin/hostname` ''' + str1 + '''" ''' + confvar.get('WMSMON_SEVER_CONTACT_EMAIL') + ''' >/dev/null < ''' + summaryfilename

	if (os.system(mail_cmd)!=0):
	   print "Sendmail FAILED!!!"
	if (os.system('rm -f ' + logfile) == 0):
	   print "Removed file: " + logfile

	#CREATING FINAL SUMMARY FILE
	if (os.system(" cat /tmp/globus_error_summaryfile_" + datafile + ">> " + summaryfilename)==0):
	   print "FINAL SUMMARY FILE CREATED: ", " /var/log/globus_error_summaryfile_" + datafile
	else:
	   print "ERROR creating SUMMARY FILE: ", " /var/log/globus_error_summaryfile_" + datafile
	sys.exit(0)
	if (os.system('rm -f /tmp/broken_jobids_' + datafile + '_uniq.txt ' + " /tmp/globus_error_summaryfile_" + datafile )):
	      print "Removed file: " + '/tmp/broken_jobids_' + datafile + '_uniq.txt ' + "/tmp/globus_error_summaryfile_" + datafile 

