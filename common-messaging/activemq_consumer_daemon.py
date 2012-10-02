#!/usr/bin/env python

# J.M. Dana
# Jose.Dana@cern.ch
import sys,os
import stomp
import time
import logging
import logpredef
import readconf_func

logging.basicConfig()
logger = logging.getLogger('activemq_consumer_daemon')
logger.info('Reading wmsmon conf file')
confvar=readconf_func.readconf();

#######################################
# ACTIVEMQ PARAMETERS INITIALIZATION  #
#######################################

HOST = confvar.get('ACTIVEMQ_BROKER_HOST')
PORT = confvar.get('ACTIVEMQ_PORT')
MSGPATH = confvar.get('ACTIVEMQ_MSGPATH')
HOST='gridmsg002.cern.ch'
#HOST='gridmsg101.cern.ch'
#HOST='msgbroker-01.cnaf.infn.it'

msglist = [HOST,PORT,MSGPATH]
print msglist

#HOST='gridmsg002.cern.ch'
PORT=6163
HEADERS={}

class MyListener(object):
    def on_connecting(self, host_and_port):
        logger.info('connecting...')

    def on_disconnected(self):
        logger.info("lost connection")

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
        print filedump
        try: 
             logger.info('Writing to file: ' + filedump)
             f = open(filedump,'w')
             f.write(body)
             f.close()
        except: 
             logger.error('ERROR: Unable to write to file: ' + filedump)

if __name__ == '__main__':
    if len(sys.argv) != 2:
        print sys.argv[0],'<topic or queue>'
        sys.exit(-1)

    TOPIC=sys.argv[1]
    print 'TOPIC = ', TOPIC
    conn = stomp.Connection([(HOST,PORT)])
    conn.set_listener('MyConsumer', MyListener())
    conn.start()
    conn.connect()    
    
    conn.subscribe(destination=TOPIC, ack='auto', headers=HEADERS)
    while(1):
        time.sleep(0.5)

    conn.disconnect()        

    
