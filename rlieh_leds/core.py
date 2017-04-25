# -*- coding: utf-8 -*-

"""
    This module provides an interface to manage light using leds and PWM.

    This module is a part of the RLIEH project.

    The PWM uses the pi-blaster driver, so the PWM value should be incuded in a
    range from 0 to 1, with 3 digits.

    Usage:

    >>> from core import RliehLeds
    >>> light = RliehLeds(pin=18)
    >>> light.pwm = 0.420
"""

import re
import os
from subprocess import call

__all__ = ['RliehLeds']

class RliehLeds(object):
    """This class manages leds intensity using PWM pi-blaster interface.

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
    bitin = RliehLeds(pin=18, pwm=1)
