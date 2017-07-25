#!/usr/bin/env python3
# -*- coding: utf-8 -*-

# @Author: Olivier Watté <user>
# @Date:   2017-04-26T04:42:30-04:00
# @Email:  owatte@ipeos.com
# @Last modified by:   user
# @Last modified time: 2017-07-25T09:27:41-04:00
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
from numpy import arange
from time import sleep

from rlieh_pwm import __version__
from rlieh_pwm.core import RliehPWM

LIGHT_THRESHOLDS = {'dawn': [0, 20],
                   'sunrise': [20, 75],
                   'noon': [75, 100, 75],
                   'sunset': [75, 20],
                   'dusk':[20, 0]
}

class MyLeds(RliehPWM):
    def __init__(self, pin, light_thresholds=LIGHT_THRESHOLDS):
        super(MyLeds, self).__init__(pin=pin)
        self.light_thresholds = light_thresholds


def main():
    arguments = docopt(__doc__, version='RLIEH PWM {}'.format(__version__))

    light = MyLeds(arguments['GPIO'])
    if arguments['set']:
        light.pwm = arguments['VALUE']
    elif arguments['on']:
        light.pwm = 100
    elif arguments['off']:
        light.pwm = 0
    elif arguments['range']:
        light.range_modulation(float(arguments['BEGIN']),
                              float(arguments['END']),
                              float(arguments['--duration'])
        )
    # fx-light --dawn|--sunrise|--noon|--sunset|--dusk
    elif arguments['fx-light']:
        if arguments['--dawn']:
            light.range_modulation(self.light_thresholds['dawn'][0],
                                   self.light_thresholds['dawn'][1],
                                   float(arguments['--duration']))
        elif arguments['--sunrise']:
            light.range_modulation(self.light_thresholds['sunrise'][0],
                                   self.light_thresholds['sunrise'][1],
                                   float(arguments['--duration']))
        elif arguments['--noon']:
            duration = float(arguments['--duration']) / 4
            light.range_modulation(self.light_thresholds['noon'][0],
                                   self.light_thresholds['noon'][1]-1,
                                   duration)
            light.range_modulation(self.light_thresholds['noon'][1]-1,
                                   self.light_thresholds['noon'][1],
                                   duration)
            light.range_modulation(self.light_thresholds['noon'][1],
                                   self.light_thresholds['noon'][1]-1,
                                   duration)
            light.range_modulation(self.light_thresholds['noon'][1]-1,
                                   self.light_thresholds['noon'][2],
                                   duration)
        elif arguments['--sunset']:
            light.range_modulation(self.light_thresholds['sunset'][0],
                                   self.light_thresholds['sunset'][1],
                                   float(arguments['--duration']))
        elif arguments['--dusk']:
            light.range_modulation(self.light_thresholds['dusk'][0],
                                   self.light_thresholds['dusk'][1],
                                   float(arguments['--duration']))

if __name__ == '__main__':
    main()
