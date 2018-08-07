import logging

from configobj import ConfigObj

logger = logging.getLogger('configLoader')
config = ConfigObj(infile = 'config.ini', write_empty_values = True)

try:
	f = open('config.ini')
	f.close()
except IOError as e:
	logger.critical('config.ini not found, token missing.')
	config['token'] = ''
	config['logid'] = ''
	config['owner'] = '180067685986467840'
	config.write()

class settings:
	token = config['token']
	logid = config['logid']
	owner = config['owner']