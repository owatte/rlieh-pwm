# @Author: Olivier Watté <user>
# @Date:   2017-07-25T12:22:59-04:00
# @Email:  owatte@ipeos.com
# @Last modified by:   user
# @Last modified time: 2017-08-01T19:39:53-04:00
# @License: GPLv3
# @Copyright: IPEOS I-Solutions

from numpy import allclose
import unittest
from .core import RliehPWM

class TestCalcPauseTime(unittest.TestCase):

    def setUp(self):
        pass

    def tearDown(self):
        pass

    def test__calc_pause_time(self):
        mytest = RliehPWM()
        actual = mytest._calc_pause_time(1000, 1000)
        expected = 60
        self.assertEqual(actual, expected, '60 should be the return value.')

class TestCalcSteps(unittest.TestCase):
    '''Perfom test on RliehPWM._calc_steps().'''

    def test__calc_steps__ascending_integer(self):
        mytest = RliehPWM()
        actual = mytest._calc_steps(10, 11)
        expected = [
            10.0, 10.1, 10.2, 10.3, 10.4, 10.5, 10.6, 10.7, 10.8, 10.9, 11.0
        ]
        self.assertTrue(allclose(actual, expected))

    def test__calc_steps__ascending_decimal(self):
        mytest = RliehPWM()
        actual = mytest._calc_steps(0.1, 2.2)
        expected = [0.1, 0.2, 0.3, 0.4, 0.5, 0.6, 0.7, 0.8, 0.9, 1.0, 1.1, 1.2,
                    1.3, 1.4, 1.5, 1.6, 1.7, 1.8, 1.9, 2.0, 2.1, 2.2]
        self.assertTrue(allclose(actual, expected))

    def test__calc_steps__descending_integer(self):
        mytest = RliehPWM()
        actual = mytest._calc_steps(81, 80)
        expected = [
            81.0, 80.9, 80.8, 80.7, 80.6, 80.5, 80.4, 80.3, 80.2, 80.1, 80.0
        ]
        self.assertTrue(allclose(actual, expected))

    def test__calc_steps__descending_decimal(self):
        mytest = RliehPWM()
        actual = mytest._calc_steps(97.1, 98.8)
        expected = [97.1, 97.2, 97.3, 97.4, 97.5, 97.6, 97.7, 97.8, 97.9, 98.0,
                    98.1, 98.2, 98.3, 98.4, 98.5, 98.6, 98.7, 98.8]
        self.assertTrue(allclose(actual, expected))


if __name__ == "__main__":
    # bt = TestPWMAvgPauseTime()
    # bt.test__get_avg_pause_time()
    unittest.main()
