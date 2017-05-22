#!/usr/bin/env python3
# -*- coding: utf-8 -*-

# @Author: Olivier Watté <user>
# @Date:   2017-04-26T04:39:06-04:00
# @Email:  owatte@ipeos.com
# @Last modified by:   user
# @Last modified time: 2017-05-22T09:41:42-04:00
# @License: GPLv3
# @Copyright: IPEOS I-Solutions


"""
    This module provides an interface to manage PWM on RLIEH systems.

    This module is a part of the RLIEH project.

    The PWM value is a percentage of the total available power:
        - 0 = off
        - 100 = 100%
    The PWM value is a float with 2 decimal points.
        eg. 42.42

    Note : The default Raspberry Pi Leds pin for RLIEH Systems is pin 18

    Usage:

    >>> from core import RliehPWM
    >>> light = RliehPWM(pin=18)
    >>> light.pwm = 42.42
"""

import re
from subprocess import call

__all__ = ['RliehPWM']

class RliehPWM(object):
    """This class manages PWM intensity on a RLIEH system build over a Raspberry Pi .


    Attributes:
        - pin (int): Raspberry Pi's gpio used for PWM.

    Properties:
        - pwm (float): PWM value (between 0 and 1, 3 digits eg. 0.042).
    """

    def __init__(self, pin=18, pwm=None):
        """Sets up the Raspberry Pi GPIOs and sets the working directory.
        Args:
            pin (int): Raspberry Pi's gpio used for PWM.
        """
        self.pin = pin
        self.blaster = '/dev/pi-blaster'
        if not pwm == None:
            self.pwm = pwm

    @property
    def pwm(self):
        '''get pwm value for the given pin.'''

        pattern = r'{0}=[.0-9]+'.format(self.pin)
        blaster_file = open(self.blaster, 'r')
        blaster = blaster_file.read()
        blaster_file.close()
        try:
            ok = re.search(
                pattern,
                blaster,
                re.DOTALL
            )
            pwm = ok.group(0).split('=')[1]
        except:
            pwm =  0
        return pwm

    @pwm.setter
    def pwm(self, value):
        '''set pwm value for the given pin.

        Args:
            value (float, 3 digits) : number between 0 and 1 (included)
        '''

        blaster = '{0}={1}'.format(self.pin, value)
        cmd = "echo " + blaster + " > " + self.blaster
        call(cmd, shell=True)


if __name__ == '__main__':
    bitin = RliehPWM(pin=18, pwm=1)
    print('bitin-bagai')
