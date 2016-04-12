import ow
import time
import sqlite3
from python import database
import threading

class sensor(threading.Thread):
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
        #Datenbank wird initialisiert
        self.db = database.database(db)
		#Tables werden erstellt, falls sie noch nicht existiert:
        sql = "CREATE TABLE IF NOT EXISTS sensors (id INTEGER PRIMARY KEY, name TEXT, temperatur REAL)"
        self.db.sql_command(sql)
		#Der Sensor wird eingetragen, falls er noch nicht existiert
        sql = "INSERT INTO sensors (name, temperatur) SELECT '%s', 0 WHERE NOT EXISTS(SELECT 1 FROM sensors WHERE name = '%s')" % (self.sensor_name, self.sensor_name)
        self.db.sql_command(sql)
        #ID des Sensors wird abgefragt
        sql = "SELECT id FROM sensors WHERE name='%s'" % self.sensor_name
        self.db.sql_command(sql)
        fetch = self.db.sql_return()
        self.id = fetch[0]
        #Thread wird gestartet
        threading.Thread.__init__(self)
    def get_sensor_liste(self):
        return  ow.Sensor("/").sensorList()
    def get_sensor(self, sensor, sensorlist):
        for item in sensorlist[:]:
            if item.r_address != sensor:
                sensorlist.remove( item )
        return sensorlist
    def run(self):
        sensor = self.get_sensor(self.sensor_adr, self.get_sensor_liste())
        while True:
            value = sensor[0].temperature
            self.temperatur = round(float(value),1)
            sql = "UPDATE sensors SET temperatur='%s' WHERE id = '%s'" % (self.temperatur, self.id)
            self.db.sql_command(sql)
            time.sleep(1)
#warten bis alle Dienste gestartet sind
time.sleep(60)
up = sensor("temp_up", "500000071D4C0328", "sensors.db")
down = sensor("temp_down","570000071CE8A828", "sensors.db")
up.start()
down.start()
