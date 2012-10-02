#!/usr/bin/env python
# danilo.dongiovanni@cnaf.infn.it
# J.M. Dana
# Jose.Dana@cern.ch

import sys, time
from daemon_class import Daemon
import os, commands, sys, fpformat
import MySQLdb,time,datetime
import logging
import logpredef
import readconf_func
import stomp

class MyDaemon(Daemon):
        def __init__(self, pidfile, stdin='/dev/null', stdout='/var/log/wmsmonitor_activemq_consumer.log', stderr='/var/log/wmsmonitor_activemq_consumer.log'):
                self.stdin = stdin
                self.stdout = stdout
                self.stderr = stderr
                self.pidfile = pidfile

        def run(self):

		logging.basicConfig()
		logger = logging.getLogger('activemq_consumer_daemon')
		logger.info('Reading wmsmon conf file')
		confvar=readconf_func.readconf();

		#######################################
		# ACTIVEMQ PARAMETERS INITIALIZATION  #
		#######################################

		HOST = confvar.get('ACTIVEMQ_BROKER_HOST')
		PORT = int(confvar.get('ACTIVEMQ_PORT'))
		MSGPATH = confvar.get('ACTIVEMQ_MSGPATH')
                TOPIC= confvar.get('ACTIVEMQ_TOPIC')
		msglist = [HOST,PORT,MSGPATH,TOPIC]
		logger.info(msglist)

		HEADERS={}

		class MyListener(object):
		    def on_connecting(self, host_and_port):
			logger.info('connecting...')

		    def on_disconnected(self, opt1='Null'):
			logger.info("lost connection")
                        sys.exit(1)

		    def on_message(self, headers, body):
			self.__dump_on_file("MESSAGE", headers, body)

		    def on_error(self, headers, body):
			self.__print_async("ERROR", headers, body)

		    def on_receipt(self, headers, body):
			self.__print_async("RECEIPT", headers, body)

		    def on_connected(self, headers, body):
			self.__print_async("CONNECTED", headers, body)
		    
		    def __print_async(self, frame_type, headers, body):
			logger.info(frame_type)

		    def __dump_on_file(self, frame_type, headers, body):

		        filedump = MSGPATH + '/' + headers['SENDERHOSTNAME'] + '_' + headers['METRICSCATEGORY'] + '_' + headers['timestamp'] + '_' + headers['message-id'].split(':')[1] + '_' + headers['message-id'].split(':')[2] + '.dat'
#			filedump = MSGPATH + '/' + headers['message-id'] + '.dat'
			print filedump
			try: 
			     logger.info('Writing to file: ' + filedump)
			     f = open(filedump,'w')
			     f.write(body)
			     f.close()
			except: 
			     logger.error('ERROR: Unable to write to file: ' + filedump)

	        print 'TOPIC = ', TOPIC
		conn = stomp.Connection([(HOST,PORT)])
		conn.set_listener('MyConsumer', MyListener())
		conn.start()
		conn.connect()    
		    
		conn.subscribe(destination=TOPIC, ack='auto', headers=HEADERS)
		while(1):
			time.sleep(0.5)

		conn.disconnect()        

		   
if __name__ == "__main__":
        daemon = MyDaemon('/tmp/activemq_consumer.pid')
        if len(sys.argv) == 2:
                if 'start' == sys.argv[1]:
                        daemon.start()
                elif 'stop' == sys.argv[1]:
                        daemon.stop()
                elif 'restart' == sys.argv[1]:
                        daemon.restart()
                else:
                        print "Unknown command"
                        sys.exit(2)
                sys.exit(0)
        else:
                print "usage: %s start|stop|restart" % sys.argv[0]
                sys.exit(2)
 
