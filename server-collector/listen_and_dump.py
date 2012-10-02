#!/usr/bin/env python

# J.M. Dana
# Jose.Dana@cern.ch

import stomp
import sys
import time
from optparse import OptionParser
import os

import logging
logging.basicConfig()


PORT=6163

NUM=-1
DEST=''
TOPIC=''

OUTPUT=[]

class MyListener(object):
    def __init__(self, verbose = True):
        self.verbose = verbose
        
    def on_connecting(self, host_and_port):
        if self.verbose:
            log.debug('Connecting : %s:%s'%host_and_port)

     def on_disconnected(self, headers, body)
#    def on_disconnected(self):
        print "lost connection"

    def on_message(self, headers, body):
        global OUTPUT
        OUTPUT.append([headers,body])

        print 'Received!'

    def on_error(self, headers, body):
        self.__print_async("ERROR", headers, body)

    def on_receipt(self, headers, body):
        self.__print_async("RECEIPT", headers, body)

    def on_connected(self, headers, body):
        self.__print_async("CONNECTED", headers, body)
    
    def __print_async(self, frame_type, headers, body):
        print "\r  \r",
        print frame_type
        
        for header_key in headers.keys():
            print '%s: %s' % (header_key, headers[header_key])
            
        print
        print body
        print '> ',
        sys.stdout.flush()

if __name__ == '__main__':
    usage='usage: %prog [options] <topic or queue>'
    parser = OptionParser(usage=usage)
    parser.add_option('-f', '--file',dest='file', 
                      help='The file where you want to dump the messages')
    parser.add_option('-b', '--broker',dest='broker',default='gridmsg001.cern.ch',help='The broker [default=gridmsg001.cern.ch]')
    parser.add_option('-n', '--num', dest='num',default=10,help='MINIMUM number of messages to be received before exiting [default=10]')
    parser.add_option('-c', '--client', dest='client',help='Client ID')
    parser.add_option('-s', '--subscription-name', dest='name',help='Subscription Name')

    parser.add_option('--json',dest='json', default=False,action="store_true", help='Use JSON format [default=YAML')


    opts,args=parser.parse_args()

    HOST=opts.broker
    NUM=int(opts.num)

    if not opts.file:
        opts.file = sys.stdout
    
    if len(args)==0:
        parser.error('Please specify topic/queue to listen to.')
    
    if opts.json:
        import simplejson as json
    else:
        import yaml
        
    TOPIC=args[0]

    conn = stomp.Connection([(HOST,PORT)])
    conn.set_listener('Dumper', MyListener())
    conn.start()
    
    connect_headers = {}
    if opts.client:
        connect_headers['client-id'] = opts.client
    conn.connect(headers = connect_headers, wait = True)

    if opts.name != None:
        connect_headers['activemq.subscriptionName'] = opts.name
   
    conn.subscribe(destination=TOPIC, ack='auto', headers=connect_headers)

    try:
        while len(OUTPUT)<NUM:
            time.sleep(0.1)
    except KeyboardInterrupt:
        pass

    f = open(opts.file,'wb')

    if opts.json:
        json.dump(OUTPUT, f, indent=2)
    else:
        f.write(yaml.dump(OUTPUT))

    f.close()

    conn.disconnect()        

    
