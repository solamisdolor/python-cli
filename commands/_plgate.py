import json
import base64
import hashlib
import datetime
import pickle


class GateID(object):
    PLGATE_TEST_REGR = "PLGATE_TEST_REGR"
    PLGATE_PWD_SCREENING = "PLGATE_PWD_SCREENING"
    PLGATE_STAGING_SIGNOFF = "PLGATE_STAGING_SIGNOFF"


class InvalidChecksumError(Exception):
    pass


class _plgate(object):
    """A gate"""
    
    def __init__(self, gate_id, value, by):
        self.id = gate_id
        self.value = value
        self.by = by
        self.dtstamp = _plgate._get_date_stamp()

    @staticmethod
    def _date_fmt():
        return "%Y.%m.%d.%H.%M.%S.%f"

    @staticmethod
    def _get_date_stamp():
        return datetime.datetime.now().strftime(_plgate._date_fmt())

    def is_passed(self):
        return True if self.value is True else False

    def dump_pretty(self):
        dt = datetime.datetime.strptime(self.dtstamp, _plgate._date_fmt())
        dt_str = dt.strftime("%A %d %B %Y, %I:%M %p ")
        return "Gate {} is set to {} by {} on {}".format(self.id, self.value, self.by, dt_str)

    def dump_jsons(self):
        return json.dumps(self.__dict__)

    def dumps(self):
        return self.pickles_64()

    def pickles_64(self) -> str:
        """returns url-safe utf-8 base64-encoded pickle of a tuple of (gate, checksum)"""
        the_tuple = (self, self.checksum())
        b = pickle.dumps(the_tuple)
        return base64.urlsafe_b64encode(b).decode("utf-8")

    @staticmethod
    def load_pickles_64(string: str) -> tuple:
        """returns a tuple of (gate, checksum) from a utf-8 base64-encoded pickle"""
        b = base64.urlsafe_b64decode(string.encode("utf-8"))
        gate, checksum = pickle.loads(b)
        return gate, checksum

    @staticmethod
    def loads(string: str) -> object:
        """returns a gate instance from a utf-8 base64-encoded pickle, if checksum is valid"""
        gate, checksum = _plgate.load_pickles_64(string)
        if _plgate.is_valid_checksum(gate, checksum):
            return gate
        else:
            raise InvalidChecksumError()

    @staticmethod
    def is_valid_checksum(gate, checksum):
        return True if gate.checksum() == checksum else False

    def checksum(self):
        return hashlib.sha256(self.dump_jsons().encode("utf-8")).hexdigest()

    def to_art_string(self, prefix=""):
        s = "properties="
        s += "{}{}={}".format(prefix, self.id, self.pickles_64())
        return s

    def from_artifactory_json(self):
        #TODO: implement this
        pass


class _plgateOverride(_plgate):
    """An override"""

    def to_art_string(self):
        s = super().to_art_string(prefix="_")
        return s

    def dump_pretty(self):
        s = super().dump_pretty()
        return "[OVERRIDE] {}".format(s)


def get_gates(gate_id, repokey, itempath):
    # 1. fetch property gate_id from artifactory/repokey/itempath
    # 2. load

    # TODO: replace below with actual value from Artifactory
    property_value = "gANjY29tbWFuZHMuX3BsZ2F0ZQpfcGxnYXRlCnEAKYFxAX1xAihYAgAAAGlkcQNYCQAAAFRFU1RfUkVHUnEEWAUAAAB2YWx1ZXEFWAQAAABwYXNzcQZYAgAAAGJ5cQdYBgAAAHN5c3RlbXEIWAcAAABkdHN0YW1wcQlYGgAAADIwMTguMDYuMTkuMTMuNTQuNTkuMTkwMDY1cQp1YlhAAAAAZjYzMzhlNmJiYTQ4YzI3OWFiMWVmZWQ2ZDdjMzZhYjExYTM2Y2Q4MzI3ZDJlMGM2MmE2NjFlZDZkZDE2ZmIzOHELhnEMLg=="
    gate = _plgate.loads(property_value)

    # 3. find overrides

    # TODO: fetch property _gate_id from Artifactory
    property_value = "gANjY29tbWFuZHMuX3BsZ2F0ZQpfcGxnYXRlT3ZlcnJpZGUKcQApgXEBfXECKFgCAAAAaWRxA1gJAAAAVEVTVF9SRUdScQRYBQAAAHZhbHVlcQVYBAAAAGZhaWxxBlgCAAAAYnlxB1gIAAAAVGhlIGJvc3NxCFgHAAAAZHRzdGFtcHEJWBoAAAAyMDE4LjA2LjE5LjE0LjIwLjAzLjE4ODg2MHEKdWJYQAAAAGNhZmM3NzQxMmMxMzNjNzIxNDE1ZDljODY5OTNjOTcyYWQyNzJlMThkNmE0N2Q2YzY4MGJlODMyMGZlNTc5ZDFxC4ZxDC4="
    gate_ovr = _plgate.loads(property_value)
    
    return gate, gate_ovr

def save_gate(gate: _plgate, repokey, itempath):
    """Save gate"""
    print("saving gate {0}".format(gate.id))
    return gate.pickles_64()
    # TODO: actually implement this.

def reset_gate(gate_id, repokey, itempath):
    """Deletes the gate for the specified repokey and itempath"""
    print("deleting gate {0}".format(gate_id))
    # TODO: actually implement this.
