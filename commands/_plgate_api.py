from ._plgate import _plgate, _plgateOverride
from requests import exceptions


class MismatchedLinksError(Exception):
    def __init__(self, stored_links, expected_links):
        super().__init__("Links in stored gate does not match expected. Expected:{}, Stored:{}".format(expected_links, stored_links))


def load_consolidated_gate(gate_id, repokey, itempath, artiuser, artipwd):
    gate, gate_ovr = get_gates(gate_id, repokey, itempath, artiuser, artipwd)
    return gate if gate_ovr is None else gate_ovr

def get_gates(gate_id, repokey, itempath, artiuser, artipwd):
    # get normal gate
    gate = load_gate(gate_id, repokey, itempath, artiuser, artipwd)
    # find overrides
    gate_ovr = None
    try:
        gate_ovr = load_gate("_" + gate_id, repokey, itempath, artiuser, artipwd)
    except exceptions.HTTPError as e:
        if not e.response.status_code == 404:
            raise e # else no overrides found
    except:
        raise
    return gate, gate_ovr

def load_gate(gate_storage_key, repokey, itempath, artiuser, artipwd):
    """Load gate from storage.
    Also checks if the links match expected, 
    i.e. if this gate was made for the specific repokey/itempath.
    """
    storage_value = _artifactory.get(artiuser, artipwd, repokey, itempath, gate_storage_key)
    gate =  _plgate.loads(storage_value)
    expected_links = (repokey, itempath)
    stored_links = gate.links[0]
    if not stored_links == expected_links:
        raise MismatchedLinksError(stored_links, expected_links)
    return _plgate.loads(storage_value)

def save_gate(gate: _plgate, repokey, itempath, artiuser, artipwd):
    """Save gate to storage"""
    gate.links.append((repokey, itempath))
    return _artifactory.set(artiuser, artipwd, repokey, itempath, gate.storage_key(), gate.storage_value())
