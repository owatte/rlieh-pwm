#!/usr/bin/env python
# -*- coding: utf-8 -*-

from setuptools import setup, find_packages

import rlieh_leds

setup(
    name='rlieh_leds',
    version=rlieh_leds.__version__,
    packages=find_packages(),
    author="Olivier Watté - RLIEH project",
    author_email="owatte@emnet.cc",
    description="This module provides an interface to manage leds light-system",
    long_description=open('README.md').read(),
    include_package_data=True,
    url='http://github.com/owatte/rlieh_leds',
    classifiers=[
        "Programming Language :: Python",
        "Development Status :: 3 - Alpha",
        "License :: OSI Approved :: GNU General Public License v3 or later (GPLv3+)",
        "Natural Language :: English",
        "Operating System :: OS Independent",
        "Programming Language :: Python :: 3",
        "Topic :: Scientific/Engineering",
    ],
    entry_points = {
        'console_scripts': [
            'rlieh-leds = rlieh_leds.cli',
        ],
    },
    install_requires=[
          'docopt',
      ],
)
