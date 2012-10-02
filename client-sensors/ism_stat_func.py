#!/usr/bin/python
import os, sys, time,datetime,logging

def ism_stat(ism_path,glite_log_dir):
	''' ism_stat(ism_path,wmlog_path) -> list (ism size, ism entries)
	    Function to return the ism size in 1kB blocks and the number of VoViews entries in ism.
	    Size is returned by ls -sk ism_path.
	    Returns a list of two integers or None is fails.'''

# Initialising variables
	stat  = [0,0]
        LASTMM_MAX_DELAY = 3600
        deltaTIME = 0
        TRY_DUMP = False
        SLEEP_RETRY = 2
        DUMP_RETRY = 5
	wmlog_path = glite_log_dir + '/workload_manager_events.log'
        logger = logging.getLogger('ism_stat')

#Check if the ism file is accessible
        if (os.access(wmlog_path,os.F_OK) == True):
	       cmd = 'grep "MM for job" ' + wmlog_path + ' |tail -1'
               std = os.popen(cmd)
               stdstr =  std.readline()
               std.close()               
               if stdstr.rfind('/') != -1 :
                  std_tmp = stdstr[(stdstr.rfind('/')) + 1:]
                  stdsplit = std_tmp.split()
                  ism_entries = stdsplit[0]
                  date_MM = time.strftime("%Y",time.localtime()) + stdstr[0:(stdstr.find("-I:") - 1)]
                  datetmp = time.strptime(date_MM,"%Y %d  %b, %H:%M:%S")
                  timeMM = int(time.mktime(datetmp))
                  time_now = int(time.time())
                  deltaTIME = time_now - timeMM
                  if ism_entries.isdigit():
                        stat[0] = 0
			stat[1] = ism_entries
                  else:
                        logger.error('ERROR: could not collect VO_VIEWS number using WM log, trying ismdump')
                        stat[0] = None
                        stat[1] = None
                        TRY_DUMP = True
               else:
                  logger.error('ERROR: could not collect VO_VIEWS number using WM log, trying ismdump')
                  stat[0] = None
                  stat[1] = None
                  TRY_DUMP = True


        else:
               logger.error('ERROR: Cannot access file: ' +  wmlog_path )
	       stat[0] = None
               stat[1] = None
               TRY_DUMP = True


# ISM.DUMP FILE OBSOLETE!!
        return stat

        if ( (deltaTIME  > LASTMM_MAX_DELAY) or TRY_DUMP == True):
#Check if the ism file is accessible
            ncount = 0
            while ncount <= DUMP_RETRY :
                ncount  = ncount + 1
  	        if (os.access(ism_path,os.F_OK) == True) and (os.WEXITSTATUS(os.system(("/usr/sbin/lsof " + ism_path + '> /dev/null'))) == 1):
#If accessible try to find the ism size ....
		   cmd = 'ls -sk ' + ism_path
		   std = os.popen(cmd)
		   stdstr =  std.readline()
		   stdsplit = stdstr.split()
		   std.close()
		   ism_size = stdsplit[0]
		   if ism_size.isdigit():
                        stat[0] = ism_size
		   else:
			logger.error('ERROR: ism size is not a digit.Returning None.')
			stat[0] = None
#...and the number of ism entries
		   cmd = 'grep CEid ' + ism_path + ' | wc -l'
	           std = os.popen(cmd)
        	   stdstr =  std.readline()
	           stdsplit = stdstr.split()
        	   std.close()
		   ism_entries = stdsplit[0]
        	   if ism_entries.isdigit():
                    	stat[1] = ism_entries
	           else:
        	        logger.error('ERROR: ism_entries is not a digit.Returning None.')
	                stat[1] = None
	
	
  	        else:
		   logger.error('ERROR: Cannot access ism file: ' + ism_path)
                   if ncount <= DUMP_RETRY:
                      logger.error('Sleeping for ' + str(SLEEP_RETRY) + 'seconds and retrying...')
                      os.system('sleep ' + str(SLEEP_RETRY))
                   else:
                      logger.error('Hit max retry count...Returning none')
                      stat = [None,None]

#Return the values.
	return stat
