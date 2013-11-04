"""
Memcache client uisng hash_ring library
"""

import random
import string
from hash_ring import HashRing
import memcache
import cPickle as pickle

_DEAD_RETRY = 30  # number of seconds before retrying a dead server.
_SOCKET_TIMEOUT = 3  #  number of seconds before sockets timeout.

class MemcacheClient(memcache.Client):
    
    def __init__(self, servers, debug=0, pickleProtocol=0,
                 pickler=pickle.Pickler, unpickler=pickle.Unpickler,
                 pload=None, pid=None, server_max_key_length=250, server_max_value_length=1048576, 
                 dead_retry=30, socket_timeout=3, cache_cas=False, flush_on_reconnect=0, check_keys=True):
    	self._ring = HashRing(servers)
    	super(MemcacheClient, self).__init__(servers, debug, pickleProtocol,
                 pickler, unpickler,
                 pload, pid,
                 server_max_key_length, server_max_value_length,
                 dead_retry, socket_timeout,
                 cache_cas, flush_on_reconnect, check_keys)

    def _get_server(self, key):
        """ Current implementation of Memcache client
        """
        if self._ring:
        	node = self._ring.get_node(key)
        	server = memcache._Host(
            	node, self.debug, dead_retry=self.dead_retry,
            	socket_timeout=self.socket_timeout,
            	flush_on_reconnect=self.flush_on_reconnect)

        	
        	server.connect()
        else:
        	server, key = super(MemcacheClient, self)._get_server(key)
        return (server, key)

    def add_server(self, server):
        """ Adds a host at runtime to client
        """
        # Create a new host entry
        server = memcache._Host(
            server, self.debug, dead_retry=self.dead_retry,
            socket_timeout=self.socket_timeout,
            flush_on_reconnect=self.flush_on_reconnect
        )
        # Add this to our server choices 
        self.servers.append(server)
        # Update our buckets
        self.buckets.append(server)


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
    	# import pdb
    	# pdb.set_trace()
        client.set(key, 1)

    # Check how many keys come back 
    valid_keys = client.get_multi(keys)
    print '%s percent of keys matched' % ((len(valid_keys)/float(len(keys))) * 100)

    # We add another server...and pow!
    client.add_server('127.0.0.1:11218')
    print 'Added new server' 

    valid_keys = client.get_multi(keys)
    print '%s percent of keys stil matched' % ((len(valid_keys)/float(len(keys))) * 100)
