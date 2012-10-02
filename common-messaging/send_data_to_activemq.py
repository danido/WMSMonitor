#!/usr/bin/env python

# J.M. Dana
# Jose.Dana@cern.ch
import sys,os
#sys.path.append('./stomp/')
import stomp
import time
import logpredef_wmslb
import logging
import readconf_func
from socket import gethostname


logger = logging.getLogger('send_data_to_activemq')

confvar = readconf_func.readconf();
sender_hostname = gethostname()

class MyListener(object):
    def on_connecting(self, host_and_port):
        logger.info('connecting...')
        #self.c.connect(wait=True)

    def on_disconnected(self):
        logger.info("lost connection")

    def on_message(self, headers, body):
        #self.__print_async("MESSAGE", headers, body)
        logger.info('MESSAGE')

    def on_error(self, headers, body):
        #self.__print_async("ERROR", headers, body)
        logger.error('ERROR')
        raise ActiveMQError
    def on_receipt(self, headers, body):
        #self.__print_async("RECEIPT", headers, body)
        logger.info('RECEIPT')
    def on_connected(self, headers, body):
        #self.__print_async("CONNECTED", headers, body)
        logger.info('CONNECTED')
    def __print_async(self, frame_type, headers, body):
        print "\r  \r",
        print frame_type
        
        for header_key in headers.keys():
            print '%s: %s' % (header_key, headers[header_key])
            
        print
        print body
        print '> ',
        sys.stdout.flush()

def send_data_to_activemq(file_to_send,HOST,PORT,TOPIC,metrics_category):

    logger.info('Iizialising activeMQ connection. HOST = ' + HOST + 'PORT = ' + PORT + 'TOPIC = ' + TOPIC)
    try:
       conn = stomp.Connection([(HOST,int(PORT))])
       conn.set_listener('MyListener', MyListener())
       conn.start()
       logger.info('Connecting...')
       conn.connect()    
       logger.info('Connection OK')
    except:
       logger.error('Connection Problems. Check HOST AND PORT in site.def or contact ' + confvar['WMSMON_SEVER_CONTACT_EMAIL'])
       logger.error('FILE NOT SENT!')
       return 'ERROR'
    try:
       fsend = open(file_to_send,'r')
    except IOError:
       logger.error('ERROR in opening the file to send: ' + file_to_send)
       return 'ERROR'
    stdstr = fsend.readlines()
    line = ''
    for st in stdstr:
       line = line + st
    try:
       conn.send(line,destination=TOPIC, ack='auto',headers = {'SENDERHOSTNAME' : sender_hostname, 'METRICSCATEGORY' : metrics_category , 'WMSHOSTNAME' : sender_hostname })
       logger.info('File SENT. File is: ' + file_to_send)
    except:
       logger.error('Sending problems. Contact ' + confvar['WMSMON_SEVER_CONTACT_EMAIL'])
       return 'PROBLEMS'

    logger.info('Disconnecting')
    conn.disconnect()        

    return 'OK'
