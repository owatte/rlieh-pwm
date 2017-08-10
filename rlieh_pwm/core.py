#!/usr/bin/env python3
# -*- coding: utf-8 -*-

# @Author: Olivier Watté <user>
# @Date:   2017-04-26T04:39:06-04:00
# @Email:  owatte@ipeos.com
# @Last modified by:   user
# @Last modified time: 2017-08-10T10:29:56-04:00
# @License: GPLv3
# @Copyright: Olivier Watté

# Rlieh-pwm provides an interface to manage PWM on RLIEH systems.
# Copyright (C) 2017 Olivier Watte
#
# This file is part of rlieh-pwm.
#
# Rlieh-pwm is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# Rlieh-pwm is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with rlieh-pwm.  If not, see <http://www.gnu.org/licenses/>.


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
from time import sleep
from subprocess import call, CalledProcessError
import sys
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
                 log_level='critical', log_path='/var/log/rlieh'):
        """Sets up the Raspberry Pi GPIOs and sets the working directory.
        Args:
            pin (int): Raspberry Pi's gpio used for PWM.
        """

        # Logger
        LOGGING_LEVELS = {'debug': 'DEBUG', 'info': 'INFO',
                          'warning': 'WARNING', 'error': 'ERROR',
                          'critical': 'CRITICAL'}

        log_level = log_level.lower()
        if log_level in LOGGING_LEVELS:
            self.log_level = LOGGING_LEVELS[log_level]
        else:
            log_levels = ', '.join(LOGGING_LEVELS.keys())
            raise ValueError(
                _('Unknown log_level "{}". '
                  'Log level should be a value in: {}.'.format(
                    log_level, log_levels))
            )
        self.log_path = log_path
        LOGGING = {
            'version': 1,
            'disable_existing_loggers': False,
            'formatters': {
                'basic': {
                    'format': ('%(asctime)-6s: %(name)s - '
                               '%(levelname)s - %(message)s'),
                },
                'short': {
                    'format': ('[%(levelname)s]  %(message)s'),
                }
            },
            'handlers': {
                'console': {
                    'level': self.log_level,
                    'class': 'logging.StreamHandler',
                    'formatter': 'short',
                },
                'main_file': {
                    'level': self.log_level,
                    'class': 'logging.handlers.WatchedFileHandler',
                    'formatter': 'basic',
                    'filename': os.path.join(self.log_path, 'pwm.log'),
                },
                'error_file': {
                    'level': 'ERROR',
                    'class': 'logging.handlers.WatchedFileHandler',
                    'formatter': 'basic',
                    'filename': os.path.join(self.log_path, 'pwm_error.log'),
                }
            },
            'loggers': {
                'rlieh': {
                    'handlers': ['console', 'main_file', 'error_file'],
                    'level': self.log_level,
                    'propagate': False
                },
            },
            'root': {
                'handlers': ['console', 'main_file', 'error_file'],
                'level': self.log_level,
            }
        }
        if self.log_level:
            logging.config.dictConfig(LOGGING)
        self.logger = logging.getLogger(__name__)

        self.blaster = '/dev/pi-blaster'

        # gpio numbers working with pwm using pi-blaster
        BCM_PINS = [3, 5, 7, 8, 10, 11, 12, 13, 15, 16, 18, 19, 21, 22, 23, 24,
                    26, 27, 28, 29, 31, 32, 33, 35, 36, 37, 38, 40]

        if not(int(pin) in BCM_PINS):
            BCM_PINS = [str(bcm_pin) for bcm_pin in BCM_PINS]
            self.logger.critical(_('Pin number must be in : {}. (was {})'.
                                   format(', '.join(BCM_PINS), str(pin))))
            raise ValueError(_('Bad pin value ({})'.format(str(pin))))
        else:
            self.pin = pin
            self.logger.debug('pin: {}'.format(self.pin))
        self.__pwm = pwm

    @property
    def pwm(self):
        '''get pwm value for the given pin.'''
        self.logger.debug('pwm: {}%'.format(self.__pwm))
        return self.__pwm

    @pwm.setter
    def pwm(self, percent):
        '''set pwm value for the given pin.

        Args:
            percent : amount of power, number between 0 and 100 
            (float, 2 decimal point)
        '''

        self._blast(self._convert_percent_to_blaster(float(percent)))
        self.__pwm = percent

    def modulate(self, begin, end, duration):
        '''Set modulation value from a range of values for a duration.

        Args:
            begin (float): first range value
            end (float): last range value
            duration (float): total time of duration in minutes
        Returns:
            integer : average sleep time in seconds
        '''
        if begin == end:
            error_msg = 'Range BEGIN and range START can\'t be equal. {}={}' \
                      .format(begin, end)
            raise ValueError(error_msg)
        elif begin < 0:
            error_msg = 'Range BEGIN must be greater or equal to 0. (was {})' \
                      .format(begin)
            raise ValueError(error_msg)
        elif end > 100:
            error_msg = 'Range END must be lower or equal to 100. (was {})' \
                      .format(end)
            raise ValueError(error_msg)

        steps = self._calc_steps(begin, end)
        pause_time = self._calc_pause_time(duration, len(steps))
        for step in steps:
            self.pwm = step
            sleep(pause_time)

    def _blast(self, value):
        '''call pi-blaster'''

        cmd = self._build_blaster_cmd(value)

        try:
            call(cmd, shell=True)
            self.logger.debug('_blast : {}'.format(value))
        except CalledProcessError as e:
            self.logger.critical(
                _('_blast failed, returned code {}'.format(e.returncode))
            )
            sys.exit(
                _('PWM modulation value {} on pin {} failed'
                    .format(self.pin, value))
            )
        except OSError as e:
            self.logger.critical(
                _('_blast failed {}.'.format(e.strerror))
            )
            sys.exit(
                _('PWM modulation value {} on pin {} failed'
                    .format(self.pin, value))
            )

    def _build_blaster_cmd(self, value):
        '''Forge blaster command.

        Args:
            value: pi-blaster pwm value

        Retruns:
            pi-blaster command
        '''

        blaster = '{0}={1}'.format(self.pin, value)
        cmd = "/bin/echo " + blaster + " > " + self.blaster
        self.logger.debug(_('cmd blaster command: {}'.format(cmd)))
        return cmd

    def _convert_percent_to_blaster(self, percent):
        '''convert PWM percent in pi-blaster value.

        Args:
            percent (float): PWM modulation percentage

        Returns:
            float: pi-blaster PWM value (number between 0 and 1, with 3 digits)
        '''

        if percent < 0:
            self.logger.critical(
                _('PWM value must be greater or equal to 0. (was {})'
                    .format(percent))
            )
            raise ValueError(_('Bad PWM percent ({})'.format(percent)))
        elif percent > 100:
            self.logger.critical(
                _('PWM value must be lower or equal to 100. (was {})').
                format(percent)
            )
            raise ValueError(_('Bad PWM percent ({})'.format(percent)))
        else:
            value = round(percent / 100., 4)

        self.logger.debug(_('{}% PWM = {}'.format(percent, value)))
        return value

    def _calc_pause_time(self, duration, steps=1000):
        '''get average pause time for giving variation total duration.

        Args:
            duration (float): total duration in minutes

        Returns:
            integer: average sleep time in seconds
        '''

        avg_pause_time = float(duration) * 60. / steps
        self.logger.debug(_('_calc_pause_time: {}').format(avg_pause_time))
        return avg_pause_time

    def _calc_steps(self, begin, end):
        '''calculates steps needed for a modulation range.

        Works like the built-in range(start, stop, step) function,
        but with float as start, stop and step vars.
        The range end value is included as last step.

        Args:
            begin: first modulation step
            end: last modulation step

        Returns:
            tuple: list of steps
        '''

        self.logger.debug(_('modulation begin: {}'.format(begin)))
        self.logger.debug(_('modulation end: {}'.format(end)))
        begin *= 10
        end *= 10
        if end > begin:
            step = 1
            end += 1
        else:
            step = -1
            end -= 1
        self.logger.debug(_('range begin: {}'.format(begin)))
        self.logger.debug(_('range end: {}'.format(end)))

        steps = [x/10. for x in range(int(begin), int(end), step)]
        self.logger.debug(_('_calc_steps: {}'.format(steps)))
        return steps
