'''
Arnau Montanes
Christian Zanger
01/05/2017 version 0.7
'''

from pyactor.context import interval


class Group(object):
    _tell = ['join', 'leave', 'init_start', 'update_membertime', 'announce',
             'attach_sequencers', 'monitor', 'update_coordinator', 'announce']
    _ask = ['get_members', 'get_sequencer', 'get_members_ids']
    _ref = ['join', 'leave', 'attach_sequencer', 'get_sequencer', 'announce',
            'get_members']

    def __init__(self, printer):
        self.group = {}
        self.printer = printer
        self.coordinator = None
        self.sequenfcers = []
        self.ids = []

    def join(self, member_ref, iden=0):
        self.group[member_ref] = 10
        # self.ids.append(iden)
        self.ids.append(member_ref.get_id())

    def leave(self, member_ref):
        self.group.pop(member_ref)

    def announce(self, member_ref):
        if member_ref in self.group:
            self.printer.printmsg("hola")
        # self.printer.printmsg(member_ref + " announced." )
        # self.group[member_ref] = 30

    def get_members(self):
        return self.group.keys()

    def attach_sequencers(self, seq):
        self.sequencers = seq

    def get_sequencer(self):
        return self.coordinator

    def update_coordinator(self, c):
        self.coordinator = self.sequencers[c]

    def get_members_ids(self):
        return self.ids

    def init_start(self):
        self.time = interval(self.host, 1, self.proxy, 'update_membertime')

    def update_membertime(self):
        for member in self.group.keys():
            self.group[member] -= 1
            if self.group[member] == 0:
                self.printer.printmsg(member.get_id() + ' left!')
                self.leave(member)
