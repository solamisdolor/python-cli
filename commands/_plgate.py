import json
import base64
import hashlib
import datetime
from urllib.parse import urlencode

class gateID(object):
    TEST_REGR="TEST_REGR"
    PWD_SCREENING="PWD_SCREENING"

class _plgate(object):
    """A gate"""
    
    def __init__(self, gate_id, value):
        self.id = gate_id
        self.value = value
        self.dtstamp = self.get_date_stamp()

    def get_date_stamp(self):
        return datetime.datetime.now().strftime("%Y.%m.%d.%H.%M.%S.%f") 

    def dumps(self):
        # s =  "|".join("{}.{}".format(key,val) for (key,val) in self.__dict__.items())
        # s = urlencode(self.__dict__)
        s = json.dumps(self.__dict__)
        return s

    def dumpbase64(self):
        return base64.urlsafe_b64encode(self.dumps().encode("utf-8"))

    def loadbase64(self, string):
        s = base64.urlsafe_b64decode(string).decode("utf-8")
        self.__dict__ = json.loads(s)

    def checksum(self):
        return hashlib.sha256(self.dumps().encode("utf-8")).hexdigest()

    def to_art_string(self, prefix=""):
        s = "properties="
        s += "{}{}={}".format(prefix, self.id, self.dumpbase64())
        s += ";{}{}_CHKSUM={}".format(prefix, self.id, self.checksum())
        return s


    def old_to_artifactory_string(self, prefix="", postfix=""):
        """
        /api/storage/{repoKey}/{itemPath}?properties=p1=v1[,v2][|p2=v3][&recursive=1]
        Returns the querystring part
        """
        s = "properties="
        s += "{}{}{}={}".format(prefix, self.id, postfix, self.value)
        s += ";{}{}_DTSTAMP{}={}".format(prefix, self.id, postfix, self.dtstamp)
        s += ";{}{}_CHKSUM{}={}".format(prefix, self.id, postfix, self.checksum())
        return s

    def from_artifactory_json(self):
        #TODO
        pass



class _plgateOverride(_plgate):
    """An override"""

    def __init__(self, gate_id=None, value=None, by=None):
        super(_plgateOverride, self).__init__(gate_id, value)
        self.by = by


    def to_art_string(self):
        s = super().to_art_string(prefix="_")
        return s

    def old_to_artifactory_string(self):
        s = super().to_artifactory_string(prefix="_")
        return s + ";{}{}_BY{}_{}".format("_", self.id, "", self.by)

