import unittest
from project import group_s
from project import printer_s
from project import member_s
from pyactor.context import set_context, create_host, shutdown, sleep

class TestGroup(unittest.TestCase):

    def setUp(self):
        # Gets executed before every test
        set_context()
        self.h = create_host()
        self.p = self.h.spawn('printer', printer_s.Printer)
        self.g = self.h.spawn('group', group_s.Group, [self.p])

    def tearDown(self):
        # Gets executed after every test
        shutdown()

    def test_members_leave(self):
        # Test if members join and leave correctly if not announced
        m1 = self.h.spawn('m1', member_s.Member, [self.p, self.g])
        self.g.join(m1)
        self.g.init_start()
        self.assertTrue(len(self.g.get_members()) == 1)
        sleep(12)
        #Test that if no announces are made by the peer, it gets kicked out
        self.assertTrue(len(self.g.get_members()) == 0)





if __name__ == '__main__':
    suite = unittest.TestLoader().loadTestsFromTestCase(TestStringMethods)
    unittest.TextTestRunner(verbosity=2).run(suite)
