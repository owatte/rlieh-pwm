#!/usr/bin/env python3
# -*- coding: utf-8 -*-

# @Author: Olivier Watté <user>
# @Date:   2017-04-26T04:42:30-04:00
# @Email:  owatte@ipeos.com
# @Last modified by:   user
# @Last modified time: 2017-07-25T11:07:19-04:00
# @License: GPLv3
# @Copyright: IPEOS I-Solutions


"""PWM management for RLIEH systems:

Usage:
  rlieh-pwm (on|off) GPIO
  rlieh-pwm set VALUE GPIO
  rlieh-pwm range BEGIN END --duration=<minutes> GPIO
  rlieh-pwm fx-light (--dawn|--sunrise|--noon|--sunset|--dusk)
           --duration=<minutes> GPIO
  rlieh-pwm (-h | --help)
  rlieh-pwm (-v |--version)

Arguments:
  GPIO        Raspberry Pi GPIO pin
  VALUE       Percent of modulation
              minimal value = 0.01, power Off = 0, power On = 100
  duration    Duration of effect in minutes (0.25 = 15 seconds)

Options:
  -h --help
  -v --version  verbose mode
  --sunrise     smoothy light on, like during the sunrise
  --sunset      smoothy light off, like during the sunset

Tip: use an alias to set a default GPIO (eg. alias light='rlieh-pwm $@ 18')

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
    mypwm = RliehPWM(arguments['GPIO'])

    if arguments['set']:
        mypwm.pwm = arguments['VALUE']
    elif arguments['on']:
        mypwm.pwm = 100
    elif arguments['off']:
        mypwm.pwm = 0
    elif arguments['range']:
        mypwm.modulate(float(arguments['BEGIN']),
                       float(arguments['END']),
                       float(arguments['--duration']))
    # fx-light --dawn|--sunrise|--noon|--sunset|--dusk
    elif arguments['fx-light']:
        if arguments['--dawn']:
            mypwm.modulate(mypwm.modulation_thresholds['dawn'][0],
                           mypwm.modulation_thresholds['dawn'][1],
                           float(arguments['--duration']))
        elif arguments['--sunrise']:
            mypwm.modulate(mypwm.modulation_thresholds['sunrise'][0],
                           mypwm.modulation_thresholds['sunrise'][1],
                           float(arguments['--duration']))
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
                           float(arguments['--duration']))
        elif arguments['--dusk']:
            mypwm.modulate(mypwm.modulation_thresholds['dusk'][0],
                           mypwm.modulation_thresholds['dusk'][1],
                           float(arguments['--duration']))


if __name__ == '__main__':
    main()
