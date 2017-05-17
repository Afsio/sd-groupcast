
from printer import Printer
from group import Group
from sequencer import Sequencer
from member import Member, LamportMember, Monitor
from pyactor.context import set_context, create_host, sleep, shutdown
from random import choice

def sequencer():
    s = h.spawn('sequencer', Sequencer)

    g.attach_sequencer(s)

    members = []

    #Simulate delay for peer3 and peer7
    for i in xrange(10):
        if i == 3:
            new_member = h.spawn('m'+str(i), Member, [g, p, 0.5])
        elif i == 7:
            new_member = h.spawn('m'+str(i), Member, [g, p, 2])
        else:
            new_member = h.spawn('m'+str(i), Member, [g, p])
        g.join(new_member)
        members.append(new_member)

    g.init_start()

    j = 0
    for member in members:
        member.multicast("Hi")
        j += 1
        print "Multicasting message."

    sleep(2)

    for member in members:
        p.printmsg(member.get_id() + ": " + ''.join(str(member.get_queue())))

    p.printmsg("======================================================")

    for member in members:
        p.printmsg(member.get_id() + ": " + ''.join(str(member.get_message())))



def lamport():
    members = []
    ids = []

    for i in xrange(5):
        iden = 'm'+str(i)
        ids.append(iden)
        new_member = h.spawn(iden, LamportMember, [g, p, iden])
        g.join(new_member, iden)
        members.append(new_member)

    # m = h.spawn('monitor', Monitor, [g, p, 'Monitor'])
    # g.join(m, 'monitor')
    # members.append(m)

    g.init_start()
    # p.printmsg(g.get_members_ids())


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

    g = h.spawn('group', Group, [3, p])

    while(demo not in ['sequencer', 'lamport']):
        demo = raw_input('sequencer or lamport demo? ')

    if demo == 'sequencer':
        sequencer()
    else:
        lamport()

    sleep(1)
    print 'Exiting demo...'
    sleep(2)

    shutdown()
