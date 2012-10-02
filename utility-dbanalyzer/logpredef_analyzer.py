import logging
import sys
import os

logger7 = logging.getLogger('db-analyzer') #put here the name of the function/main
hdlr = logging.FileHandler('/var/log/wmsmon-db-analyzer.log')
formatter = logging.Formatter('%(asctime)s   %(name)-20s :  %(levelname)-8s %(message)s','%Y-%m-%d %H:%M:%S')
hdlr.setFormatter(formatter)
logger7.addHandler(hdlr)
logger7.setLevel(logging.DEBUG)

logger8 = logging.getLogger('analyzer-utils') #put here the name of the function/main
hdlr = logging.FileHandler('/var/log/wmsmon-db-analyzer.log')
formatter = logging.Formatter('%(asctime)s   %(name)-20s :  %(levelname)-8s %(message)s','%Y-%m-%d %H:%M:%S')
hdlr.setFormatter(formatter)
logger8.addHandler(hdlr)
logger8.setLevel(logging.DEBUG)



# define a Handler which writes INFO messages or higher to the sys.stderr
console = logging.StreamHandler()
console.setLevel(logging.DEBUG)
# set a format which is simpler for console use
formatter = logging.Formatter('%(asctime)s   %(name)-20s :  %(levelname)-8s %(message)s','%Y-%m-%d %H:%M:%S')
#formatter = logging.Formatter('%(name)-20s: %(levelname)-8s %(message)s')
# tell the handler to use this format
console.setFormatter(formatter)
# add the handler to the root logger
logging.getLogger('').addHandler(console)
