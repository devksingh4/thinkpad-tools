#!/bin/bash
sudo rm -rf dist && sudo python3 setup.py sdist && twine upload dist/*