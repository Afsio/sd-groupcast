from pyactor.context import set_context, create_host, serve_forever, shutdown, sleep
from group import Group
from member import Member, LamportMember
from printer import Printer

def sequencer():
    members = []

    for i in xrange(1):
        new_member = h.spawn('Remote'+str(i), Member, [g, p, 0, True])
        g.join(new_member)
        members.append(new_member)

def lamport():
    members = []

    for i in xrange(1):
        new_member = h.spawn('Remote'+str(i), LamportMember, [g, p, 'Remote'+str(i), True])
        g.join(new_member)
        members.append(new_member)


if __name__ == '__main__':
    set_context()

    h = create_host('http://127.0.0.1:1278')

    p = h.spawn('printer', Printer)
    g = h.lookup_url('http://127.0.0.1:1277/group', 'Group', 'test')

    demo = ''

    while(demo not in ['sequencer', 'lamport']):
        demo = raw_input('sequencer or lamport demo? ')

    if demo == 'sequencer':
        sequencer()
    else:
        lamport()

    serve_forever()
