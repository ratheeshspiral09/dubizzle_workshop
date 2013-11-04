"""
This is a simple script that uses the pylibmc library to test the performace after adding new server
"""

import pylibmc
import random
import string

class MemcacheClient(object):
    """  
    Memchache client class

    This class composit a client instance created from the pylibmc library and it only implements the set and get_multi functions
    for the purpose of this task.
    """
    def __init__(self, servers):
    	"""
    	Initialize the client with a set of servers
    	"""
    	self._servers = self._convert_servers(servers)
    	self._client = pylibmc.Client(servers=self._servers,
    		binary=True,
    		behaviors={'tcp_nodelay': True,
    		'ketama': True})

    def _convert_servers(self, servers):
    	"""
    	Converts a list of servers in the formate of ['server1:port1', ...] to a list of 
    	tuples [(1, 'server1', port), ...] to match pylibmc format 
    	"""
    	formated_servers = list()
    	for server in servers:
    		server, port = server.split(":")
    		formated_servers.append((1, server, int(port)))

    	return formated_servers

    def add_server(self, server):
        """ Adds a host at runtime to client
        """
        self._servers.append(self._convert_servers([server])[0])
        self._client = pylibmc.Client(servers=self._servers,
    		binary=True,
    		behaviors={'tcp_nodelay': True,
    		'ketama': True}) 

    def set(self, key, value):
    	"""
    	Set function
    	"""
    	return self._client.set(key, value)

    def get_multi(self, keys):
    	"""
    	Gets mulitple keys
    	"""
    	return self._client.get_multi(keys)

def random_key(size):
    """ Generates a random key
    """
    return ''.join(random.choice(string.letters) for _ in range(size))

if __name__ == '__main__':
    # We have 7 running memcached servers
    servers = ['127.0.0.1:1121%d' % i for i in range(1,8)]
    # We have 100 keys to split across our servers
    keys = [random_key(10) for i in range(100)]
    # Init our subclass
    client = MemcacheClient(servers=servers)
    # Distribute the keys on our servers
    for key in keys:
        client.set(key, 1)

    # Check how many keys come back 
    valid_keys = client.get_multi(keys)
    print '%s percent of keys matched' % ((len(valid_keys)/float(len(keys))) * 100)

    # We add another server...and pow! not anymore!
    client.add_server('127.0.0.1:11218')
    print 'Added new server' 

    valid_keys = client.get_multi(keys)
    print '%s percent of keys stil matched' % ((len(valid_keys)/float(len(keys))) * 100)
