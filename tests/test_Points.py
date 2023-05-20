import unittest
from models.Utils import calc_d

class TestPoints(unittest.TestCase):

    def test_calc_d(self):

        p1, p2 = (1.0, 1.0), (1.0, 2.0)
        self.assertEqual(0.0, calc_d(p1, p2))
        p1, p2 = (1.0, 1.0), (2.0, 2.0)
        self.assertEqual(1.0, calc_d(p1, p2))
        p1, p2 = (2.0, 2.0), (2.0, 2.0)
        self.assertEqual(-1.0, calc_d(p1, p2))

        # test for too many decimals
        p1, p2 = (24.23, 44.44), (43.43, 34.34)
        self.assertEqual(28.299999999999994, calc_d(p1, p2))
        p1, p2 = (24.24, 42.42), (42.42, 24.24)
        self.assertEqual(35.36000000000001, calc_d(p1, p2))
        p1, p2 = (43.43, 22.22), (11.11, 12.12)
        self.assertEqual(41.42, calc_d(p1, p2))

if __name__ == '__main__':
    unittest.main()
