# Thinkpad Tools
Tools created to manage thinkpad properties

## Currently Supported Properties
* Adjusting Trackpoint Speed and Sensitivity
* Managing battery/batteries
  * Setting Charge Stop and Start thresholds
  * Checking battery health
* Undervolting CPU (Can write values but cannot read them)

## Planned Features
None right now, but feel free to suggest one in issues!

While most of these tools exist seperately, it would be nice to have a first-class linux tool that allows all of the above to be managed all in one place. This is why I started development on thinkpad-tools. 

## Installing Utility
Run `python3 setup.py install` after cloning the repository (`git clone https://github.com/devksingh4/thinkpad-tools`). 


## Contribution Copyright Assignment
By contributing to this codebase, you hereby assign copyright in this code to the project, to be licensed under the same terms as the rest of the code.

## Persistence of Settings
Edit file `/etc/thinkpad-tools-persistence.sh` to set settings. Setting will take effect next reboot, or you can run `systemctl daemon-reload && systemctl restart thinkpad-tools.service` to have them take effect immediately. 

## Donating
A few people have reached out to me about donating so I can continue to keep improving on the project. If you would like to donate,  I'm `@Dev-Singh-11` on Venmo and [paypal.me/androstudios](https://paypal.me/androstudios) on Paypal
