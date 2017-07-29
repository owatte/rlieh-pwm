# @Author: Olivier Watté <user>
# @Date:   2017-07-25T12:22:59-04:00
# @Email:  owatte@ipeos.com
# @Last modified by:   user
# @Last modified time: 2017-07-29T05:05:10-04:00
# @License: GPLv3
# @Copyright: IPEOS I-Solutions

from numpy import allclose, arange
import unittest
from .core import RliehPWM

class TestPWMAvgPauseTime(unittest.TestCase):

    def setUp(self):
        pass

    def tearDown(self):
        pass

    def test__get_avg_pause_time(self):
        mytest = RliehPWM(log_level="WARNING")
        actual = mytest._avg_pause_time(1000, 1000)
        expected = 60
        self.assertEqual(actual, expected, '60 should be the return value.')

class TestSteps(unittest.TestCase):
    '''Perfom test on RliehPWM._steps().'''

    def test___steps_ascending(self):
        mytest = RliehPWM(log_level="WARNING")
        begin = 0
        end = 10
        actual = mytest._steps(0, 10)
        expected = arange(0, 10, 0.1)
        self.assertTrue(allclose(actual, expected))

    def test___steps_descending(self):
        mytest = RliehPWM(log_level="WARNING")
        begin = 10
        end = 0
        actual = mytest._steps(10, 0)
        expected = arange(10, 0, -0.1)
        self.assertTrue(allclose(actual, expected))

if __name__ == "__main__":
    # bt = TestPWMAvgPauseTime()
    # bt.test__get_avg_pause_time()
    unittest.main()
