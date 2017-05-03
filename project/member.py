'''
Arnau Montanes
Christian Zanger
01/05/2017 version 0.2
'''

from pyactor.context import sleep

class Member(object):
    _tell = ["multicast", "receive"]
    _ask = ["get_message"]

    def __init__(self, group, printer, delay):
        self.group = group
        self.printer = printer
        self.queue = []
        self.message = []
        self.delay = delay

    def multicast(self, message):
        ts = self.group.get_sequencer().timestamp()
        sleep(self.delay)
        for member in self.group.get_members():
            member.receive(message, ts)

    def receive(self, message, seq):
        self.queue.append((message, seq))

    def get_message(self):
        #TODO: update to msg
        return sorted(self.queue, key=lambda tup: tup[1])
