import logging
from com.util.ConfigOptionUtil import *

def getLog():
    logFormate='%(name)s %(asctime)s %(levelname)s %(message)s'
    log=logging.getLogger(getConfigOption('log','name'))
    console=logging.FileHandler(getConfigOption('log','path'),'a')
    formatter=logging.Formatter(logFormate)
    console.setFormatter(formatter)
    log.addHandler(console)
    log.setLevel(logging.INFO)
    return log

              
if __name__=='__main__':
    log=getLog()
    log.debug('debug info ignored')
    log.info('info to let you track')
    log.error('error please notice')
    log.critical('critical serious problem occured')
