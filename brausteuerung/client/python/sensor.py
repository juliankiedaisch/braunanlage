import ow
import os
import time
from threading import Thread

class sensor(Thread):
    #sensor ist die Adresse des Sensors
    senorlist = []
    location = "localhost:4304"
    ow.init(location)
    def __init__(self, sensor_name, sensor_adr, db):
        #Location wird vorgegeben
        #self.temp_sensor_down = "570000071CE8A828"
        #self.temp_sensor_up = "500000071D4C0328"
        self.sensor_adr = sensor_adr
        self.sensor_name = sensor_name
        #Thread wird gestartet
        Thread.__init__(self)
    def get_sensor_liste(self):
        a=0
        while a==0:
            try:
                return ow.Sensor("/").sensorList()
                a=1
            except:
                os.system("sudo service owserver restart")
                time.sleep(10)
                print "Server wird neu gestartet"
    def get_sensor(self, sensor, sensorlist):
        for item in sensorlist[:]:
            if item.r_address != sensor:
                sensorlist.remove( item )
        return sensorlist
    def run(self):
        sensor = self.get_sensor(self.sensor_adr, self.get_sensor_liste())
        while True:
            value = sensor[0].temperature
            self.temperatur = round(float(value),2)
            time.sleep(1)
#warten bis alle Dienste gestartet sind

#up = sensor("temp_up", "500000071D4C0328", "sensors.db")
#down = sensor("temp_down","570000071CE8A828", "sensors.db")
#up.start()
#down.start()
