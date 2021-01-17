import unittest

from zoter import Zoter


class ZoterTest(unittest.TestCase):

    def test_get_publications(self):
        with Zoter() as z:
            pubs = z.get_my_publications()
            self.assertTrue(len(pubs) > 0)
