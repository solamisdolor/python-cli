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

        print (gate.to_artifactory_string())

        gate_override = _plgateOverride(gateID.TEST_REGR, "fail", "the overlord")

        print (gate_override.dumps())
        print (gate_override.checksum())