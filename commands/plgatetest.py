from .base import base
from ._plgate import _plgate, _plgateOverride, gateID

from urllib.parse import urlencode

class plgatetest(base):
    """plgate test"""
    
    @staticmethod
    def run():
        
        gate = _plgate(gateID.TEST_REGR, "pass")

        print (gate.dumps())
        print (gate.checksum())
        print (gate.to_art_string())

        gate_override = _plgateOverride(gateID.TEST_REGR, "fail", "the overlord")

        print ("---override---")

        print (gate_override.dumps())
        print (gate_override.checksum())
        print (gate_override.to_art_string())

        print ("---using base64---")

        s = gate_override.dumpbase64()
        print (s)
        reloaded = _plgateOverride()
        reloaded.loadbase64(s)
        print (reloaded.__dict__)
        print (reloaded.to_art_string())
