
from printer import Printer
from group import Group
from member import Member
from pyactor.context import set_context, create_host, sleep, shutdown
from random import choice


if __name__ == '__main__':
    set_context('green_thread')

    h = create_host()
    p = h.spawn('printer', Printer)

    g = h.spawn('group', Group, [3, p])

    members = []

    for i in xrange(20):
        new_member = h.spawn('m'+str(i), Member, [g, p])
        g.join(new_member)
        members.append(new_member)

    g.init_start()

    for i in xrange(20):
        member = choice(members)
        member.multicast("Hi" + str(i) +  " ")
        print "Multicasting " + str(i)
        sleep(1)

    for member in members:
        p.printmsg(member.get_id() + ": " + ''.join(member.get_message()))

    # p.printmsg(g.get_members())
    #
    # sleep(5)
    # g.announce(p1)
    # sleep(12)
    #
    # p.printmsg(g.get_members())

    shutdown()
