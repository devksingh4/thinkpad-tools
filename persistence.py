from shutil import copyfile
import os

copyfile("thinkpad-tools.service", "/lib/systemd/system/thinkpad-tools.service")
copyfile("thinkpad-tools-persistence.sh", "/etc/thinkpad-tools-persistence.sh")
os.system('systemctl daemon-reload')
os.system('systemctl enable thinkpad-tools.service')
