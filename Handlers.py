class Trackpoint(object):
    def __init__(self, sensitivity, speed):
        self.__sensitivity = sensitivity
        self.__speed = speed
    def setValues(self):
        tp_sens_file = open("/sys/devices/platform/i8042/serio1/serio2/sensitivity", "w")
        tp_speed_file = open("/sys/devices/platform/i8042/serio1/serio2/speed", "w")
        tp_sens_file.write(self.__sensitivity)
        tp_speed_file.write(self.__speed)
        tp_sens_file.close()
        tp_speed_file.close()
class Battery(object):
    def __init__(self, bat1startthresh, bat2startthresh, bat1stopthresh, bat2stopthresh):
        self.bat1_start_thresh = bat1startthresh
        self.bat2_start_thresh = bat2startthresh
        self.bat1_stop_thresh = bat1stopthresh
        self.bat2_stop_thresh = bat2stopthresh
    def getBatteryHealth(self):
        try:
            self.bat1health = round(((int(open("/sys/class/power_supply/BAT0/energy_full", "r").readline()) / int(open("/sys/class/power_supply/BAT0/energy_full_design", "r").readline())) * 100),2)
        except FileNotFoundError:
            self.bat1health = "Not Present"
        try:
            self.bat2health = round(((int(open("/sys/class/power_supply/BAT1/energy_full", "r").readline()) / int(open("/sys/class/power_supply/BAT1/energy_full_design", "r").readline())) * 100),2)
        except FileNotFoundError:
            self.bat2health = "Not Present"
        return self.bat1health, self.bat2health
    def setBatteryThreshold(self):
        try:
            open("/sys/class/power_supply/BAT0/charge_stop_threshold", "w").write(self.bat1_stop_thresh)
            open("/sys/class/power_supply/BAT0/charge_start_threshold", "w").write(self.bat1_start_thresh)
            bat1set = True
        except FileNotFoundError:
            bat1set = False
        try:
            open("/sys/class/power_supply/BAT1/charge_stop_threshold", "w").write(self.bat2_stop_thresh)
            open("/sys/class/power_supply/BAT1/charge_start_threshold", "w").write(self.bat2_start_thresh)
            bat2set = True
        except FileNotFoundError:
            bat2set = False
        return bat1set, bat2set