class TrackpointConfig(object):
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
