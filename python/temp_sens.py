import time
import sqlite3
from python import database

class sensor():
    def __init__(self, dc, sensor_name, db):
        self.sensor_name = sensor_name
        self.dc = dc
        self.temperatur = 0
        #Datenbank wird initialisiert
        self.db = database.database(db)
        #ID des Sensors wird abgefragt
        sql = "SELECT id FROM sensors WHERE name='%s'" % self.sensor_name
        self.db.sql_command(sql)
        fetch = self.db.sql_return()
        self.id = fetch[0]
    def get_temp(self):
        while True:
            sql = "SELECT temperatur FROM sensors WHERE id='%s'" % self.id
            self.db.sql_command(sql)
            fetch = self.db.sql_return()
            self.temperatur = round(float(fetch[0]),1)
            self.dc.data_input( self.sensor_name, str(self.temperatur))
            time.sleep(1)

#up = sensor("500000071D4C0328")
#down = sensor("570000071CE8A828")
#up.start()
#down.start()
