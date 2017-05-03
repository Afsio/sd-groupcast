
from printer import Printer
from group import Group
from sequencer import Sequencer
from member import Member
from pyactor.context import set_context, create_host, sleep, shutdown
from random import choice


if __name__ == '__main__':
    set_context('green_thread')

    h = create_host()
    p = h.spawn('printer', Printer)

    g = h.spawn('group', Group, [3, p])
    s = h.spawn('sequencer', Sequencer)

    g.attach_sequencer(s)

    members = []

    for i in xrange(10):
        if i == 3:
            new_member = h.spawn('m'+str(i), Member, [g, p, 0.5])
        elif i == 7:
            new_member = h.spawn('m'+str(i), Member, [g, p, 0.7])
        else:
            new_member = h.spawn('m'+str(i), Member, [g, p])
        g.join(new_member)
        members.append(new_member)

    g.init_start()

    for member in members:
        member.multicast("Hi" + str(i) +  " ")
        print "Multicasting message."

    sleep(2)

    for member in members:
        p.printmsg(member.get_id() + ": " + ''.join(str(member.get_queue())))

    p.printmsg("======================================================")

    for member in members:
        p.printmsg(member.get_id() + ": " + ''.join(str(member.get_message())))

    shutdown()
