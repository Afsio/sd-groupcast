'''
Arnau Montanes
Christian Zanger
01/05/2017 version 0.1
'''

from pyactor.context import interval

class Group(object):
    _tell = ["join", "leave", "init_start", "update_membertime", "announce"]
    _ask = ["get_members"]

    #TODO: Ask if group only has to manage 1 group and not multiple
    def __init__(self, n, printer):
        self.group = {}
        self.n = n
        self.printer = printer

    def join(self, member_ref):
        self.group[member_ref] = 10

    def leave(self, member_ref):
        self.group.pop(member_ref)

    def get_members(self):
        return self.group.keys()

    def init_start(self):
        self.time = interval(self.host, 1, self.proxy, "update_membertime")

    def update_membertime(self):
        for member in self.group.keys():
            self.group[member] -= 1
            self.printer.printmsg(member.get_id() + " " + str(self.group[member]))
            if self.group[member] == 0:
                self.group.pop(member)
                # self.printer.printmsg(member.get_id() + " left!")

    def announce(self, member_ref):
        self.group[member_ref] = 10
