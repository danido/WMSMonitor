import logging
import sys
import os
import readconf_func

confvar=readconf_func.readconf();

LOG_FILE = confvar.get('LOG_FILE')
if LOG_FILE == '' :
   print 'No LOG_FILE key found in conf file ! Exiting...'
   sys.exit()


logger = logging.getLogger('wms-sensor-wrapper') #put here the name of the function/main
hdlr = logging.FileHandler(LOG_FILE)
formatter = logging.Formatter('%(asctime)s   %(name)-20s :  %(levelname)-8s %(message)s','%Y-%m-%d %H:%M:%S')
hdlr.setFormatter(formatter)
logger.addHandler(hdlr)
logger.setLevel(logging.DEBUG)

logger1 = logging.getLogger('lb-sensor-wrapper') #put here the name of the function/main
hdlr = logging.FileHandler(LOG_FILE)
formatter = logging.Formatter('%(asctime)s   %(name)-20s :  %(levelname)-8s %(message)s','%Y-%m-%d %H:%M:%S')
hdlr.setFormatter(formatter)
logger1.addHandler(hdlr)
logger1.setLevel(logging.DEBUG)

logger2 = logging.getLogger('wms_sensor') #put here the name of the function/main
hdlr = logging.FileHandler(LOG_FILE)
formatter = logging.Formatter('%(asctime)s   %(name)-20s :  %(levelname)-8s %(message)s','%Y-%m-%d %H:%M:%S')
hdlr.setFormatter(formatter)
logger2.addHandler(hdlr)
logger2.setLevel(logging.DEBUG)

logger3 = logging.getLogger('lb_sensor') #put here the name of the function/main
hdlr = logging.FileHandler(LOG_FILE)
formatter = logging.Formatter('%(asctime)s   %(name)-20s :  %(levelname)-8s %(message)s','%Y-%m-%d %H:%M:%S')
hdlr.setFormatter(formatter)
logger3.addHandler(hdlr)
logger3.setLevel(logging.DEBUG)

logger4 = logging.getLogger('lb_query') #put here the name of the function/main
hdlr = logging.FileHandler(LOG_FILE)
formatter = logging.Formatter('%(asctime)s   %(name)-20s :  %(levelname)-8s %(message)s','%Y-%m-%d %H:%M:%S')
hdlr.setFormatter(formatter)
logger4.addHandler(hdlr)
logger4.setLevel(logging.DEBUG)

logger5 = logging.getLogger('lb_query_daily') #put here the name of the function/main
hdlr = logging.FileHandler(LOG_FILE)
formatter = logging.Formatter('%(asctime)s   %(name)-20s :  %(levelname)-8s %(message)s','%Y-%m-%d %H:%M:%S')
hdlr.setFormatter(formatter)
logger5.addHandler(hdlr)
logger5.setLevel(logging.DEBUG)


logger6 = logging.getLogger('ism_stat') #put here the name of the function/main
hdlr = logging.FileHandler(LOG_FILE)
formatter = logging.Formatter('%(asctime)s   %(name)-20s :  %(levelname)-8s %(message)s','%Y-%m-%d %H:%M:%S')
hdlr.setFormatter(formatter)
logger6.addHandler(hdlr)
logger6.setLevel(logging.DEBUG)

logger7 = logging.getLogger('dg20') #put here the name of the function/main
hdlr = logging.FileHandler(LOG_FILE)
formatter = logging.Formatter('%(asctime)s   %(name)-20s :  %(levelname)-8s %(message)s','%Y-%m-%d %H:%M:%S')
hdlr.setFormatter(formatter)
logger7.addHandler(hdlr)
logger7.setLevel(logging.DEBUG)

logger8 = logging.getLogger('cerate_CE_MM') #put here the name of the function/main
hdlr = logging.FileHandler(LOG_FILE)
formatter = logging.Formatter('%(asctime)s   %(name)-20s :  %(levelname)-8s %(message)s','%Y-%m-%d %H:%M:%S')
hdlr.setFormatter(formatter)
logger8.addHandler(hdlr)
logger8.setLevel(logging.DEBUG)

logger9 = logging.getLogger('send_CE_MM') #put here the name of the function/main
hdlr = logging.FileHandler(LOG_FILE)
formatter = logging.Formatter('%(asctime)s   %(name)-20s :  %(levelname)-8s %(message)s','%Y-%m-%d %H:%M:%S')
hdlr.setFormatter(formatter)
logger9.addHandler(hdlr)
logger9.setLevel(logging.DEBUG)

logger10 = logging.getLogger('send_long_file') #put here the name of the function/main
hdlr = logging.FileHandler(LOG_FILE)
formatter = logging.Formatter('%(asctime)s   %(name)-20s :  %(levelname)-8s %(message)s','%Y-%m-%d %H:%M:%S')
hdlr.setFormatter(formatter)
logger10.addHandler(hdlr)
logger10.setLevel(logging.DEBUG)

logger11 = logging.getLogger('lb-refill-sensor-wrapper') #put here the name of the function/main
hdlr = logging.FileHandler(LOG_FILE)
formatter = logging.Formatter('%(asctime)s   %(name)-20s :  %(levelname)-8s %(message)s','%Y-%m-%d %H:%M:%S')
hdlr.setFormatter(formatter)
logger11.addHandler(hdlr)
logger11.setLevel(logging.DEBUG)

logger12 = logging.getLogger('wms_usermapping') #put here the name of the function/main
hdlr = logging.FileHandler(LOG_FILE)
formatter = logging.Formatter('%(asctime)s   %(name)-20s :  %(levelname)-8s %(message)s','%Y-%m-%d %H:%M:%S')
hdlr.setFormatter(formatter)
logger12.addHandler(hdlr)
logger12.setLevel(logging.DEBUG)

logger13 = logging.getLogger('wms_balancing_metric') #put here the name of the function/main
hdlr = logging.FileHandler(LOG_FILE)
formatter = logging.Formatter('%(asctime)s   %(name)-20s :  %(levelname)-8s %(message)s','%Y-%m-%d %H:%M:%S')
hdlr.setFormatter(formatter)
logger13.addHandler(hdlr)
logger13.setLevel(logging.DEBUG)

logger14 = logging.getLogger('send_data_to_activemq') #put here the name of the function/main
hdlr = logging.FileHandler(LOG_FILE)
formatter = logging.Formatter('%(asctime)s   %(name)-20s :  %(levelname)-8s %(message)s','%Y-%m-%d %H:%M:%S')
hdlr.setFormatter(formatter)
logger14.addHandler(hdlr)
logger14.setLevel(logging.DEBUG)

logger15 = logging.getLogger('mail_garbage_coll') #put here the name of the function/main
hdlr = logging.FileHandler(LOG_FILE)
formatter = logging.Formatter('%(asctime)s   %(name)-20s :  %(levelname)-8s %(message)s','%Y-%m-%d %H:%M:%S')
hdlr.setFormatter(formatter)
logger15.addHandler(hdlr)
logger15.setLevel(logging.DEBUG)

logger16 = logging.getLogger('stomp') #put here the name of the function/main
hdlr = logging.FileHandler(LOG_FILE)
formatter = logging.Formatter('%(asctime)s   %(name)-20s :  %(levelname)-8s %(message)s','%Y-%m-%d %H:%M:%S')
hdlr.setFormatter(formatter)
logger16.addHandler(hdlr)
logger16.setLevel(logging.DEBUG)


logger17 = logging.getLogger('lb_apiquery') #put here the name of the function/main
hdlr = logging.FileHandler(LOG_FILE)
formatter = logging.Formatter('%(asctime)s   %(name)-20s :  %(levelname)-8s %(message)s','%Y-%m-%d %H:%M:%S')
hdlr.setFormatter(formatter)
logger17.addHandler(hdlr)
logger17.setLevel(logging.DEBUG)

# define a Handler which writes INFO messages or higher to the sys.stderr
#console = logging.StreamHandler()
#console.setLevel(logging.DEBUG)
# set a format which is simpler for console use
#formatter = logging.Formatter('%(name)-20s: %(levelname)-8s %(message)s')
# tell the handler to use this format
#console.setFormatter(formatter)
# add the handler to the root logger
#logging.getLogger('').addHandler(console)
