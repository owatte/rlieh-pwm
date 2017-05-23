#!/usr/bin/env python
# -*- coding: utf-8 -*-

# @Author: Olivier Watté <user>
# @Date:   2017-04-26T04:39:06-04:00
# @Email:  owatte@ipeos.com
# @Last modified by:   user
# @Last modified time: 2017-05-23T12:40:02-04:00
# @License: GPLv3
# @Copyright: IPEOS I-Solutions


from setuptools import setup, find_packages

import rlieh_pwm

setup(
    name='rlieh_pwm',
    version=rlieh_pwm.__version__,
    packages=find_packages(),
    author="Olivier Watté - RLIEH project",
    author_email="owatte@lebiklab.com",
    description="This module provides an interface to manage PWM on RLIEH systems",
    long_description=open('README.md').read(),
    include_package_data=True,
    url='http://github.com/owatte/rlieh-pwm',
    classifiers=[
        "Programming Language :: Python",
        "Development Status :: 3 - Alpha",
        "Environment :: Console",
        "License :: OSI Approved :: GNU General Public License v3 or later (GPLv3+)",
        "Intended Audience :: Science/Research",
        "Natural Language :: English",
        "Operating System :: OS Independent",
        "Programming Language :: Python :: 3",
        "Topic :: Scientific/Engineering",
    ],
    entry_points = {
        'console_scripts': ['rlieh-pwm=rlieh_pwm.cli:main'],
    },
    install_requires=[
          'docopt',
      ],
)
