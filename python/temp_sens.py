import ow
import time

class sensor():
    #sensor ist die Adresse des Sensors
    senorlist = []
    location = "localhost:4304"
    ow.init(location)
    def __init__(self, dc, sensor_name, sensor_adr):
        #Location wird vorgegeben
        
        #self.temp_sensor_down = "570000071CE8A828"
        #self.temp_sensor_up = "500000071D4C0328"
        self.sensor_adr = sensor_adr
        self.sensor_name = sensor_name
        self.dc = dc
        #OW wird initialisiert
    
    def get_sensor_liste(self):
        return  ow.Sensor("/").sensorList()
    def get_sensor(self, sensor, sensorlist):
        for item in sensorlist[:]:
            if item.r_address != sensor:
                sensorlist.remove( item ) 
        return sensorlist
    def get_temp(self):
        sensor = self.get_sensor(self.sensor_adr, self.get_sensor_liste())
        while True:
            value = sensor[0].temperature
            self.dc.data_input( self.sensor_name, str(round(float(value),1)))
            time.sleep(2)
            
#up = sensor("500000071D4C0328")
#down = sensor("570000071CE8A828")
#up.start()
#down.start()