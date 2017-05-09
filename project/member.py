'''
Arnau Montanes
Christian Zanger
01/05/2017 version 0.3
'''

from pyactor.context import sleep

class Member(object):
    _tell = ["multicast", "receive"]
    _ask = ["get_message", "get_queue"]

    def __init__(self, group, printer, delay=0):
        self.group = group
        self.printer = printer
        self.queue = []
        self.delay = delay

    def multicast(self, message):
        ts = self.group.get_sequencer().timestamp()
        sleep(self.delay)
        for member in self.group.get_members():
            member.receive(message, ts)

    def receive(self, message, seq):
        self.queue.append((message, seq))

    def get_queue(self):
        return self.queue

    def get_message(self):
        return sorted(self.queue, key=lambda tup: tup[1])

class LamportMember(Member):
    _tell = ["multicast", "receive"]
    _ask = ["get_message", "get_queue"]

    def __init__(self, group, printer, identifier):
        self.group = group
        self.printer = printer
        self.queue = []
        self.ready = []
        self.clock = 0
        self.iden = identifier
        self.num_mes = 0

    def multicast(self, message):
        for member in self.group.get_members():
            member.receive(message, self.clock, self.iden)
        self.clock += 1

    def receive(self, message, ts, iden):
        if message != "ACK":
            #If m recieved, append to queue and sort according to timestamp
            self.queue.append((message, ts, iden))
            self.queue.sort(key=lambda tup: tup[1])
            self.num_mes += 1
            #Then, ack everybody
            self.multicast("ACK")
        else:
            #When ack recieved, append to queue and sort according to timestamp
            self.queue.append(("ACK", ts, iden))
            self.queue.sort(key=lambda tup: tup[1])

    def get_message(self):
        j = 0
        while j < self.num_mes:
            first = self.queue[0]
            if first == "ACK":
                #If first element is ack it means it is for a message not sent to this member. Remove.
                del self.queue[0]
            else:
                #If first element is m, search for ack of all members
                for member in self.group.get_members_ids():
                    out_tup = [m for m in self.queue if m[0] == "ACK" and m[2] == member]
                    if out_tup != []:
                        #If list has all the ack, remove it and continue
                        for i in out_tup:
                            self.queue.remove(i)
                #If message is ack by all members, is ready
                self.ready.append(first)
                self.queue.remove(first)
            j += 1

        return sorted(self.ready, key=lambda tup: tup[1])