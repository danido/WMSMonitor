#! /usr/bin/python
import time,sys,os

sys.path.append('/opt/WMSMonitor/common')
sys.path.append('/opt/WMSMonitor/common/classes')
import readconf_func

if len(sys.argv) < 2:
   print "\nUsage:\n"
   print "globus_error_detector.py NDAYAGO\n"
   print "Ex. globus_error_detector.py 0 [-1]\n"
   print "..will detect today's [yesterday's] errors\n"
   sys.exit(1)
timestart=time.time()
#calculating date
nday=int(sys.argv[1])
if nday > 0:
   print "\nUsage:\n"
   print "globus_error_detector.py NDAYAGO\n"
   print "ERROR: NDAYAGO must be <=0 "
   sys.exit(1)

confvar = readconf_func.readconf();

#DISABLING HISTOGRAM N_ERROR vs CE
HISTCE_FLAG=0
VERBOSE_FLAG=0

data = "\"" + time.strftime("%d %b",time.localtime(time.time()+nday*84600)) + "\""
datafile=time.strftime("%d%b",time.localtime(time.time()+nday*84600))
datacalc=time.localtime(time.time()+nday*84600)[1:3]
print "\n\nGlobus error detector starts on date: " + data + "\""

#deciding whether to use rotated log or not
#confvar={'GLITE_LOG_DIR':'/var/log/wms','SITE_CONTACT': 'danilo.dongiovanni@cnaf.infn.it,daniele.cesini@cnaf.infn.it,marco.cecchi@cnaf.infn.it'}
logfile = ''
if ((os.access(confvar.get('GLITE_LOG_DIR') + '/logmonitor_events.log',os.F_OK) == True ) and 
    (os.access(confvar.get('GLITE_LOG_DIR') + '/logmonitor_events.log.1',os.F_OK) == False)):
   logfile = confvar.get('GLITE_LOG_DIR') + '/logmonitor_events.log'

elif  (os.access(confvar.get('GLITE_LOG_DIR') + '/logmonitor_events.log',os.F_OK) == True):
   lines = os.popen("tail -n2 /var/log/wms/logmonitor_events.log.*|grep -v 'file rotation'|grep -v '==>'").readlines()
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
      print "ERROR:Could not find logmonitor log files \n"
      sys.exit(-1)
            
else:
   print "ERROR: Could not find logmonitor log files in :", confvar.get('GLITE_LOG_DIR') + '/logmonitor_events.log' , '\n'
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
   if (os.access('/tmp/broken_jobids_' + datafile + '_uniq.txt',os.F_OK) == False):
      print "No Globus error found, exiting"
      sys.exit(0)
   else:
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

if HISTCE_FLAG: 
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
summaryfilename= confvar['GLOBUS_ERROR_FILE_LOCATION']
summaryfile = open(summaryfilename,'w')
if VERBOSE_FLAG:
   stream = os.popen('cat /tmp/globus_error_summaryfile_' + datafile + '|wc -l')
   if (stream):
      totalfail=stream.readlines()
   summaryfile.write("\nTOTAL FAILURES DETECTED: " + totalfail[0].strip() + "\n")
   summaryfile.write("\nHISTOGRAM OF GLOBUS ERROR MESSAGES:\n")

#WRITING GLOBUS ERR STATS
for line in histerr:
    summaryfile.write(line)

if HISTCE_FLAG:
   #WRITING GLOBUS ERR STATS vs CE INVOLVED
   summaryfile.write("\n\nHISTOGRAM OF DESTINATION CE:\n")
   for line in histce:
      summaryfile.write(line)
if VERBOSE_FLAG:
   summaryfile.write("\n\n")
   summaryfile.write("STATS CALCULATION TIME: " + str(time.time()-timestart) + "\n")
summaryfile.close()


#if (os.system(" cat /tmp/globus_error_summaryfile_" + datafile + ">> " + summaryfilename)==0):
#   print "FINAL SUMMARY FILE CREATED: ", " /var/log/globus_error_summaryfile_" + datafile
#else:
#   print "ERROR creating SUMMARY FILE: ", " /var/log/globus_error_summaryfile_" + datafile
#sending stats results by mail
#str1 = 'GLOBUS_ERRORS_STATS: ' + time.strftime("%d %b",time.localtime(time.time()+nday*84600))
#mail_cmd = '''mail -s "WMS `/bin/hostname` ''' + str1 + '''" ''' + confvar.get('SITE_CONTACT') + ''' >/dev/null < ''' + summaryfilename

#if (os.system(mail_cmd)!=0):
#   print "Sendmail FAILED!!!"
#if (os.system('rm -f ' + logfile) == 0):
#   print "Removed file: " + logfile




#CREATING FINAL SUMMARY FILE
#commenting the following lines, the cat of the summary file on the final summary is not needed!!!
#if (os.system(" cat /tmp/globus_error_summaryfile_" + datafile + ">> " + summaryfilename)==0):
#   print "FINAL SUMMARY FILE CREATED: ",  confvar['GLOBUS_ERROR_FILE_LOCATION']
#else:
#   print "ERROR creating SUMMARY FILE: ",  confvar['GLOBUS_ERROR_FILE_LOCATION']
#sys.exit(0)


if (os.system('rm -f /tmp/broken_jobids_' + datafile + '_uniq.txt ' + " /tmp/globus_error_summaryfile_" + datafile )):
   print "Removed file: " + '/tmp/broken_jobids_' + datafile + '_uniq.txt ' + "/tmp/globus_error_summaryfile_" + datafile 
