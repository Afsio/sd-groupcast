'''
Arnau Montanes
Christian Zanger
01/05/2017 version 0.1
'''

class Member(object):
    _tell = ["multicast", "receive"]
    _ask = ["get_message"]

    def __init__(self, group, printer):
        self.group = group
        self.printer = printer
        self.queue = []
        self.message = []

    def multicast(self, message):
        for member in self.group.get_members():
            member.receive(message)

    def receive(self, message):
        self.queue.append(message)

    def get_message(self):
        #TODO: update to msg
        return self.queue
