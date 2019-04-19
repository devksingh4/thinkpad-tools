#!/usr/bin/env python3
# -*- encoding: utf-8 -*-

"""
Setup tools wrapper
"""

from setuptools import find_packages, setup


setup(
    name='thinkpad_tool',
    version='0.0.1',
    description='Tools for ThinkPads',
    platforms=['Linux'],
    keywords='thinkpad trackpoint battery',
    packages=find_packages(),
    license='GPLv3',
    scripts=['thinkpad-tool']
)
