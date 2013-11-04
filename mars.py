"""
i) Contains a class "Mars" with atleast the following methods:
        - "__init__" : initialize what you feel neccessary
        - "send" : (over)writes a JSON object to a file. Takes in one argument of type
          dict. Returns 1 on success. Raises a general exception on error.
       - "receive" : reads a JSON object from a file. Returns a dict on success.
         Raises a general exception on error.
    ii) If run on the command line, a test of the above methods should be displayed with appropriate output
    iii) Class should be importable by other modules
    iv) Must work with Python 2.6
    v) Must meet PEP-8 specifications
    vi) Must be in one file
"""
import os
import simplejson

class Mars(object):
    """
    Class represnts Mars objects
    """

    def __init__(self, data_location=None):
        """
        Initialize Mars objects

        @param data_location:           Path to the data directory to use to load and dump the objects
        @type data_location:            String
        """
        if data_location is None:
            self._data_location = os.path.join(os.path.dirname(__file__),
             'data')
            os.mkdir(self._data_location)
        elif not os.path.exists(data_location):
            raise RuntimeError("Data dir [%s] does not exist" % data_location)
        else:
            self._data_location = data_location
        self._data_file_path = os.path.join(self._data_location, 'data.dat')

    def send(self, data):
        """
        (over)writes a JSON object to a file. Takes in one argument of type
          dict. Returns 1 on success. Raises a general exception on error.

        @param data:                    Data as dictionary
        @type data:                     Dictionary

        @return:                        1 on success
        """
        try:
            simplejson.dump(data, open(self._data_file_path, 'wb'))
        except Exception, ex:
            raise RuntimeError('Failed to send object to the store.\
 Reason [%s]' % str(ex))
        return 1

    def receive(self):
        """
        Reads a JSON object from a file. Returns a dict on success.
         Raises a general exception on error.

        @return:                    Dictonary representing the data
        """
        try:
            return simplejson.load(open(self._data_file_path, 'rb'))
        except Exception, ex:
            raise RuntimeError('Failed to read object from the store.\
Reason [%s]' % str(ex))



def test():
    """
    Test function
    """
    data = {'key': 'value'}
    mars_obj = Mars()
    print 'Sending data %s to the store' % data
    if mars_obj.send(data) == 1:
        print 'Data is sent'
    print 'Reading data from the store'
    data = mars_obj.receive()
    print 'Received the following data from the store: %s' % data

if __name__ == '__main__':
    test() 