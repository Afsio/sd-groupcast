'''
Arnau Montanes
Christian Zanger
01/05/2017 version 0.7
'''

from pyactor.context import sleep, interval


class Member(object):
    _tell = ['multicast', 'receive', 'process_msg', 'process_queue',
             'init_start', 'announce']
    _ask = ['get_message', 'get_queue']

    def __init__(self, group, printer, delay=0, monitor=False):
        self.group = group
        self.printer = printer
        self.queue = []
        self.message = []
        self.delay = delay
        self.monitor = monitor
        self.cur_acks = 0

    def init_start(self):
        self.time_announce = interval(self.host, 6, self.proxy, 'announce')

    def stop_announce(self):
        self.time_announce.set()

    def announce(self):
        self.group.announce(self)

    def multicast(self, message):
        ts = self.group.get_sequencer().timestamp()
        sleep(self.delay)
        for member in self.group.get_members():
            member.receive(message, ts)

    def process_queue(self, message, ts):
        if len(self.message) == 0:
            # Message empty, we expect a ts of 0
            if ts == 0:
                self.process_msg(self.queue[0])
                self.queue.pop(0)
        elif ts == self.message[-1][1] + 1:
            self.queue = sorted(self.queue, key=lambda tup: tup[1])
            self.process_msg(self.queue[0])
            self.queue.pop(0)
            if len(self.queue) != 0:
                self.process_queue(self.queue[0][0], self.queue[0][1])

    def receive(self, message, ts):
        self.queue.append((message, ts))
        self.process_queue(message, ts)

    def process_msg(self, msg):
        if self.monitor:
            self.printer.printmsg(msg)
        self.message.append(msg)

    def get_queue(self):
        return self.queue

    def get_message(self):
        return self.message


class LamportMember(Member):

    def __init__(self, group, printer, identifier, monitor=False):
        self.group = group
        self.printer = printer
        self.queue = []
        self.message = []
        self.clock = 0
        self.iden = identifier
        self.curr_acks = 0
        self.monitor = monitor

    def multicast(self, message):
        self.clock += 1
        for member in self.group.get_members():
            member.receive(message, self.clock, self.iden)

    def receive(self, message, ts, iden):
        self.clock = max(self.clock, ts) + 1
        if message != 'ACK':
            # self.printer.printmsg(self.proxy.get_id() + ' received MESSAGE')
            # If m recieved, append to queue and sort according to timestamp
            self.queue.append((message, self.clock, iden))
            self.queue.sort(key=lambda tup: tup[1])
            # Then, ack everybody
            self.multicast('ACK')
        else:
            future = self.group.get_members(future=True)
            future.add_callback('process_ack')

    def process_ack(self, future):
            # When ack recieved,append to queue and sort according to timestamp
            self.queue.append(('ACK', self.clock))
            self.queue.sort(key=lambda tup: tup[1])

            # nmembers = len(self.group.get_members())
            nmembers = len(future.result())
            self.curr_acks += 1

            if self.curr_acks == nmembers:
                # All ACKS received, it's safe to process the message
                self.process_msg(self.queue[0])
                # Delete message from queue and the corresponding ACKS
                self.curr_acks = 0
                self.queue.pop(0)
                for i in range(nmembers):
                    self.queue.pop(0)
