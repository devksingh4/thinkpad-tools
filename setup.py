#!/usr/bin/env python3
# -*- encoding: utf-8 -*-

"""
Setup tools wrapper
"""

from setuptools import find_packages, setup
import os
import sys
from shutil import copyfile

setup(
    name='thinkpad-tools',
    maintainer="Dev Singh",
    maintainer_email="dev@singhk.dev",
    version='0.13',
    zip_safe=False,
    description='Tools for ThinkPads',
    long_description="Tools created to manage thinkpad properties such as TrackPoint, Undervolt, and Battery",
    platforms=['Linux'],
    include_package_data=True,
    keywords='thinkpad trackpoint battery undervolt',
    packages=find_packages(),
    project_urls={
        "Bug Tracker": "https://github.com/devksingh4/thinkpad-tools/issues",
        "Documentation": "https://github.com/devksingh4/thinkpad-tools/blob/master/README.md",
        "Source Code": "https://github.com/devksingh4/thinkpad-tools/",
    },
    license='GPLv3',
    scripts=['thinkpad-tools'],
    data_files=[
        ('/etc/', ["thinkpad_tools_assets/thinkpad-tools.ini"]),
        ('/usr/lib/systemd/system/', ["thinkpad_tools_assets/thinkpad-tools.service"]),
        ('/usr/share/licenses/python-thinkpad-tools/', ["LICENSE"])

    ],
)
