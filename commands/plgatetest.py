from .base import base
from ._plgate import _plgate, _plgateOverride, GateID, get_gate


class plgatetest(base):
    """plgate test"""
    
    @staticmethod
    def run():
        # Let's simulate an actual situation
        #
        # Something sets a gate
        # gate = _plgate(GateID.PLGATE_TEST_REGR, True, "system")


        # 1. pipeline requires to check gate status
        #
        gate, gate_ovr = get_gate(GateID.PLGATE_TEST_REGR, "lendfast", "646")

        # 2. check if there are any overrides
        gate = gate if gate_ovr is None else gate
        if gate.is_passed():
            # proceed!
            print("pass!")
            pass
        else:
            # return fail!
            print("fail!")
            pass



        exit(0)

        #ovr = _plgateOverride(GateID.TEST_REGR, "fail", "The boss")
        #print(ovr.pickles_64())

        #exit(0)
        #pickledstr = "gANjY29tbWFuZHMuX3BsZ2F0ZQpfcGxnYXRlT3ZlcnJpZGUKcQApgXEBfXECKFgCAAAAaWRxA1gJAAAAVEVTVF9SRUdScQRYBQAAAHZhbHVlcQVYBAAAAGZhaWxxBlgCAAAAYnlxB1gIAAAAVGhlIGJvc3NxCFgHAAAAZHRzdGFtcHEJWBoAAAAyMDE4LjA2LjE5LjE0LjIwLjAzLjE4ODg2MHEKdWJYQAAAAGNhZmM3NzQxMmMxMzNjNzIxNDE1ZDljODY5OTNjOTcyYWQyNzJlMThkNmE0N2Q2YzY4MGJlODMyMGZlNTc5ZDFxC4ZxDC4="

        pickledstr = "gANjY29tbWFuZHMuX3BsZ2F0ZQpfcGxnYXRlCnEAKYFxAX1xAihYAgAAAGlkcQNYCQAAAFRFU1RfUkVHUnEEWAUAAAB2YWx1ZXEFWAQAAABwYXNzcQZYAgAAAGJ5cQdYBgAAAHN5c3RlbXEIWAcAAABkdHN0YW1wcQlYGgAAADIwMTguMDYuMTkuMTMuNTQuNTkuMTkwMDY1cQp1YlhAAAAAZjYzMzhlNmJiYTQ4YzI3OWFiMWVmZWQ2ZDdjMzZhYjExYTM2Y2Q4MzI3ZDJlMGM2MmE2NjFlZDZkZDE2ZmIzOHELhnEMLg=="

        reload = _plgate.load_pickles_64(pickledstr)
        r_gate = reload[0]
        print (r_gate)
        print (r_gate.dumps())
        print (r_gate.to_art_string())
        #exit(0)


        gate = _plgate(GateID.TEST_REGR, "pass", "system")

        print (gate.dumps())
        print (gate.checksum())
        #print (gate.to_art_string())
        pickled = gate.pickles_64()
        print(pickled)

        reloaded_set = _plgate.load_pickles_64(pickled)
        reloaded_gate = reloaded_set[0]
        reloaded_checksum = reloaded_set[1]
        print (reloaded_gate.dumps())
        print (reloaded_checksum)


        exit(0)

        gate_override = _plgateOverride(gateID.TEST_REGR, "fail", "the overlord")

        print ("---override---")

        print (gate_override.dumps())
        print (gate_override.checksum())
        print (gate_override.to_art_string())

        print ("---using base64---")

        s = gate_override.dump_base64()
        print (s)
        reloaded = _plgateOverride.load_base64(s)
        print (reloaded.__dict__)
        print (reloaded.to_art_string())
