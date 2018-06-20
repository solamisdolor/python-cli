from .base import base
from ._plgate import _plgate, _plgateOverride, GateID
from ._plgate_api import get_gates, save_gate, load_consolidated_gate, load_gate

class plgate(base):
    """plgate test"""
    
    @staticmethod
    def run():
        # plgate.simulate_actual()
        # plgate.test_old_pickle()
        # plgate.test_loads()
        plgate.test_save()
        # plgate.test_load()
        plgate.test_save_ovr()
        plgate.test_load_consolidated()

    @staticmethod
    def test_load_consolidated():
        gate = load_consolidated_gate(GateID.PLGATE_TEST_REGR, 'local-ing-lendfast-pipeline-release', '646', 'bobthebuilder', 'dizzysc00p')
        print(gate.dump_pretty())
        print(gate.dump_jsons())
        print(gate)

    @staticmethod
    def test_load():
        gate: _plgate
        gate = load_gate(GateID.PLGATE_TEST_REGR, 'local-ing-lendfast-pipeline-release', '646', 'bobthebuilder', 'dizzysc00p')
        print(gate.dump_pretty())

    @staticmethod
    def test_save():
        gate: _plgate
        gate = _plgate(GateID.PLGATE_TEST_REGR, False, "system")
        save_gate(gate, 'local-ing-lendfast-pipeline-release', '646', 'bobthebuilder', 'dizzysc00p')

    @staticmethod
    def test_save_ovr():
        gate_ovr = _plgateOverride(GateID.PLGATE_TEST_REGR, False, "Mr Big Shot")
        save_gate(gate_ovr, 'local-ing-lendfast-pipeline-release', '646', 'bobthebuilder', 'dizzysc00p')

    @staticmethod
    def test_loads():
        gate: _plgate
        saved_pickle = "gANjY29tbWFuZHMuX3BsZ2F0ZQpfcGxnYXRlCnEAKYFxAX1xAihYAgAAAGlkcQNYEAAAAFBMR0FURV9URVNUX1JFR1JxBFgFAAAAdmFsdWVxBYlYAgAAAGJ5cQZYBgAAAHN5c3RlbXEHWAcAAABkdHN0YW1wcQhYGgAAADIwMTguMDYuMTkuMTcuNTcuMTYuNzQ5OTY0cQl1YlhAAAAAN2Y3NDdlNzA0NTdlMTk4OTk5NjA0ZDAzZmZmZmJjMThjNmNiYzdmMDYwZmJlZDA4MzExMzlhZGI5ZTZjZDFjMHEKhnELLg=="
        gate = _plgate.loads(saved_pickle)
        print(gate.dump_pretty())

        saved_pickle = "gANjY29tbWFuZHMuX3BsZ2F0ZQpfcGxnYXRlT3ZlcnJpZGUKcQApgXEBfXECKFgCAAAAaWRxA1gQAAAAUExHQVRFX1RFU1RfUkVHUnEEWAUAAAB2YWx1ZXEFiFgCAAAAYnlxBlgKAAAAQWxsIE1pZ2h0eXEHWAcAAABkdHN0YW1wcQhYGgAAADIwMTguMDYuMTkuMTcuNTcuMTYuNzUwMjQ4cQl1YlhAAAAAMWJiMTVmNGYxMTM4ZmZjN2E5YjMxMTJjYTc1NWYzMDlmMzc2YzlkMjZiNDMyMTIwMjhiNzViMmVjN2MxMDNmYXEKhnELLg=="
        gate = _plgate.loads(saved_pickle)
        print(gate.dump_pretty())

    @staticmethod
    def test_old_pickle():
        saved_pickle = "gANjY29tbWFuZHMuX3BsZ2F0ZQpfcGxnYXRlCnEAKYFxAX1xAihYAgAAAGlkcQNYEAAAAFBMR0FURV9URVNUX1JFR1JxBFgFAAAAdmFsdWVxBYlYAgAAAGJ5cQZYBgAAAHN5c3RlbXEHWAcAAABkdHN0YW1wcQhYGgAAADIwMTguMDYuMTkuMTcuNTcuMTYuNzQ5OTY0cQl1YlhAAAAAN2Y3NDdlNzA0NTdlMTk4OTk5NjA0ZDAzZmZmZmJjMThjNmNiYzdmMDYwZmJlZDA4MzExMzlhZGI5ZTZjZDFjMHEKhnELLg=="
        saved_override_pickle = "gANjY29tbWFuZHMuX3BsZ2F0ZQpfcGxnYXRlT3ZlcnJpZGUKcQApgXEBfXECKFgCAAAAaWRxA1gQAAAAUExHQVRFX1RFU1RfUkVHUnEEWAUAAAB2YWx1ZXEFiFgCAAAAYnlxBlgKAAAAQWxsIE1pZ2h0eXEHWAcAAABkdHN0YW1wcQhYGgAAADIwMTguMDYuMTkuMTcuNTcuMTYuNzUwMjQ4cQl1YlhAAAAAMWJiMTVmNGYxMTM4ZmZjN2E5YjMxMTJjYTc1NWYzMDlmMzc2YzlkMjZiNDMyMTIwMjhiNzViMmVjN2MxMDNmYXEKhnELLg=="

        saved_gate, chksum = _plgate.load_pickles_64(saved_pickle)
        saved_override_gate, chksumovr = _plgate.load_pickles_64(saved_override_pickle)

        print(saved_gate.dump_jsons())

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
