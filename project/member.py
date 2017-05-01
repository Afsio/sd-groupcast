'''
Arnau Montanes
Christian Zanger
01/05/2017 version 0.1
'''

class Member(object):
    _tell = ["multicast", "receive"]

    def __init__(self, group, printer):
        self.group = group
        self.printer = printer
        self.queue = []

    def multicast(self, message):
        for member in self.group:
            member.receive(message)

    def receive(self, message):
        self.queue.append(message)
