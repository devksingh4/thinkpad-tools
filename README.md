# Thinkpad Tools
Tools created to manage thinkpad properties

## Currently Supported Properties
* Adjusting Trackpoint Speed and Sensitivity
* Managing battery/batteries
  * Setting Charge Stop and Start thresholds
  * Checking battery health (cli tool not working but working in scripts)

## Planned Supported Properties

* Undervolting CPU
* Replicate other features present in Lenovo Vantage!

While most of these tools exist seperately, it would be nice to have a first-class linux tool that allows all of the above to be managed all in one place. This is why I started development on thinkpad-tools. 

## Installing Utility
There are 2 ways to install the utility; using setup.py or the distribution package

### Setup.py
Run `python3 setup.py install` after cloning the repository (`git clone https://github.com/devksingh4/thinkpad-tools`). 

### Ubuntu/Debian
While a PPA is in the works, you can download the .deb file and install it with `sudo dpkg -i python3-thinkpad-tool.deb`. The package name is `python3-thinkpad-tool` once installed. 

### Other platforms
Use the setup.py method above
