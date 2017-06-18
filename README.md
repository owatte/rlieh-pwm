# RLIEH PWM

This module is intended to provide an interface to manage PWM on RLIEH systems.

rlieh-pwm is a part of the [RLIEH project](http://www.lebiklab.com/portfolio/rlieh/) and can be used on Raspberry Pi.

## Prerequisites

This module relies on [pi-blaster project](https://github.com/hybridgroup/pi-blaster) providing 8 PWM channels at a 100Hz PWM frequency and 1000 PWM steps.

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

### as CLI tool

## Licence
```
  >>> from core import RliehLeds
  >>> light = RliehLeds(pin=18)
  >>> light.pwm = 0.420
```
