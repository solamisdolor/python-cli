import json
import base64
import hashlib
import datetime
import pickle


class GateID(object):
    PLGATE_TEST_REGR = "PLGATE_TEST_REGR"
    PLGATE_PWD_SCREENING = "PLGATE_PWD_SCREENING"
    PLGATE_STAGING_SIGNOFF = "PLGATE_STAGING_SIGNOFF"
    PLGATE_PRE_PROD_SIGNOFF = "PLGATE_PRE_PROD_SIGNOFF"


class InvalidChecksumError(Exception):
    pass


class _plgate(object):
    """A gate.

    Args:
        gate_id (str): ID of the Gate. Should be from GateID attributes.
        value (bool): Value of the Gate. Should be True/False.
        by (str): User/service name associated with this change.

    Attributes:
        id (str): ID of the Gate.
        value (bool): Value of the Gate.
        by (str): User/service name associated with this change.
        dtstamp (str): Dynamically created string representation of date time stamp.
        links ([]): List of objects linked to this gate.
    """
    
    def __init__(self, gate_id, value, by):
        self.id = gate_id
        self.value = value
        self.by = by
        self.dtstamp = _plgate._get_date_stamp()
        self.links = [] # set this just before saving to storage

    @staticmethod
    def _date_fmt():
        return "%Y.%m.%d.%H.%M.%S.%f"

    @staticmethod
    def _get_date_stamp():
        return datetime.datetime.now().strftime(_plgate._date_fmt())

    def is_passed(self):
        return True if self.value in [True, "True", "true"] else False

    def dump_pretty(self):
        dt = datetime.datetime.strptime(self.dtstamp, _plgate._date_fmt())
        dt_str = dt.strftime("%A %d %B %Y, %I:%M %p ")
        return "Gate {} is set to {} by {} on {} for {}".format(self.id, self.value, self.by, dt_str, self.links)

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

    def storage_key(self):
        """use this to represent the gate's identity when storing in a DB"""
        return self.id

    def storage_value(self):
        return self.dumps()


class _plgateOverride(_plgate):
    """An override"""

    def __init__(self, gate_id, value, by):
        super().__init__(gate_id, value, by)
        self.is_override = True

    def to_art_string(self):
        s = super().to_art_string(prefix="_")
        return s

    def dump_pretty(self):
        s = super().dump_pretty()
        return "[OVERRIDE] {}".format(s)

    def storage_key(self):
        return "_" + super().storage_key()

