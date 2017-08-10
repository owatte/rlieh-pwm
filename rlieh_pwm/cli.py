#!/usr/bin/env python3
# -*- coding: utf-8 -*-

# @Author: Olivier Watté <user>
# @Date:   2017-04-26T04:42:30-04:00
# @Email:  owatte@ipeos.com
# @Last modified by:   user
# @Last modified time: 2017-08-10T10:29:34-04:00
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


"""PWM management for RLIEH systems:

Usage:
  rlieh-pwm (on|off) GPIO [--log-level=LOG_LEVEL] [--log-path=LOG_DIR_PATH]
  rlieh-pwm set VALUE GPIO [--log-level=LOG_LEVEL] [--log-path=LOG_DIR_PATH]
  rlieh-pwm range BEGIN END GPIO [--duration=MINUTES] [--log-level=LOG_LEVEL]
            [--log-path=LOG_DIR_PATH]
  rlieh-pwm fx-light (--dawn|--sunrise|--noon|--sunset|--dusk) GPIO
            [--duration=MINUTES] [--log-level=LOG_LEVEL]
            [--log-path=LOG_DIR_PATH]
  rlieh-pwm (-h |--help)
  rlieh-pwm (-v |--version)

Arguments:
  GPIO        Raspberry Pi GPIO pin
  VALUE       Percent of modulation
              minimal modulation = 0.01, power Off = 0, power On = 100

Options:
  -h --help                 Shows this help message and exit.
  -v --version              Shows version number and exit.
  --duration=MINUTES        Duration of effect in minutes. (Default = 0.5)
  --log-level=LOG_LEVEL     none, critical, warning, error, info, debug.
                            (Default = none, no log)
  --log-path=LOG_DIR_PATH  Set log file path. (Default = /var/log/rlieh)

Tip:
  Use an alias to set a default GPIO (eg. alias light='rlieh-pwm $@ 18')

RLIEH puts a roXXXing poney in your aquarium and greenhouses
"""


from __future__ import absolute_import
from docopt import docopt

from rlieh_pwm import __version__
from rlieh_pwm.core import RliehPWM

PWM_THRESHOLDS = {'dawn': [0, 20],
                  'sunrise': [20, 75],
                  'noon': [75, 100, 75],
                  'sunset': [75, 20],
                  'dusk': [20, 0]}

# default modulation range duration (in minutes)
DURATION = 0.5

# default log level
LOG_LEVEL = 'error'


class MyPWM(RliehPWM):
    def __init__(self, pin, pwm_thresholds=PWM_THRESHOLDS, **kwargs):
        super().__init__(pin=pin, **kwargs)
        self.pwm_thresholds = pwm_thresholds


def main():
    arguments = docopt(__doc__, version='RLIEH PWM {}'.format(__version__))
    # optionnal args and default values
    if arguments['--duration']:
        duration = float(arguments['--duration'])
    else:
        duration = float(DURATION)
    if arguments['--log-level']:
        log_level = arguments['--log-level'].lower()
    else:
        log_level = LOG_LEVEL
    if arguments['--log-path']:
        log_path = arguments['--log-path']
    else:
        log_path = '/var/log/rlieh'

    mypwm = MyPWM(arguments['GPIO'], log_level=log_level, log_path=log_path,
                  pwm_thresholds=PWM_THRESHOLDS)

    if arguments['set']:
        mypwm.pwm = arguments['VALUE']
    elif arguments['on']:
        mypwm.pwm = 100
    elif arguments['off']:
        mypwm.pwm = 0
    elif arguments['range']:
        mypwm.modulate(float(arguments['BEGIN']),
                       float(arguments['END']),
                       duration)
    # fx-light --dawn|--sunrise|--noon|--sunset|--dusk
    elif arguments['fx-light']:
        if arguments['--dawn']:
            mypwm.modulate(mypwm.pwm_thresholds['dawn'][0],
                           mypwm.pwm_thresholds['dawn'][1],
                           duration)
        elif arguments['--sunrise']:
            mypwm.modulate(mypwm.pwm_thresholds['sunrise'][0],
                           mypwm.pwm_thresholds['sunrise'][1],
                           duration)
        elif arguments['--noon']:
            duration = float(arguments['--duration']) / 4
            mypwm.modulate(mypwm.pwm_thresholds['noon'][0],
                           mypwm.pwm_thresholds['noon'][1]-1,
                           duration)
            mypwm.modulate(mypwm.pwm_thresholds['noon'][1]-1,
                           mypwm.pwm_thresholds['noon'][1],
                           duration)
            mypwm.modulate(mypwm.pwm_thresholds['noon'][1],
                           mypwm.pwm_thresholds['noon'][1]-1,
                           duration)
            mypwm.modulate(mypwm.pwm_thresholds['noon'][1]-1,
                           mypwm.modulation.light_thresholds['noon'][2],
                           duration)
        elif arguments['--sunset']:
            mypwm.modulate(mypwm.pwm_thresholds['sunset'][0],
                           mypwm.pwm_thresholds['sunset'][1],
                           duration)
        elif arguments['--dusk']:
            mypwm.modulate(mypwm.pwm_thresholds['dusk'][0],
                           mypwm.pwm_thresholds['dusk'][1],
                           duration)
        elif arguments['-v']:
            print(__name__.__version__)


if __name__ == '__main__':
    main()
