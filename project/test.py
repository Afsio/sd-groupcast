from printer_s import Printer
from group_s import Group
from sequencer_s import Sequencer, BullySequencer
from member_s import Member, LamportMember
from pyactor.context import set_context, create_host, sleep, shutdown
from random import choice

def sequencer():
    s = []
    for i in xrange(4):
        new = h.spawn('sequencer'+str(i), BullySequencer, [i, g, p])
        s.append(new)

    g.attach_sequencers(s)

    for bully in s:
        bully.init_start(s)

    members = []

    #Simulate delay for peer3 and peer7
    for i in xrange(10):
        if i == 3:
            new_member = h.spawn('m'+str(i), Member, [g, p, 0.5])
        elif i == 7:
            new_member = h.spawn('m'+str(i), Member, [g, p, 1])
        else:
            new_member = h.spawn('m'+str(i), Member, [g, p])
        g.join(new_member)
        members.append(new_member)

    g.init_start()

    for member in g.get_members():
        member.init_start()

    j = 0
    for member in g.get_members():
        member.multicast("Hi" + str(j))
        j += 1
        print "Multicasting message " + str(j)
        sleep(0.2)

    sleep(3)

    for member in g.get_members():
        p.printmsg(member.get_id() + ": " + ''.join(str(member.get_queue())))

    p.printmsg("======================================================")

    for member in members:
        p.printmsg(member.get_id() + ": " + ''.join(str(member.get_message())))

def lamport():
    members = []

    for i in xrange(5):
        iden = 'm'+str(i)
        new_member = h.spawn(iden, LamportMember, [g, p])
        g.join(new_member, iden)
        members.append(new_member)

    g.init_start()

    for member in members:
        member.init_start()

    j = 0
    for member in members:
        member.multicast("Hi" + str(j) +  " ")
        j += 1
        print "Multicasting message."
        sleep(1)

    for member in members:
        p.printmsg(member.get_id() + ": " + ''.join(str(member.get_queue())))

    p.printmsg("======================================================")

    for member in members:
        p.printmsg(member.get_id() + ": " + ''.join(str(member.get_message())))

if __name__ == '__main__':
    set_context()

    h = create_host('http://127.0.0.1:1277/')

    p = h.spawn('printer', Printer)
    demo = ""

    g = h.spawn('group', Group, [p])

    while(demo not in ['sequencer', 'lamport']):
        demo = raw_input('sequencer or lamport demo? ')

    if demo == 'sequencer':
        sequencer()
    else:
        lamport()

    sleep(3)
    print 'Exiting demo...'

    shutdown()
