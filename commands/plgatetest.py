from .base import base
from ._plgate import _plgate, _plgateOverride, GateID, get_gates, save_gate


class plgatetest(base):
    """plgate test"""
    
    @staticmethod
    def run():
        # plgatetest.simulate_actual()
        plgatetest.test_old_pickle()

    @staticmethod
    def test_old_pickle():
        saved_pickle = "gANjY29tbWFuZHMuX3BsZ2F0ZQpfcGxnYXRlCnEAKYFxAX1xAihYAgAAAGlkcQNYEAAAAFBMR0FURV9URVNUX1JFR1JxBFgFAAAAdmFsdWVxBYlYAgAAAGJ5cQZYBgAAAHN5c3RlbXEHWAcAAABkdHN0YW1wcQhYGgAAADIwMTguMDYuMTkuMTcuNTcuMTYuNzQ5OTY0cQl1YlhAAAAAN2Y3NDdlNzA0NTdlMTk4OTk5NjA0ZDAzZmZmZmJjMThjNmNiYzdmMDYwZmJlZDA4MzExMzlhZGI5ZTZjZDFjMHEKhnELLg=="
        saved_override_pickle = "gANjY29tbWFuZHMuX3BsZ2F0ZQpfcGxnYXRlT3ZlcnJpZGUKcQApgXEBfXECKFgCAAAAaWRxA1gQAAAAUExHQVRFX1RFU1RfUkVHUnEEWAUAAAB2YWx1ZXEFiFgCAAAAYnlxBlgKAAAAQWxsIE1pZ2h0eXEHWAcAAABkdHN0YW1wcQhYGgAAADIwMTguMDYuMTkuMTcuNTcuMTYuNzUwMjQ4cQl1YlhAAAAAMWJiMTVmNGYxMTM4ZmZjN2E5YjMxMTJjYTc1NWYzMDlmMzc2YzlkMjZiNDMyMTIwMjhiNzViMmVjN2MxMDNmYXEKhnELLg=="

        saved_gate, chksum = _plgate.load_pickles_64(saved_pickle)
        saved_override_gate, chksumovr = _plgate.load_pickles_64(saved_override_pickle)

        print(saved_gate.dumps())

        pass

    @staticmethod
    def simulate_actual():
        # Let's simulate an actual situation
        #
        # 0. Something sets a gate
        gate = _plgate(GateID.PLGATE_TEST_REGR, False, "system")
        saved_pickle = save_gate(gate, "lendfast", "646")


        # 1. pipeline requires to check gate status
        #
        loaded_gate:_plgate
        loaded_gate, chksum = _plgate.load_pickles_64(saved_pickle)

        print(loaded_gate.is_passed())

        # 2. then someone overrides the value
        #
        gate = _plgateOverride(GateID.PLGATE_TEST_REGR, True, "All Mighty")
        saved_override_pickle = save_gate(gate, "lendfast", "646")

        # 3. pipeline is checking gate status
        #
        loaded_gate, chksum = _plgate.load_pickles_64(saved_pickle)
        loaded_gate_ovr, chksum_ovr = _plgate.load_pickles_64(saved_override_pickle)
        gate = loaded_gate_ovr if not loaded_gate_ovr is None else loaded_gate

        print(gate.is_passed())

        print(saved_pickle)
        print("-----")
        print(saved_override_pickle)

        exit(0)
