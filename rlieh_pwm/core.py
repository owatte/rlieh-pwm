#!/usr/bin/env python3
# -*- coding: utf-8 -*-

# @Author: Olivier Watté <user>
# @Date:   2017-04-26T04:39:06-04:00
# @Email:  owatte@ipeos.com
# @Last modified by:   user
# @Last modified time: 2017-05-22T19:05:14-04:00
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
                 #  log_formatter='%(name)-12s: %(levelname)-8s %(message)s',
                 log_formatter='%(levelname)s:%(message)s',
                 verbose=False):
        """Sets up the Raspberry Pi GPIOs and sets the working directory.
        Args:
            pin (int): Raspberry Pi's gpio used for PWM.
        """

        # gpio numbers working with pwm using pi-blaster
        BCM_PINS = [3, 5, 7, 8, 10, 11, 12, 13, 15, 16, 18, 19, 21, 22, 23, 24,
                    26, 27, 28, 29, 31, 32, 33, 35, 36, 37, 38, 40]
        LOG_LEVELS = {'debug': logging.DEBUG,
                      'info': logging.INFO,
                      'warning': logging.WARNING,
                      'error': logging.ERROR,
                      'critical': logging.CRITICAL
        }
        # Logger
        self.logger = logging.getLogger('rlieh')
        # Logger file handler
        log_fh = logging.FileHandler('log_filepath')
        log_fh.setLevel(LOG_LEVELS.get(log_level, logging.NOTSET))
        log_fh.setFormatter(log_formatter)
        self.logger.addHandler(log_fh)
        # Logger console handler
        log_ch = logging.StreamHandler()
        if not verbose:
            log_ch.setLevel(logging.ERROR)
        else:
            log_ch.setLevel(logging.INFO)
        log_ch.setFormatter(log_formatter)
        self.logger.addHandler(log_ch)

        self.blaster = '/dev/pi-blaster'
        # for pinz in BCM_PINS:
        #     print(pinz)
        # print('<<<<', pin, '>>>>>> ',type(pin))
        if not(int(pin) in BCM_PINS):
            BCM_PINS = [str(bcm_pin) for bcm_pin in BCM_PINS]
            logging.critical(_('Pin number must be in : {}. (was {})'.\
                               format(', '.join(BCM_PINS), str(pin))))
            raise ValueError
        else:
            self.pin = pin
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
    def pwm(self, percent):
        '''set pwm value for the given pin.

        Args:
            percent : amount of power, number between 0 and 100 (float, 2 decimal point)
        '''
        percent = float(percent)
        if percent < 0:
            logging.critical(_('PWM value must be greater or equal to 0. (was {})'.format(percent)))
            raise ValueError
        elif percent > 100:
            logging.critical(_('PWM value must be lower or equal to 100. (was {})'.format(percent)))
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
