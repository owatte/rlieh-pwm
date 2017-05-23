#!/usr/bin/env python3
# -*- coding: utf-8 -*-

# @Author: Olivier Watté <user>
# @Date:   2017-04-26T04:42:30-04:00
# @Email:  owatte@ipeos.com
# @Last modified by:   user
# @Last modified time: 2017-05-22T18:21:53-04:00
# @License: GPLv3
# @Copyright: IPEOS I-Solutions


"""PWM management for RLIEH systems:

Usage:
  light.py set VALUE GPIO
  light.py (on | off | up | down) [--duration=<minutes>] GPIO
  light.py range BEGIN END --duration=<minutes> GPIO
  light.py fx (--sunrise | --sunset) [--duration=<minutes>] GPIO
  light.py (-h | --help)
  light.py (-v |--version)

Arguments:
  GPIO        Raspberry Pi GPIO pin
  VALUE       Light intensity: number between 0 and 1 (eg. 0.421)
              0 = light off, 1 = light on
  duration    action duration in minutes

Options:
  -h --help
  -v --version  verbose mode
  --sunrise     smoothy light on, like during the sunrise
  --sunset      smoothy light off, like during the sunset

Tip: use an alias to set a default GPIO (eg. alias light='light.py $@ 18')

RLIEH puts a roXXXing poney in your aquarium and greenhouses
"""


from __future__ import absolute_import

from time import sleep
from docopt import docopt
# from rlieh_leds.core import RliehLeds
from .core import RliehPWM

class MyLeds(RliehPWM):
    def __init__(self, pin):
        super(MyLeds, self).__init__(pin=pin)

    def regular_variation(self, duration, ascending=True):
        '''Set regular modulation during duration minutes.'''

        avg_pause_time = self._get_avg_pause_time(duration)
        for i in self._get_range(ascending):
            f = (i/float(1000))
            self.pwm = str(f)
            sleep(avg_pause_time)
        self.variation_out(ascending)

    def range_variation(self, begin, end, duration):
        '''Set variation in range(begin, end) during duration minutes.'''

        if begin == end:
            error_msg = 'Range BEGIN and range START can\'t be equal. {}={}' \
                      .format(begin, end)
            raise ValueError(error_msg)
        elif begin < 0:
            error_msg = 'Range BEGIN must be greater or equal to 0. (was {})' \
                      .format(begin)
            raise ValueError(error_msg)
        elif end > 1000:
            error_msg = 'Range END must be lower or equal to 1000. (was {})' \
                      .format(end)
            raise ValueError(error_msg)
        else:
            steps = abs(end - begin)
        pause_time = self._get_avg_pause_time(duration, steps)
        if end > begin:
            step = 1
            end +=  1
        else:
            step = -1
            end -=  1
        print('begin: ', begin)
        print('end: ', end)
        for i in range(begin, end, step):
            f = i/float(1000)
            self.pwm = str(f)
            sleep(pause_time)

    def progressive_variation(self, duration, ascending=True):
        '''Set progressive variation during duration minutes.

        Note: sleep duration is longer for low light values
        '''
        avg_pause_time = self._get_avg_pause_time(duration)
        for i in self._get_range(ascending):
            f = (i/float(1000))
            print(f)
            self.pwm = str(f)
            if ascending:
                if i < 201:
                    pause_time = avg_pause_time * 3
                elif i > 200 and i < 401:
                    pause_time = avg_pause_time * 2
                elif i > 400 and i < 601:
                    pause_time = avg_pause_time
                elif i > 600 and i < 801:
                    pause_time = avg_pause_time / 2
                else:
                    pause_time = avg_pause_time / 3
            else:
                if i < 201:
                    pause_time = avg_pause_time / 3
                elif i > 200 and i < 401:
                    pause_time = avg_pause_time / 2
                elif i > 400 and i < 601:
                    pause_time = avg_pause_time
                elif i > 600 and i < 801:
                    pause_time = avg_pause_time * 2
                else:
                    pause_time = avg_pause_time * 3
            sleep(pause_time)
        self.variation_out(ascending)

    def _get_range(self, ascending=True):
        '''get iteration range according with chosen order.

        Args:
            ascending (bool): if True starts from 0,
                              if False, starts from self.limit
        '''

        if ascending:
            range_ = range(0, 1000)
        else:
            range_ = range(1000, 0, -1)
        return range_

    def _get_avg_pause_time(self, duration, steps=1000):
        '''get average pause time for giving variation total duration.

        Args:start
            duration (int): total duration in minutes

        Returns:
            integer : average sleep time
        '''
        avg_pause_time = int(duration) * 60. / steps
        return avg_pause_time

    def variation_out(self, ascending):
        '''Manages variation loop out with a full on/off value.

        Args:
            ascending(bool): if True: set light on on variation loop exit,
                             if False: set light off on variation loop exit
        '''
        if ascending:
            self.pwm = str(1)
        else:
            self.pwm = str(0)

def main():
    arguments = docopt(__doc__, version='RLIEH lighting 0.2')

    light = MyLeds(arguments['GPIO'])
    if arguments['--duration'] is None:
        arguments['--duration'] = 1
    if arguments['set']:

        light.pwm = arguments['VALUE']
    elif arguments['on']:
        # light = RliehLeds(pin=18)
        light.pwm = 1
    elif arguments['off']:
        light.pwm = 0
    elif arguments['up']:
        light.regular_variation(arguments['--duration'], ascending=True)
    elif arguments['down']:
        light.regular_variation(arguments['--duration'], ascending=False)
    elif arguments['range']:
        light.range_variation(int(arguments['BEGIN']),
                              int(arguments['END']),
                              int(arguments['--duration'])
        )
    elif arguments['fx']:
        if arguments['--sunrise']:
            light.progressive_variation(arguments['--duration'],
                                        ascending=True)
        elif arguments['--sunset']:
            light.progressive_variation(arguments['--duration'],
                                        ascending=False)

if __name__ == '__main__':
    main()
