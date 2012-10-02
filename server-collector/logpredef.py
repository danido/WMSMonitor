import logging
import sys
import os
import readconf_func

confvar=readconf_func.readconf();

LOG_FILE = confvar.get('LOG_FILE')
if LOG_FILE == '' :
   print 'No LOG_FILE key found in conf file ! Exiting...'
   sys.exit()

logger4 = logging.getLogger('data_collector') #put here the name of the function/main
hdlr = logging.FileHandler(LOG_FILE)
formatter = logging.Formatter('%(asctime)s   %(name)-20s :  %(levelname)-8s %(message)s','%Y-%m-%d %H:%M:%S')
hdlr.setFormatter(formatter)
logger4.addHandler(hdlr)
logger4.setLevel(logging.DEBUG)


logger5 = logging.getLogger('data_sensor_collector') #put here the name of the function/main
hdlr = logging.FileHandler(LOG_FILE)
formatter = logging.Formatter('%(asctime)s   %(name)-20s :  %(levelname)-8s %(message)s','%Y-%m-%d %H:%M:%S')
hdlr.setFormatter(formatter)
logger5.addHandler(hdlr)
logger5.setLevel(logging.WARNING)


logger6 = logging.getLogger('activemq_consumer_daemon') #put here the name of the function/main
hdlr = logging.FileHandler(LOG_FILE)
formatter = logging.Formatter('%(asctime)s   %(name)-20s :  %(levelname)-8s %(message)s','%Y-%m-%d %H:%M:%S')
hdlr.setFormatter(formatter)
logger6.addHandler(hdlr)
logger6.setLevel(logging.WARNING)


logger7 = logging.getLogger('data_sensor_trigger') #put here the name of the function/main
hdlr = logging.FileHandler(LOG_FILE)
formatter = logging.Formatter('%(asctime)s   %(name)-20s :  %(levelname)-8s %(message)s','%Y-%m-%d %H:%M:%S')
hdlr.setFormatter(formatter)
logger7.addHandler(hdlr)
logger7.setLevel(logging.WARNING)

logger8 = logging.getLogger('data_collector_daily') #put here the name of the function/main
hdlr = logging.FileHandler(LOG_FILE)
formatter = logging.Formatter('%(asctime)s   %(name)-20s :  %(levelname)-8s %(message)s','%Y-%m-%d %H:%M:%S')
hdlr.setFormatter(formatter)
logger8.addHandler(hdlr)
logger8.setLevel(logging.WARNING)

logger9 = logging.getLogger('create_daily') #put here the name of the function/main
hdlr = logging.FileHandler(LOG_FILE)
formatter = logging.Formatter('%(asctime)s   %(name)-20s :  %(levelname)-8s %(message)s','%Y-%m-%d %H:%M:%S')
hdlr.setFormatter(formatter)
logger9.addHandler(hdlr)
logger9.setLevel(logging.WARNING)

logger10 = logging.getLogger('data_lb_autoupdater_main') #put here the name of the function/main
hdlr = logging.FileHandler(LOG_FILE)
formatter = logging.Formatter('%(asctime)s   %(name)-20s :  %(levelname)-8s %(message)s','%Y-%m-%d %H:%M:%S')
hdlr.setFormatter(formatter)
logger10.addHandler(hdlr)
logger10.setLevel(logging.WARNING)

logger11 = logging.getLogger('snmp-collector-module') #put here the name of the function/main
hdlr = logging.FileHandler(LOG_FILE)
formatter = logging.Formatter('%(asctime)s   %(name)-20s :  %(levelname)-8s %(message)s','%Y-%m-%d %H:%M:%S')
hdlr.setFormatter(formatter)
logger11.addHandler(hdlr)
logger11.setLevel(logging.WARNING)

logger12 = logging.getLogger('get_result_LB') #put here the name of the function/main
hdlr = logging.FileHandler(LOG_FILE)
formatter = logging.Formatter('%(asctime)s   %(name)-20s :  %(levelname)-8s %(message)s','%Y-%m-%d %H:%M:%S')
hdlr.setFormatter(formatter)
logger12.addHandler(hdlr)
logger12.setLevel(logging.WARNING)

logger13 = logging.getLogger('get_result_WMS') #put here the name of the function/main
hdlr = logging.FileHandler(LOG_FILE)
formatter = logging.Formatter('%(asctime)s   %(name)-20s :  %(levelname)-8s %(message)s','%Y-%m-%d %H:%M:%S')
hdlr.setFormatter(formatter)
logger13.addHandler(hdlr)
logger13.setLevel(logging.WARNING)

logger14 = logging.getLogger('wms_balancing_metric') #put here the name of the function/main
hdlr = logging.FileHandler(LOG_FILE)
formatter = logging.Formatter('%(asctime)s   %(name)-20s :  %(levelname)-8s %(message)s','%Y-%m-%d %H:%M:%S')
hdlr.setFormatter(formatter)
logger14.addHandler(hdlr)
logger14.setLevel(logging.WARNING)

logger15 = logging.getLogger('CE_MM_collector.py') #put here the name of the function/main
hdlr = logging.FileHandler(LOG_FILE)
formatter = logging.Formatter('%(asctime)s   %(name)-20s :  %(levelname)-8s %(message)s','%Y-%m-%d %H:%M:%S')
hdlr.setFormatter(formatter)
logger15.addHandler(hdlr)
logger15.setLevel(logging.WARNING)

logger16 = logging.getLogger('long_file_collector') #put here the name of the function/main
hdlr = logging.FileHandler(LOG_FILE)
formatter = logging.Formatter('%(asctime)s   %(name)-20s :  %(levelname)-8s %(message)s','%Y-%m-%d %H:%M:%S')
hdlr.setFormatter(formatter)
logger16.addHandler(hdlr)
logger16.setLevel(logging.WARNING)

logger17 = logging.getLogger('get_result_CEMM') #put here the name of the function/main
hdlr = logging.FileHandler(LOG_FILE)
formatter = logging.Formatter('%(asctime)s   %(name)-20s :  %(levelname)-8s %(message)s','%Y-%m-%d %H:%M:%S')
hdlr.setFormatter(formatter)
logger17.addHandler(hdlr)
logger17.setLevel(logging.WARNING)

logger18 = logging.getLogger('get_WMS_usermap') #put here the name of the function/main
hdlr = logging.FileHandler(LOG_FILE)
formatter = logging.Formatter('%(asctime)s   %(name)-20s :  %(levelname)-8s %(message)s','%Y-%m-%d %H:%M:%S')
hdlr.setFormatter(formatter)
logger18.addHandler(hdlr)
logger18.setLevel(logging.WARNING)

logger19 = logging.getLogger('get_LB_userstats') #put here the name of the function/main
hdlr = logging.FileHandler(LOG_FILE)
formatter = logging.Formatter('%(asctime)s   %(name)-20s :  %(levelname)-8s %(message)s','%Y-%m-%d %H:%M:%S')
hdlr.setFormatter(formatter)
logger19.addHandler(hdlr)
logger19.setLevel(logging.WARNING)

logger20 = logging.getLogger('map_user') #put here the name of the function/main
hdlr = logging.FileHandler(LOG_FILE)
formatter = logging.Formatter('%(asctime)s   %(name)-20s :  %(levelname)-8s %(message)s','%Y-%m-%d %H:%M:%S')
hdlr.setFormatter(formatter)
logger20.addHandler(hdlr)
logger20.setLevel(logging.WARNING)

logger21 = logging.getLogger('query_to_insert_user') #put here the name of the function/main
hdlr = logging.FileHandler(LOG_FILE)
formatter = logging.Formatter('%(asctime)s   %(name)-20s :  %(levelname)-8s %(message)s','%Y-%m-%d %H:%M:%S')
hdlr.setFormatter(formatter)
logger21.addHandler(hdlr)
logger21.setLevel(logging.WARNING)

logger22 = logging.getLogger('get_LB_CE_stats') #put here the name of the function/main
hdlr = logging.FileHandler(LOG_FILE)
formatter = logging.Formatter('%(asctime)s   %(name)-20s :  %(levelname)-8s %(message)s','%Y-%m-%d %H:%M:%S')
hdlr.setFormatter(formatter)
logger22.addHandler(hdlr)
logger22.setLevel(logging.WARNING)

logger23 = logging.getLogger('query_to_insert_CE') #put here the name of the function/main
hdlr = logging.FileHandler(LOG_FILE)
formatter = logging.Formatter('%(asctime)s   %(name)-20s :  %(levelname)-8s %(message)s','%Y-%m-%d %H:%M:%S')
hdlr.setFormatter(formatter)
logger23.addHandler(hdlr)
logger23.setLevel(logging.WARNING)

logger24 = logging.getLogger('update_user_tmp') #put here the name of the function/main
hdlr = logging.FileHandler(LOG_FILE)
formatter = logging.Formatter('%(asctime)s   %(name)-20s :  %(levelname)-8s %(message)s','%Y-%m-%d %H:%M:%S')
hdlr.setFormatter(formatter)
logger24.addHandler(hdlr)
logger24.setLevel(logging.WARNING)

logger25 = logging.getLogger('update_user_stats_table') #put here the name of the function/main
hdlr = logging.FileHandler(LOG_FILE)
formatter = logging.Formatter('%(asctime)s   %(name)-20s :  %(levelname)-8s %(message)s','%Y-%m-%d %H:%M:%S')
hdlr.setFormatter(formatter)
logger25.addHandler(hdlr)
logger25.setLevel(logging.WARNING)

logger26 = logging.getLogger('update_CE_stats_tmp') #put here the name of the function/main
hdlr = logging.FileHandler(LOG_FILE)
formatter = logging.Formatter('%(asctime)s   %(name)-20s :  %(levelname)-8s %(message)s','%Y-%m-%d %H:%M:%S')
hdlr.setFormatter(formatter)
logger26.addHandler(hdlr)
logger26.setLevel(logging.WARNING)

logger27 = logging.getLogger('update_CE_stats_table') #put here the name of the function/main
hdlr = logging.FileHandler(LOG_FILE)
formatter = logging.Formatter('%(asctime)s   %(name)-20s :  %(levelname)-8s %(message)s','%Y-%m-%d %H:%M:%S')
hdlr.setFormatter(formatter)
logger27.addHandler(hdlr)
logger27.setLevel(logging.WARNING)

logger28 = logging.getLogger('old_file_garbage_coll') #put here the name of the function/main
hdlr = logging.FileHandler(LOG_FILE)
formatter = logging.Formatter('%(asctime)s   %(name)-20s :  %(levelname)-8s %(message)s','%Y-%m-%d %H:%M:%S')
hdlr.setFormatter(formatter)
logger28.addHandler(hdlr)
logger28.setLevel(logging.WARNING)

logger29 = logging.getLogger('wms_balancing_arbiter') #put here the name of the function/main
hdlr = logging.FileHandler(LOG_FILE)
formatter = logging.Formatter('%(asctime)s   %(name)-20s :  %(levelname)-8s %(message)s','%Y-%m-%d %H:%M:%S')
hdlr.setFormatter(formatter)
logger29.addHandler(hdlr)
logger29.setLevel(logging.WARNING)


logger30 = logging.getLogger('collector_wms_class') #put here the name of the function/main
hdlr = logging.FileHandler(LOG_FILE)
formatter = logging.Formatter('%(asctime)s   %(name)-20s :  %(levelname)-8s %(message)s','%Y-%m-%d %H:%M:%S')
hdlr.setFormatter(formatter)
logger30.addHandler(hdlr)
logger30.setLevel(logging.WARNING)

logger31 = logging.getLogger('collector_lb_class') #put here the name of the function/main
hdlr = logging.FileHandler(LOG_FILE)
formatter = logging.Formatter('%(asctime)s   %(name)-20s :  %(levelname)-8s %(message)s','%Y-%m-%d %H:%M:%S')
hdlr.setFormatter(formatter)
logger31.addHandler(hdlr)
logger31.setLevel(logging.WARNING)

logger32 = logging.getLogger('host_usagetest_consumer') #put here the name of the function/main
hdlr = logging.FileHandler(LOG_FILE)
formatter = logging.Formatter('%(asctime)s   %(name)-20s :  %(levelname)-8s %(message)s','%Y-%m-%d %H:%M:%S')
hdlr.setFormatter(formatter)
logger32.addHandler(hdlr)
logger32.setLevel(logging.WARNING)

logger33 = logging.getLogger('activemq_consumer_wmsnagiostest') #put here the name of the function/main
hdlr = logging.FileHandler(LOG_FILE)
formatter = logging.Formatter('%(asctime)s   %(name)-20s :  %(levelname)-8s %(message)s','%Y-%m-%d %H:%M:%S')
hdlr.setFormatter(formatter)
logger33.addHandler(hdlr)
logger33.setLevel(logging.WARNING)



# define a Handler which writes INFO messages or higher to the sys.stderr
console = logging.StreamHandler()
console.setLevel(logging.WARNING)
# set a format which is simpler for console use
formatter = logging.Formatter('%(asctime)s   %(name)-20s :  %(levelname)-8s %(message)s','%Y-%m-%d %H:%M:%S')
#formatter = logging.Formatter('%(name)-20s: %(levelname)-8s %(message)s')
# tell the handler to use this format
console.setFormatter(formatter)
# add the handler to the root logger
logging.getLogger('').addHandler(console)
