from configobj import ConfigObj


config = ConfigObj(infile = 'config/config.ini', write_empty_values = True)

class settings:
	token = config['token']
	logid = config['logid']
	owner = config['owner']