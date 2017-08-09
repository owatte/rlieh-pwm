#!/usr/bin/env python
# -*- coding: utf-8 -*-

# @Author: Olivier Watté <user>
# @Date:   2017-04-26T04:39:06-04:00
# @Email:  owatte@ipeos.com
# @Last modified by:   user
# @Last modified time: 2017-08-09T14:51:38-04:00
# @License: GPLv3
# @Copyright: IPEOS I-Solutions

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
    entry_points={
        'console_scripts': ['rlieh-pwm=rlieh_pwm.cli:main'],
    },
    install_requires=[
          'docopt',
      ],
)
