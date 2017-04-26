'''
Arnau Montanes
Christian Zanger
28/02/2017 version 1.2
'''

from random import sample
from pyactor.context import interval


class Tracker(object):
    _tell = ["announce", "init_start", "update_peertime", "attach_printer"]
    _ask = ["get_peers", "get_protocol"]
    _ref = ["announce", "get_peers", "attach_printer"]

    def __init__(self, n, protocol_type):
        self.swarms = {}
        self.n = n
        self.protocol_type = protocol_type

    def init_start(self):
        self.time = interval(self.host, 1, self.proxy, "update_peertime")

    def announce(self, torrent_hash, peer_ref):
        if torrent_hash in self.swarms:
            if peer_ref not in self.swarms[torrent_hash]:
                self.swarms[torrent_hash].update({peer_ref: 10})
            else:
                self.swarms[torrent_hash][peer_ref] = 10
        else:
            self.swarms[torrent_hash] = {peer_ref: 10}

    def get_peers(self, torrent_hash):
        try:
            peers = sample(self.swarms[torrent_hash], self.n)
            return peers
        except ValueError:
            return self.swarms[torrent_hash].keys()
        except KeyError:
            return []

    def update_peertime(self):
        for torrent_hash in self.swarms:
            to_delete = []

            for peer in self.swarms[torrent_hash]:
                self.swarms[torrent_hash][peer] -= 1
                if self.swarms[torrent_hash][peer] == 0:
                    to_delete.append(peer)

            for idle in to_delete:
                self.swarms[torrent_hash].pop(idle)

    def attach_printer(self, printer):
        self.printer = printer

    def get_protocol(self):
        return self.protocol_type
