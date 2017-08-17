# RLIEH PWM

This module is intended to provide an interface to manage PWM on RLIEH systems.

Rlieh-pwm is a part of the [RLIEH project](http://www.lebiklab.com/portfolio/rlieh/)
and can be used on a Raspberry Pi.

## Prerequisites

This module relies on [pi-blaster project](https://github.com/hybridgroup/pi-blaster) providing 8_PWM channels at a 100Hz PWM frequency and 1000 PWM steps.

### Default supported GPIO pins

    GPIO number  Pin P1 header
    4              P1-7
    17             P1-11
    18             P1-12
    21             P1-13
    22             P1-15
    23             P1-16
    24             P1-18
    25             P1-22

## Install

### From source

```
git clone https://github.com/owatte/rlieh-pwm.git
cd rlieh-pwm
python3 setup.py install
```
### From pip

```
pip3 install rlieh-pwm
```
## Usage

### as Py module
```python
  >>> from rlieh_pwm.core import RliehPWM
  >>> light = RliehPWM(pin=18)
  >>> light.pwm = 0.420
  >>> light.modulate(0.1, 80, duration=0.5)
```

### as CLI tool
```bash
  $ rlieh-pwm set 0.42 18, duration=0
  $ rlieh-pwm range 0.1 80 18 --duration=0.5
```

The CLI tool code shows a use case with LEDs to make some special effects such as
dusk, dawn, sunrise, sunset or even a thunderstorm with lightening effect.

```bash
rlieh@raspberry:~ $ rlieh-pwm -h
PWM management for RLIEH systems:

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

```
## Licence

Released under The [GPL v3 License](COPYING.md).

Copyright (C) 2017 Olivier Watte
