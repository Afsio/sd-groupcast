'''
Arnau Montanes
Christian Zanger
01/05/2017 version 0.5
'''

from pyactor.context import sleep, interval, serve_forever

class Member(object):
    #TODO: implement bully leader election
    _tell = ['multicast', 'receive']
    _ask = ['get_message', 'get_queue']

    def __init__(self, group, printer, delay=0):
        self.group = group
        self.printer = printer
        self.queue = []
        self.delay = delay
        self.cur_acks = 0

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
    _tell = ['multicast', 'receive', 'process_msg', 'process_msg']
    _ask = ['get_message', 'get_queue']

    def __init__(self, group, printer, identifier):
        self.group = group
        self.printer = printer
        self.queue = []
        self.message = []
        self.clock = 0
        self.iden = identifier
        self.curr_acks = 0

    def multicast(self, message):
        self.clock += 1
        for member in self.group.get_members():
            member.receive(message, self.clock, self.iden)

    def receive(self, message, ts, iden):
        # self.printer.printmsg(self.proxy.get_id() + ' received: (' + message + ',' + str(ts) + ') clock: ' + str(self.clock))
        self.clock = max(self.clock, ts) + 1
        if message != 'ACK':
            # self.printer.printmsg(self.proxy.get_id() + ' received MESSAGE')
            #If m recieved, append to queue and sort according to timestamp
            self.queue.append((message, self.clock, iden))
            self.queue.sort(key=lambda tup: tup[1])
            #Then, ack everybody
            self.multicast('ACK')
        else:
            # self.printer.printmsg(self.proxy.get_id() + ' received ACK' + str(self.curr_acks ) + ' from ' + iden)
            future = self.group.get_members(future=True)
            future.add_callback('process_ack')

    def process_ack(self, future):
            #When ack recieved, append to queue and sort according to timestamp
            self.queue.append(('ACK', self.clock))
            self.queue.sort(key=lambda tup: tup[1])

            # nmembers = len(self.group.get_members())
            nmembers = len(future.result())
            self.curr_acks += 1

            if self.curr_acks == nmembers:
                #All ACKS received, it's safe to process the message
                self.process_msg(self.queue[0])
                #Delete message from queue and the corresponding ACKS
                self.curr_acks = 0
                self.queue.pop(0)
                for i in range(nmembers):
                    self.queue.pop(0)

    def process_msg(self, msg):
        self.message.append(msg)

    def get_message(self):
        return self.message

class Monitor(LamportMember):

    def process_msg(self, msg):
        self.message.append(msg)
        self.printer.printmsg(msg[2] + ": " + msg[0])
