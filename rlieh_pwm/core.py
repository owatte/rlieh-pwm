#!/usr/bin/env python3
# -*- coding: utf-8 -*-

# @Author: Olivier Watté <user>
# @Date:   2017-04-26T04:39:06-04:00
# @Email:  owatte@ipeos.com
# @Last modified by:   user
# @Last modified time: 2017-05-22T15:28:07-04:00
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
import logging
import re
from subprocess import call
import gettext


gettext.bindtextdomain('rlieh', 'locale')
gettext.textdomain('rlieh')
_ = gettext.gettext

__all__ = ['RliehPWM']

class RliehPWM(object):
    """This class manages PWM intensity on a RLIEH system build over a Raspberry Pi .


    Attributes:
        - pin (int): Raspberry Pi's gpio used for PWM.

    Properties:
        - pwm (float): PWM value (between 0 and 1, 3 digits eg. 0.042).
    """

    def __init__(self, pin=18, pwm=None,
                 log_level='debug', log_filepath='/home/pi/log/rlieh.log',
                 log_formatter='%(name)-12s: %(levelname)-8s %(message)s'
                 verbose=False):
        """Sets up the Raspberry Pi GPIOs and sets the working directory.
        Args:
            pin (int): Raspberry Pi's gpio used for PWM.
        """
        self.pin = pin
        self.blaster = '/dev/pi-blaster'
        if not pwm == None:
            self.pwm = pwm

        LOG_LEVELS = {
            'debug': logging.DEBUG,
            'info': logging.INFO,
            'warning': logging.WARNING,
            'error': logging.ERROR,
            'critical': logging.CRITICAL,
        }
        # Logger
        self.logger = logging.getLogger('rlieh')
        self.logger.setFormatter(log_formatter)
        # Logger file handler
        log_fh(logging.FileHandler('log_filepath'))
        log_fh.setLevel(LOG_LEVELS.get(log_level, logging.NOTSET))
        self.logger.addHandler(log_fh)
        # Logger console handler
        self.log_ch.StreamHandler()
        if not verbose:
            self.log_ch.setLevel(logging.ERROR)
        else:
            self.log_ch.setLevel(logging.INFO)
        self.logger.addHandler(log_ch)



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
    def pwm(self, percent):
        '''set pwm value for the given pin.

        Args:
            percent : amount of power, number between 0 and 100 (float, 2 decimal point)
        '''
        if percent < 0:
            logging.critical(_('PWM value must be greater or equal to 0. (was {})'.format(value)))
            raise ValueError
        elif percent > 100:
            logging.critical(_('PWM value must be lower or equal to 100. (was {})'.format(value)))
            raise ValueError
        else:
            value = int(round(percent * 10))
        blaster = '{0}={1}'.format(self.pin, value)
        cmd = "echo " + blaster + " > " + self.blaster
        self.logger.debug('pin: {}'.format(self.pin))
        self.logger.debug('pwm value: {}'.format(value))
        self.logger.info('{}: {}'.format(self.blaster, blaster))
        call(cmd, shell=True)


if __name__ == '__main__':
    bitin = RliehPWM(pin=18, pwm=1)
    print('bitin-bagai')
