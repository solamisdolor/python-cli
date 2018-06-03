from .base import base

class set(base):
    """Set property value. key = property key, value = property value."""
    
    @staticmethod
    def run(key, value):
        print ("setting key {0} to {1}".format(key, value))

