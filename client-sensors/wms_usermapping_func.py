#!/usr/bin/python

import os
import sys
import time
import readconf_func
import socket


def wms_usermapping():

    #Initializing logger
    import logging
    import logpredef_wmslb 
    logger = logging.getLogger('wms_usermapping')
    confvar=readconf_func.readconf();
    timenow = str(int(time.mktime(time.localtime())))
 
    hostname=socket.getfqdn()
    logger.info("server hostname is :" + hostname)

    if hostname == '':
      logger.error('Could not determine machine hostname! Exiting...')
      sys.exit(1)
 
    filename = confvar['INSTALL_PATH'] + '/sensors/tmp/USERSMAPPING.txt'
    f = open(filename,'w')
    f.write("START OF MAPPING TABLE\n")
    data = "\"" + time.strftime("%d %b",time.localtime()) + "\""

    #deciding whether to use rotated log or not

    logfile = ''
    maxlog = int(confvar['MAX_ROTATED_LOG'])
    for i in range(maxlog + 1):
       if i == 0:
          if  (os.access(confvar.get('GLITE_LOG_DIR') + '/wmproxy.log',os.F_OK) == True):
             logfile = logfile + confvar.get('GLITE_LOG_DIR') + '/wmproxy.log'
       else:
          fname = confvar.get('GLITE_LOG_DIR') + '/wmproxy.log.' + str(i)
          if  (os.access(fname,os.F_OK) == True):
             std = os.popen("tail -2 " + fname + " | grep " + data)
             if len(std.readlines()):
                logfile = logfile + ' ' + fname

    cmd = "grep " + data + " " + logfile + " |grep -A1 CLIENT > " + confvar['INSTALL_PATH'] + "/sensors/tmp/tmpgrep.txt"
    if (os.system(cmd) == 0): 
       logfile = confvar['INSTALL_PATH'] + "/sensors/tmp/tmpgrep.txt"
       cmd = "cat " + logfile + " | grep CLIENT| sed -e 's/.*DN: //g' -e 's/\/CN=proxy.*//g' |" + "grep -v " + data + " " + "| sort |uniq"
       std = os.popen(cmd)
       stdstr =  std.readlines()
       if ( len(stdstr) > 0 ):
         for line in stdstr:
                ltmp = line.split('/CN=')
                user = ltmp[len(ltmp)-1]
                user = user.split('/')[0]
                cmd =  'grep -A1 "' + user.rstrip() + '" '  + logfile + " |grep Role |tail -1 | sed \'s/.*VOMS.*0 //g\'"
                std = os.popen(cmd)
                stdstr =  std.readlines()
                if ( len(stdstr) > 0 ):
                    istr = stdstr[0]
                    for l in istr.split(' '):
                        if l.find('Role')!= -1:
                           VO = l.split('/')[1]
                           VO_SUB = l[(l.find(VO)+len(VO)):-1]
#                           CAPABILITY = l.split('/')[3].split('=')[1]
#                           print 'USER: ' + user.rstrip() + '\nVO = ' + VO + '\nRole = ' + ROLE + '\nCapability = ' + CAPABILITY 
#                           print line.rstrip(),' ',user.rstrip(), ' ', VO , ' ', VO_SUB
                           f.write(line.rstrip() + ' | ' + VO + ' | ' + VO_SUB + '\n')
                           
                else:
                     logger.error("ERROR: Could not determine User /VO/Role/Capability ! \n")
       else:
         logger.error("FILE " + logfile + " NOT FOUND! Exiting...\n")

       f.write("END OF MAPPING TABLE\n")
       f.close()
       cmd = 'rm -f ' + logfile
       os.system(cmd)
       
wms_usermapping()

