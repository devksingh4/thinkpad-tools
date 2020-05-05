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
### Debian/Ubuntu
`.deb` files are available for Debian/Ubuntu on the releases page.
### Fedora/CentOS
A COPR repository has been created for Fedora/CentOS at `https://copr.fedorainfracloud.org/coprs/dsingh/thinkpad-tools/`.
### Other distros
Run `python3 setup.py install` after cloning the repository (`git clone https://github.com/devksingh4/thinkpad-tools`). 

## Supported Devices
While this tool should work for any Core-i (xx10 series and onwards) ThinkPad, the following devices have been tested to work with this tool: 
* T480
* X1 Carbon Gen 7
* T470
* X260

Undervolting is only supported on Skylake or newer Intel CPUs. 

If you have tested this tool to work on more machines, please open a pull request and add it to this list!

## Contribution Copyright Assignment
By contributing to this codebase, you hereby assign copyright in this code to the project, to be licensed under the same terms as the rest of the code.

## Persistence of Settings
Run `thinkpad-tools persistence enable` to enable persistence and see the instructions to set the persistent settings.

## Donating
A few people have reached out to me about donating so I can continue to keep improving on the project. If you would like to donate,  I'm `@Dev-Singh-11` on Venmo and [paypal.me/androstudios](https://paypal.me/androstudios) on Paypal

[![Copr build status](https://copr.fedorainfracloud.org/coprs/dsingh/thinkpad-tools/package/python-thinkpad-tools/status_image/last_build.png)](https://copr.fedorainfracloud.org/a/dsingh/thinkpad-tools/package/python-thinkpad-tools/)
