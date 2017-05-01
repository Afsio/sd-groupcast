
from printer import Printer
from group import Group
from member import Member
from pyactor.context import set_context, create_host, sleep, shutdown


if __name__ == '__main__':
    set_context('green_thread')

    h = create_host()
    p = h.spawn('printer', Printer)

    g = h.spawn('group', Group, [3, p])

    p1 = h.spawn('p1', Member, [g, p])
    p2 = h.spawn('p2', Member, [g, p])
    p3 = h.spawn('p3', Member, [g, p])

    g.join(p1)
    g.join(p2)
    g.join(p3)

    g.init_start()

    p.printmsg(g.get_members())

    sleep(5)
    g.announce(p1)
    sleep(12)

    p.printmsg(g.get_members())

    shutdown()
