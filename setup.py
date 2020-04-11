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
    version='0.10.0',
    description='Tools for ThinkPads',
    platforms=['Linux'],
    keywords='thinkpad trackpoint battery undervolt',
    packages=find_packages(),
    license='GPLv3',
    scripts=['thinkpad-tools']
)

print("Will now install the systemd unit service for persistence.")
print("""To set persistent settings, please edit the file
      '/etc/thinkpad-tools-persistence.sh'""")
copyfile("thinkpad-tools.service", "/lib/systemd/system/thinkpad-tools.service")
try:
    f = open("/etc/thinkpad-tools-persistence.sh")
except FileNotFoundError:
    copyfile("thinkpad-tools-persistence.sh", "/etc/thinkpad-tools-persistence.sh")
finally:
    f.close()
os.system('systemctl daemon-reload')
os.system('systemctl enable thinkpad-tools.service')