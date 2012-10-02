#!/usr/bin/env python
# Danilo Dongiovanni (danilo.dongiovanni@cnaf.infn.it)

import stomp
import sys
import time
import logging
try:
    import pycurl
except ImportError:
    print "Error importing pycurl"
    sys.exit(1)
try:
    import StringIO
except ImportError:
    print "Error"
    sys.exit(1)
try:
    from xml.dom import minidom
except ImportError:
    print "Error"
    sys.exit(1)
    
import logpredef
import readconf_func

logging.basicConfig()
logger = logging.getLogger('activemq_consumer_wmsnagiostest')
logger.info('Reading wmsmon conf file')
confvar=readconf_func.readconf();

#######################################
# PARAMETERS INITIALIZATION  #
#######################################
HOST = confvar.get('ACTIVEMQ_NAGIOS_BROKER_HOST')
PORT = confvar.get('ACTIVEMQ_NAGIOS_BROKER_PORT')
MSGPATH = confvar.get('ACTIVEMQ_NAGIOS_BROKER_MSGPATH')
msglist = [HOST,PORT,MSGPATH]
print msglist
HEADERS={}
LEVEL = debug_level()
LOG_FILENAME = '/tmp/wmsnagios_consumer.log'
FORMAT='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
logging.basicConfig(level=LEVEL,
                    filename=LOG_FILENAME,
                    filemode='a',
                    format=FORMAT)
# create logger
LOGGER = 'customer_stomp'
logger = logging.getLogger(LOGGER)

#######################################
# CLASS DEFINITION#####################
class MyListener(object):
    def on_connecting(self, host_and_port):
        logger.info("connecting...")
        logger.debug(host_and_port)

    def on_disconnected(self):
        global conn
        logger.info("lost connection")
        sys.exit(1)
    def on_message(self, headers, body):
        self.parse_message(headers, body)

    def on_error(self, headers, body):
        logger.error("\n\nERROR HEADERS "+str(headers))
        logger.error("\n\nERROR BODY "+str(body))
    def on_receipt(self, headers, body):
        pass

    def on_connected(self, headers, body):
        logger.info("CONNECTED")

    def parse_message(self, headers, body):
        msg = {}
        for line in body.split('\n'):
            mykey = line.split(':')[0]
            mystr = line[len(mykey)+2:]
            msg[mykey] = mystr
        #logger.debug("Parse result:  " + str(msg))
        if msg['metricName'] == 'org.sam.WN-MPI':
            logger.info("org.sam.WN-MPI FOUNDED")
            logger.debug("org.sam.WN-MPI FOUNDED: \n" + str(msg))
            msg['FLAG'] = check_msg(msg)
            if msg['FLAG'] != 2:
                is_present(msg)
            else:
                logger.info("FLAG = " + str(msg['FLAG']) + ". Nothing to do.\n")
        else:
            SITE = msg['siteName']
            logger.debug("Skipping msg for "+SITE+" about "+msg['metricName'])

def check_msg(msg):
    """Return 1 if MPI check is OK, 0 if it fails, 2 otherwise"""
    FLAG=0
##    CE = msg['hostName']
##    SITE = msg['siteName']
    STATE = {}
    if 'detailsData' in msg.keys():
        detailsData = msg['detailsData']
        for line in detailsData.split('\\n'):
            if 'Status' in line:
                STATE[line.split()[0]] = line.split()[2]
        if 'MPI' in STATE.keys():
            if STATE['MPI'] == 'OK':
                FLAG=1
        else:
            logger.warning("MPI overall status don't find")
            FLAG=2
    else:
        logger.warning("Details data don't find.")
        if 'metricStatus' in msg.keys():
            if msg['metricStatus'] == 'OK':
                logger.warning("metricStatus = OK.")
                FLAG=2
            else:
                logger.warning("metricStatus not OK.")
                FLAG=2
    logger.info("FLAG (0=FAILED, 1=OK, 2=UNKNOWN): " + str(FLAG))
    if FLAG == 2:
        logger.warning("MPI UNKNOWN for msg:")
        for k in msg.keys():
            if k != 'detailsData':
                logger.warning(str(k) + ": " + msg[k])
            else:
                logger.warning("### STARTING DETAILS ###")
                for line in detailsData.split('\\n'):
                    logger.warning(str(k) + ": " + line)
                logger.warning("### END DETAILS ###")
    return FLAG


def is_present(msg):
    UPDATE=0
    SITE = msg['siteName']
    CE = msg['hostName']
    FLAG = msg['FLAG']
    myfile = '/home/veronesi/MyDropbox/Public/pippo.ldif'
    f = open(myfile,'r')
    LINES = []
    Record = []
    try:
        for line in f:
            if line=='\n':
                LINES.append(Record)
                Record = []
            else:
                Record.append(line)
    finally:
        f.close()
    # MPI fallisce
    if FLAG == 0:
        logger.info("SITE "+SITE+", MPI FAILED. Looking for " + CE + " in " + myfile)
        FOUND = 0
        for l in LINES:
            for s in l:
                if s.find(CE)!= -1:
                    #CE gia' presente, nulla da fare
                    FOUND = 1
                    logger.info("SITE "+SITE+", MPI FAILED. CE " + CE + " already present in " + myfile + ". Nothing to do.\n")
        if FOUND == 0:
            newline = []
            #CE non presente nel file .ldf, mpi fallisce => aggiungo entry
            logger.info("SITE "+SITE+", MPI FAILED. CE " + CE + "not found in " + myfile + ". The entry should be added.")
            TAG = []
            RECORD = 0
            detailsData = msg['detailsData']
            for line in detailsData.split('\\n'):
                if line.find("MPI tags were found at") != -1:
                    RECORD = 1
                if line == '':
                    RECORD = 0
                if (RECORD == 1) and (line.find("MPI tags were found at") == -1) and (line.find("MPI-START") == -1):
                    TAG.append(line)
            comment = "# SITE %s, CE %s\n# CHECK %s, RETRIEVED FROM %s\n# SUMMARY: %s\n# EXECUTION TIME: %s\n" %(SITE,CE,msg['metricName'],msg['gatheredAt'],msg['summaryData'],msg['timestamp'])
            mystr = comment + "dn: GlueSubClusterUniqueID=%s,GlueClusterUniqueID=%s,Mds-Vo-name=%s,Mds-Vo-name=local,o=grid\nchangetype:modify\n" %(CE,CE,SITE)
            for tag in TAG:
                mystr = mystr + "delete: GlueHostApplicationSoftwareRunTimeEnvironment\nGlueHostApplicationSoftwareRunTimeEnvironment: "+tag+"\n"
            logger.info("STRING to be added:\n" + mystr + '\n')
            newline.append(mystr)
            LINES.append(mystr)
            UPDATE=1
    # MPI ok
    elif FLAG == 1:
        logger.info("SITE "+SITE+", MPI OK. Looking for "+CE+" on "+myfile)
        for l in LINES:
            for s in l:
                if s.find(CE)!= -1:
                    #CE presente nel file .ldif, mpi ok => rimuovo entry
                    logger.info("SITE "+SITE+", MPI OK. CE " + CE + "is in " + myfile + ". The entry should be removed.")
                    #LINES.remove(l)
                    UPDATE=1
            if UPDATE == 1:
                LINES.remove(l)
        if UPDATE==0:
            logger.info("SITE "+SITE+", MPI OK. CE " + CE + " not present in " + myfile + ". Nothing to do.\n")
    if UPDATE==1:
        logger.info(myfile +" need to be UPDATED." + str(len(LINES)) + "to be added.")
        f = open(myfile,'w')
        for l in LINES:
            for s in l:
                if s.find("LAST UPDATE") == -1:
                    f.writelines(s)
            f.write('\n')
        f.writelines("\n# LAST UPDATE: "+time.strftime("%Y-%m-%d %H:%M:%S"))
        f.write('\n')
        f.close()
        logger.info(myfile +" writed.\n")

def curlDownload():
    """
   Performs curl download and store output into the IO string variable 
    """
    logger.debug("Starting curlDownload")
    # GOCDB-PI url and method settings
    # Set the GOCDB URL
    gocdbpi_url = "https://goc.gridops.org/gocdbpi/public/?"
    gocdbpi_method = "get_site_list"
    gocdbpi_certification_status = "Certified"
    gocdbpi_production_status = "Production"
    # GOCDB-PI to query
    try:
        #gocdbpi_roc
        gocdb_ep = gocdbpi_url + "method=" + gocdbpi_method + "&certification_status=" + gocdbpi_certification_status + "&production_status=" + gocdbpi_production_status
    except NameError:
        #logger.debug(gocdb_ep)
        logger.critical(NameError)
        pass
    output = StringIO.StringIO()
    c = pycurl.Curl()
    c.setopt(c.URL, gocdb_ep)
    c.setopt(c.SSL_VERIFYPEER, 0)
    c.setopt(c.WRITEFUNCTION, output.write)
    c.perform()
    c.close()
    #logger.debug(output)
    return output


def xmlParsing(out):
    """
    Performs xml parsing from the xml_doc string and save result into a dictionary handler
    """
    logger.debug("Starting xmlParsing")
    xml_doc = out.getvalue()
    #logger.debug("xmlParsing - xml_doc: "+str(xml_doc))
    try:
        doc = minidom.parseString(xml_doc)
    except minidom.DOMException, e:
        logger.error(e)
    sites = doc.getElementsByTagName("SITE")
    #logger.debug("xmlParsing - sites: "+str(sites))
    handler_list  = []
    # Iterating over the main topic element and creating the mysql handler dictionary
    for s in sites:
        #logger.debug("xmlParsing - s "+str(s))
        ## Instatiating the result dictionary handler 
        handler = {}

        if s.getAttributeNode("NAME"):
            attrs_name = s.attributes["NAME"]
            handler["SiteName"] = str(attrs_name.value)
            #logger.debug("xmlParsing - handler: "+str(handler))
        handler_list.append(handler)
    logger.debug("xmlParsing - handler_list: "+str(handler_list))
    return handler_list

def get_sites():
    """ Return the list of all site name in the IT region.
        TODO: the list should be retrieved from the GOCDB. """
    logger.debug("STARTING get_sites ")
    out=curlDownload()
    #logger.debug("GET_SITES - out: "+str(out))
    site_list = xmlParsing(out)
    if len(site_list) <1:
        logger.critical("SITEs= "+str(site_list))
        sys.exit(1)
    #logger.debug("GET_SITES - site_list: "+str(site_list))
    SITE = []
    for site in site_list:
        logger.debug("Find SITE "+str(site))
        SITE.append(site['SiteName'])
    SITE.sort()
    return SITE
##    SITE = ['CIRMMP',    
##     'CNR-ILC-PISA',
##     'CNR-PROD-PISA',
##     'ESA-ESRIN',
##     'GILDA-INFN-CATANIA',
##     'GILDA-PADOVA',
##     'GILDA-SIRIUS',
##     'GILDA-VEGA',
##     'GRISU-COMETA-INAF-CT',
##     'GRISU-COMETA-INFN-CT',
##     'GRISU-COMETA-INFN-LNS',
##     'GRISU-COMETA-ING-MESSINA',
##     'GRISU-COMETA-UNICT-DIIT',
##     'GRISU-COMETA-UNICT-DMI',
##     'GRISU-COMETA-UNIPA',
##     'GRISU-CYBERSAR-CAGLIARI',
##     'GRISU-CYBERSAR-PORTOCONTE',
##     'GRISU-ENEA-GRID',
##     'GRISU-SPACI-LECCE',
##     'GRISU-SPACI-NAPOLI',
##     'GRISU-UNINA',
##     'ICEAGE-CATANIA',
##     'INFN-BARI',
##     'INFN-BOLOGNA',
##     'INFN-CAGLIARI',
##     'INFN-CATANIA',
##     'INFN-CNAF',
##     'INFN-CNAF-LHCB',
##     'INFN-FERRARA',
##     'INFN-FRASCATI',
##     'INFN-GENOVA',
##     'INFN-LNL-2',
##     'INFN-LNS',
##     'INFN-MILANO-ATLASC',
##     'INFN-NAPOLI',
##     'INFN-NAPOLI-ARGO',
##     'INFN-NAPOLI-ATLAS',
##     'INFN-NAPOLI-CMS',
##     'INFN-NAPOLI-PAMELA',
##     'INFN-PADOVA',
##     'INFN-PADOVA-CMS',
##     'INFN-PARMA',
##     'INFN-PERUGIA',
##     'INFN-PISA',
##     'INFN-ROMA1',
##     'INFN-ROMA1-CMS',
##     'INFN-ROMA1-TEO',
##     'INFN-ROMA1-VIRGO',
##     'INFN-ROMA2',
##     'INFN-ROMA3',
##     'INFN-T1',
##     'INFN-TORINO',
##     'INFN-TRIESTE',
##     'SNS-PISA',
##     'TRIGRID-INFN-CATANIA',
##     'UNI-PERUGIA',
##     'UNINA-EGEE']


def debug_level():
    LEVELS = {'debug': logging.DEBUG,
              'info': logging.INFO,
              'warning': logging.WARNING,
              'error': logging.ERROR,
              'critical': logging.CRITICAL}
    if len(sys.argv) > 1:
        if sys.argv[1] in LEVELS.keys():
            level_name = sys.argv[1]
        else:
            level_name='debug'
    else:
        level_name='info'
    return LEVELS.get(level_name, logging.NOTSET)

if __name__ == '__main__':
    logger.info("\n\n\nPROGRAM STARTED")
    SITE=get_sites()
    logger.debug("MAIN - SITE "+str(SITE))
    #sys.exit(0)
    conn = stomp.Connection([(HOST,PORT)])
    conn.set_listener('MyConsumer', MyListener())
    conn.start()
    conn.connect(headers = {'client-id' : 'WMSMonitor'})
    i=0
    while i < len(SITE):
        logger.debug("SITE "+SITE[i])
        TOPIC="/topic/grid.probe.metricOutput.EGEE.project."+SITE[i]
        logger.info("Subscribing "+TOPIC)
        conn.subscribe(destination=TOPIC, ack='auto',headers = {'activemq.subscriptionName' : 'WMSMonitor_'+SITE[i]})
        i=i+1

    while 1:
        time.sleep(0.5)
                                          