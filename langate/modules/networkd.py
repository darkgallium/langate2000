import sys, socket, struct
import pickle

class NetworkDaemonError(RuntimeError):
    """ every error originating from networkd raise this exception  """

def _send(sock, data):
    pack = struct.pack('>I', len(data)) + data
    sock.sendall(pack)

def _recv_bytes(sock, size):
    data = b''
    while len(data) < size:
        r = sock.recv(size - len(data))
        if not r:
            return None
        data += r
    return data

def _recv(sock):
    data_length_r = _recv_bytes(sock, 4)

    if not data_length_r:
        return None

    data_length = struct.unpack('>I', data_length_r)[0]
    return _recv_bytes(sock, data_length)


def communicate(payload):
    networkd_socket_file = "/var/run/langate2000-networkd.sock"

    with socket.socket(socket.AF_UNIX, socket.SOCK_STREAM) as sock:
        sock.connect(networkd_socket_file)
        r = pickle.dumps(payload)
        _send(sock, r)

        response_r = _recv(sock)
        response = pickle.loads(response_r)
        
        if response["success"]:
            return response
        
        else:
            raise NetworkDaemonError(response["message"])

def query(q, opts = {}):
    b = { "query": q }
    return communicate({ **b, **opts })
