import logging
import sys

from configobj import ConfigObj

logger = logging.getLogger('configLoader')
config = ConfigObj(infile = 'config.ini', write_empty_values = True)

try:
  f = open('config.ini')
  f.close()
except IOError as e:
  f = open('config.ini', 'w+')
  f.close()
  
  logger.critical('config.ini not found, token missing.')
  config['token'] = ''
  config['logid'] = ''
  config['owner'] = '180067685986467840'
  config.write()
  sys.exit()

class settings:
  token = config['token']
  logid = config['logid']
  owner = config['owner']