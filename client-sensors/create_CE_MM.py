#!/usr/bin/python


# Python executable to creare CE matchmaking statistics
# It creates a file in /tmp with the histogram of matched ce statistics
# according to the format occurrence ce_number
# If the file already exists the file is overwritten
# The file start with START OF FILE and end with END OF FILE 
# it returns (prints in std) a string FILE CREATED.FILENAME=<filename>


import os,sys,logging,time

import logpredef_wmslb

logger = logging.getLogger('cerate_CE_MM')

DATE = time.strftime('%d %b',time.localtime())
FILEDATE = time.strftime('%d%b%Y',time.localtime())

filename = "/tmp/CE_MM_" + FILEDATE + ".txt"
try:
   logger.info('Opening file for writing. File is ' + filename)
   outfile = open(filename,'w')
except IO_Error:
   logger.Error('Error opening file for writing. File is ' + filename + '. Exiting')
   sys.exit(1)

outfile.write('START OF FILE\n')
logger.info('Launching grep command to extract statistics')
cmd = "grep 'MM for '  /var/log/wms/workload_manager_events.log* |grep " + '"' + DATE + '"' + " |awk '{print $11}'| sed 's/(/ /'| sed 's/\// /'|awk '{print $1}' |sort -g|uniq -c"
logger.info('Command is ' + cmd)
std = os.popen(cmd)
outstring = std.readlines()
logger.info('Writing statistics on file')
for line in outstring:
   outfile.write(line)
logger.info('Closing output file')
outfile.write('END OF FILE\n')
outfile.close()
print 'FILE CREATED.FILENAME=' + filename
