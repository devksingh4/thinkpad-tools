#!/usr/bin/env python3
# -*- encoding: utf-8 -*-

"""
Setup tools wrapper
"""

from setuptools import find_packages, setup


setup(
    name='thinkpad_tool',
    maintainer="Dev Singh",
    maintainer_email="devksingh4@gmail.com",
    version='1.0.0',
    description='Tools for ThinkPads',
    platforms=['Linux'],
    keywords='thinkpad trackpoint battery undervolt',
    packages=find_packages(),
    license='GPLv3',
    scripts=['thinkpad-tool']
)
