from .base import base
from .common import common

class get(base):
    """Get property value"""
    
    @staticmethod
    def run(key):
        print ("getting key {0}".format(key))
