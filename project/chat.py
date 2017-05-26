from pyactor.context import set_context, create_host, serve_forever, sleep
from group_s import Group
from member_s import Member, LamportMember
from printer_s import Printer


def sequencer():
    members = []

    for i in xrange(1):
        new_member = h.spawn('Remote'+str(i), Member, [g, p, 0, True])
        g.join(new_member)
        members.append(new_member)


def lamport():
    members = []

    for i in xrange(1):
        new_id = 'Remote'+str(i)
        new_member = h.spawn(new_id, LamportMember, [g, p, new_id, True])
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
