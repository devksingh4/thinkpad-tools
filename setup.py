#!/usr/bin/env python3
# -*- encoding: utf-8 -*-

"""
Setup tools wrapper
"""

from setuptools import find_packages, setup
import os
import sys

setup(
    name='thinkpad-tools',
    maintainer="Dev Singh",
    maintainer_email="devksingh4@gmail.com",
    version='0.9.3',
    description='Tools for ThinkPads',
    platforms=['Linux'],
    keywords='thinkpad trackpoint battery undervolt',
    packages=find_packages(),
    license='GPLv3',
    scripts=['thinkpad-tools']
)

print("Will now install the systemd unit service for persistence.")
print("To set persistent settings, please edit the file '/etc/thinkpad-tools-persistence.sh'")
os.system('sudo python3 persistence.py')
