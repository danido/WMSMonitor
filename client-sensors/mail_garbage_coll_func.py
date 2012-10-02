#! /usr/bin/python
import os
import time
import logging
import logpredef_wmslb

def mail_garbage_coll(path,time_to_live):

   logger = logging.getLogger('mail_garbage_coll')
   logger.info('Sent mail garbage collector invoked. We will now search for too old sent mail')
   logger.info('Searching on path: ' + path)
   logger.info('And using a time_to_live: ' + str(time_to_live) + ' seconds')
   time_to_live = float(time_to_live)
   timenow = time.time()
   flist = os.listdir(path)
   #logger.info('This is the filelist ' + str(flist) )
   for fff in flist:
      fcomp = path + '/' + fff
      mod_time = os.stat(fcomp)[8]
      #logger.info(fff + '   ' + str(timenow - mod_time))
      if (timenow - mod_time) > time_to_live:
         try:
            os.remove(fcomp)
            logger.info('File removed: '  + fcomp)
         except OSError:
            logger.error('Cannot remove file: ' + fcomp)
   try:
      tmpfile = open(path + '/last_garbage_run.txt','w')
      tmpfile.write(str(timenow) + '\n')
      tmpfile.close()
   except IOError:
      logger.error('Cannot put the lastrun time file on path: ' + path )
   logger.info('Sent mail garbage collection completed')
