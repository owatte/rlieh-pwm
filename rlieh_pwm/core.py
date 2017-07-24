#!/usr/bin/env python3
# -*- coding: utf-8 -*-

# @Author: Olivier Watté <user>
# @Date:   2017-04-26T04:39:06-04:00
# @Email:  owatte@ipeos.com
# @Last modified by:   user
# @Last modified time: 2017-07-24T12:39:15-04:00
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
import logging.config
import os
import re
from subprocess import call
import gettext


gettext.bindtextdomain('rlieh', 'locale')
gettext.textdomain('rlieh')
_ = gettext.gettext


__all__ = ['RliehPWM']


class RliehPWM(object):
    """This class manages PWM on a RLIEH system build over a Raspberry Pi .


    Attributes:
        - pin (int): Raspberry Pi's gpio used for PWM.

    Properties:
        - pwm (float): PWM value (between 0 and 1, 3 digits eg. 0.042).
    """

    def __init__(self, pin=18, pwm=None,
                 log_level='DEBUG', log_path='/home/pi/log'):
        """Sets up the Raspberry Pi GPIOs and sets the working directory.
        Args:
            pin (int): Raspberry Pi's gpio used for PWM.
        """

        # gpio numbers working with pwm using pi-blaster
        BCM_PINS = [3, 5, 7, 8, 10, 11, 12, 13, 15, 16, 18, 19, 21, 22, 23, 24,
                    26, 27, 28, 29, 31, 32, 33, 35, 36, 37, 38, 40]

        # Logger
        self.logger = logging.getLogger(__name__)
        DEFAULT_LOGGING = {
            'version': 1,
            'disable_existing_loggers': False,
            'formatters': {
                'basic': {
                    'format': '%(asctime)-6s: %(name)s - %(levelname)s - %(message)s',
                }
            },
            'handlers': {
                'console': {
                    'level': 'DEBUG',
                    'class': 'logging.StreamHandler',
                    'formatter': 'basic',
                },
                'main_file': {
                    'level': 'INFO',
                    'filter': 'WARNING',
                    'class': 'logging.handlers.WatchedFileHandler',
                    'formatter': 'basic',
                    'filename': os.path.join(log_path, 'pwm.log'),
                },
                'error_file': {
                    'level': 'ERROR',
                    'class': 'logging.handlers.WatchedFileHandler',
                    'formatter': 'basic',
                    'filename': os.path.join(log_path, 'pwm_error.log'),
                }
            },
            'loggers': {
                'foo.bar': {
                    'handlers': ['console', 'main_file', 'error_file'],
                    'level': log_level,
                    'propagate': False
                },
            },
            'root': {
                'handlers': ['console', 'main_file', 'error_file'],
                'level': log_level,
            }
        }
        logging.config.dictConfig(DEFAULT_LOGGING)

        self.blaster = '/dev/pi-blaster'
        if not(int(pin) in BCM_PINS):
            BCM_PINS = [str(bcm_pin) for bcm_pin in BCM_PINS]
            logging.critical(_('Pin number must be in : {}. (was {})'.
                               format(', '.join(BCM_PINS), str(pin))))
            raise ValueError
        else:
            self.pin = pin
        if pwm is not None:
            self.pwm = pwm

    @property
    def pwm(self):
        '''get pwm value for the given pin.'''
        pass
        pattern = r'{0}=[.0-9]+'.format(self.pin)
        blaster_file = open(self.blaster, 'r')
        blaster = blaster_file.read()
        blaster_file.close()

        ok = re.search(
            pattern,
            blaster,
            re.DOTALL
        )
        if ok:
            pwm = ok.group(0).split('=')[1]
        else:
            pwm =  0
        return pwm
        #
        #
        # try:
        #     ok = re.search(
        #         pattern,
        #         blaster,
        #         re.DOTALL
        #     )
        #     pwm = ok.group(0).split('=')[1]
        # except:
        #     pwm =  0
        # return pwm

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
            value = round(percent / 100., 4)
        blaster = '{0}={1}'.format(self.pin, value)
        cmd = "echo " + blaster + " > " + self.blaster
        self.logger.debug('pin: {}'.format(self.pin))
        self.logger.debug('pwm value: {}'.format(value))
        self.logger.info('{}: {}'.format(self.blaster, blaster))
        call(cmd, shell=True)


if __name__ == '__main__':
    bitin = RliehPWM(pin=18, pwm=1)
    for i in range(1000, -1, -1):
        print(i)
        if i != 0 :
            j = i/10.
        else:
            j = i
        val = round(j / 100., 4)
        print ("percent: ", j, " value: ", val)

    print('bitin-bagai')
