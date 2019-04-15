#!/bin/bash
# exit when any command fails
set -e

# keep track of the last executed command
trap 'last_command=$current_command; current_command=$BASH_COMMAND' DEBUG
# echo an error message before exiting
trap 'echo "\"${last_command}\" command filed with exit code $?."' EXIT

if [[ $EUID -ne 0 ]]; then
   echo "Setup must be run as root" 
   exit 1
fi


echo "Copying stock configuration file..." 
# cp config.ini /etc/thinkpad_tools

echo "Configuration located at /etc/thinkpad_tools/config.ini"
echo ""
echo "Copying handlers and libraries..."
mkdir /usr/lib/ThinkpadTools/
cp Handlers.py /usr/lib/ThinkpadTools/
echo "Finished copying handlers and libraries"
echo ""
echo "Copying startup unit files..."
cp ThinkpadTools.service /lib/systemd/system/
cp service_runner.py /usr/lib/ThinkpadTools/
echo "Copying binaries..."
cp thinkpad-tools.py /usr/bin/
chmod +x /usr/bin/thinkpad-tools.py
echo "Configuring Service..."
systemctl daemon-reload
systemctl enable ThinkpadTools.service
echo "Starting Service..."
systemctl start ThinkpadTools.service
echo "Done!"
