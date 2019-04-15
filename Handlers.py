class Trackpoint(object):
    def __init__(self, sensitivity = False, speed = False):
        self.__sensitivity = sensitivity
        self.__speed = speed
    def setValues(self):
        if self.__sensitivity != False and self.__speed != False:
            tp_sens_file = open("/sys/devices/platform/i8042/serio1/serio2/sensitivity", "w")
            tp_speed_file = open("/sys/devices/platform/i8042/serio1/serio2/speed", "w")
            tp_sens_file.write(self.__sensitivity)
            tp_speed_file.write(self.__speed)
            tp_sens_file.close()
            tp_speed_file.close()
    def getValues(self):
            sensitivity = open("/sys/devices/platform/i8042/serio1/serio2/sensitivity", "r").readline()
            speed = open("/sys/devices/platform/i8042/serio1/serio2/speed", "r").readline()
            return sensitivity, speed
class Battery(object):
    def __init__(self, bat1startthresh = None, bat2startthresh = None, bat1stopthresh = None, bat2stopthresh = None):
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
    def getBatteryThreshold(self):
        try:
            bat1start = open("/sys/class/power_supply/BAT0/charge_start_threshold", "r").readline().strip("\n")
            bat1stop = open("/sys/class/power_supply/BAT0/charge_stop_threshold", "r").readline().strip("\n")
        except FileNotFoundError:
            bat1start = False
            bat1stop = False
        try:
            bat2start = open("/sys/class/power_supply/BAT1/charge_start_threshold", "r").readline().strip("\n")
            bat2stop = open("/sys/class/power_supply/BAT1/charge_stop_threshold", "r").readline().strip("\n")
        except FileNotFoundError:
            bat2start = False
            bat2stop = False
        return bat1start, bat1stop, bat2start, bat2stop