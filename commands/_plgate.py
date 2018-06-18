import json
import hashlib
import datetime
from urllib.parse import urlencode

class gateID(object):
    TEST_REGR="TEST_REGR"
    PWD_SCREENING="PWD_SCREENING"

class _plgate(object):
    """A gate"""
    
    def __init__(self, id, value):
        self.id = id
        self.value = value
        self.dtstamp = self.get_date_stamp()

    def get_date_stamp(self):
        return datetime.datetime.now().strftime("%Y.%m.%d.%H.%M.%S.%f") 

    def dumps(self):
        #s =  "|".join("{}.{}".format(key,val) for (key,val) in self.__dict__.items())        
        s = urlencode(self.__dict__)
        return s

    def checksum(self):
        return hashlib.sha256(self.dumps().encode("utf-8")).hexdigest()

    def to_artifactory_string(self):
        """
        /api/storage/{repoKey}/{itemPath}?properties=p1=v1[,v2][|p2=v3][&recursive=1]
        Returns the querystring part
        """
        s="properties="
        s += "{}={};".format(self.id, self.value)
        s += "{}_DTSTAMP={};".format(self.id, self.dtstamp)
        s += "{}_CHKSUM={}".format(self.id, self.checksum())
        return s

    def from_artifactory_string(self):
        #TODO
        pass



class _plgateOverride(_plgate):
    """An override"""

    def __init__(self, id, value, made_by):
        super(_plgateOverride, self).__init__(id, value)
        self.made_by = made_by

    