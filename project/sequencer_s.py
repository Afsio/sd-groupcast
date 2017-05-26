'''
Arnau Montanes
Christian Zanger
01/05/2017 version 0.2
'''

from pyactor.context import interval
from pyactor.exceptions import TimeoutError


class Sequencer(object):
    _tell = []
    _ask = ["timestamp"]

    def __init__(self):
        self.seq = -1

    def timestamp(self):
        self.seq += 1
        return self.seq


class BullySequencer(Sequencer):
    _tell = ["init_start", "s_fail", "s_recover", "recieve",
             "become_coordinator"]
    _ask = ["timestamp", "election"]

    def __init__(self, iden, g, p, n=1):
        self.seq = -1
        self.iden = iden
        self.all = []
        self.state = " "
        self.coord = -1
        self.n = n
        self.group = g
        self.printer = p

    def init_start(self, sequencers):
        self.all = sequencers
        if self.iden == len(self.all) - 1:
            self.become_coordinator()
        else:
            self.state = "Sequencer"
            # self.printer.printmsg("Sequencer: " + str(self.iden))
            i = 0
            sempais = 0
            while i < len(self.all):
                if self.iden < i:
                    try:
                        # self.printer.printmsg("Enviant eleccio")
                        self.all[i].election(self.iden)
                        sempais += 1
                        # self.printer.printmsg("Eleccio enviada")
                    except TimeoutError:
                        # self.printer.printmsg("Coordinator no respon")
                        pass
                i += 1
            if sempais == 0:
                self.become_coordinator()

    def become_coordinator(self):
        self.state = "Coordinator"
        for s in self.all:
            s.recieve("Victory", self.iden)
        self.coord = self.iden
        self.group.update_coordinator(self.iden)

    def election(self, iden):
        if self.state != "Failed":
            self.all[iden].recieve("Active", self.iden)
        else:
            raise TimeoutError("Coordinator not responding")

    def recieve(self, m, iden):
        if self.state != "Failed":
            if m == "Victory":
                self.coord = iden
            if m == "Fail" or m == "Recover":
                self.init_start(self.all)
            if m == "Active":
                pass
            if m == "Timestamp":
                self.seq = iden

    def s_fail(self):
        #  Auxiliar method to force TimeoutErrors
        self.state = "Failed"
        for s in self.all:
            s.recieve("Fail", self.iden)

    def s_recover(self):
        self.state = "Sequencer"
        for s in self.all:
            s.recieve("Recover", self.iden)

    def timestamp(self):
        self.seq += 1
        for s in self.all:
            s.recieve("Timestamp", self.seq)
        return self.seq
