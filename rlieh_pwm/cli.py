#!/usr/bin/env python3
# -*- coding: utf-8 -*-

# @Author: Olivier Watté <user>
# @Date:   2017-04-26T04:42:30-04:00
# @Email:  owatte@ipeos.com
# @Last modified by:   user
# @Last modified time: 2017-07-31T05:58:43-04:00
# @License: GPLv3
# @Copyright: IPEOS I-Solutions


"""PWM management for RLIEH systems:

Usage:
  rlieh-pwm (on|off) GPIO [--log-level=LOG_LEVEL] [--log-path=LOG_FILE_PATH]
  rlieh-pwm set VALUE GPIO [--log-level=LOG_LEVEL] [--log-path=LOG_FILE_PATH]
  rlieh-pwm range BEGIN END GPIO [--duration=MINUTES] [--log-level=LOG_LEVEL]
            [--log-path=LOG_FILE_PATH]
  rlieh-pwm fx-light (--dawn|--sunrise|--noon|--sunset|--dusk) GPIO
            [--duration=MINUTES] [--log-level=LOG_LEVEL]
            [--log-path=LOG_FILE_PATH]
  rlieh-pwm (-h |--help)
  rlieh-pwm (-v |--version)

Arguments:
  GPIO        Raspberry Pi GPIO pin
  VALUE       Percent of modulation
              minimal modulation = 0.01, power Off = 0, power On = 100

Options:
  -h --help                 Shows this help and exit.
  -v --version              Shows version number.
  --duration=MINUTES        Duration of effect in minutes.
                            (Default value = 1.0)
  --log-level=LOG_LEVEL     notset, critical, warning, error, info, debug.
                            (Default value = notset)
  --log-path=LOG_FILE_PATH  Set log file path.
                            (Default value = /var/log/rlieh)

Tip:
  Use an alias to set a default GPIO (eg. alias light='rlieh-pwm $@ 18')

RLIEH puts a roXXXing poney in your aquarium and greenhouses
"""


from __future__ import absolute_import
from docopt import docopt

from rlieh_pwm import __version__
from rlieh_pwm.core import RliehPWM

MODULATION_THRESHOLDS = {'dawn': [0, 20],
                         'sunrise': [20, 75],
                         'noon': [75, 100, 75],
                         'sunset': [75, 20],
                         'dusk': [20, 0]}


class MyPWM(RliehPWM):
    def __init__(self, pin, modulation_thresholds=MODULATION_THRESHOLDS):
        super(MyPWM, self).__init__(pin=pin)
        self.modulation_thresholds = modulation_thresholds


def main():
    arguments = docopt(__doc__, version='RLIEH PWM {}'.format(__version__))
    if arguments['--duration']:
        duration = float(arguments['--duration'])
    else:
        duration = float(1.0)
    if arguments['--log-level']:
        log_level = arguments['--log-level'].lower()
    else:
        log_level = 'notset'
    if arguments['--log-path']:
        log_path = arguments['--log-path']
    else:
        log_path = '/var/log/rlieh'
    mypwm = RliehPWM(arguments['GPIO'], log_level=log_level, log_path=log_path)
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
            mypwm.modulate(mypwm.modulation_thresholds['dawn'][0],
                           mypwm.modulation_thresholds['dawn'][1],
                           duration)
        elif arguments['--sunrise']:
            mypwm.modulate(mypwm.modulation_thresholds['sunrise'][0],
                           mypwm.modulation_thresholds['sunrise'][1],
                           duration)
        elif arguments['--noon']:
            duration = float(arguments['--duration']) / 4
            mypwm.modulate(mypwm.modulation_thresholds['noon'][0],
                           mypwm.modulation_thresholds['noon'][1]-1,
                           duration)
            mypwm.modulate(mypwm.modulation_thresholds['noon'][1]-1,
                           mypwm.modulation_thresholds['noon'][1],
                           duration)
            mypwm.modulate(mypwm.modulation_thresholds['noon'][1],
                           mypwm.modulation_thresholds['noon'][1]-1,
                           duration)
            mypwm.modulate(mypwm.modulation_thresholds['noon'][1]-1,
                           mypwm.modulation.light_thresholds['noon'][2],
                           duration)
        elif arguments['--sunset']:
            mypwm.modulate(mypwm.modulation_thresholds['sunset'][0],
                           mypwm.modulation_thresholds['sunset'][1],
                           duration)
        elif arguments['--dusk']:
            mypwm.modulate(mypwm.modulation_thresholds['dusk'][0],
                           mypwm.modulation_thresholds['dusk'][1],
                           duration)
        elif arguments['-v']:
            print(__name__.__version__)


if __name__ == '__main__':
    main()
