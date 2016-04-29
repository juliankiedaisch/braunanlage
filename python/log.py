import Queue, time
from python import database

class koch_log():

    def __init__(self, db, rezept_id, engines, sensors):
        self.queue = Queue.Queue()
        self.db = database.database(db)
        self.rezept_id = rezept_id
        self.engines = engines
        self.sensors = sensors
        #Tabelle wird erstellt, falls nicht vorhanden
        sql = "CREATE TABLE IF NOT EXISTS koch_log_id (koch_id INTEGER PRIMARY KEY, start DATETIME DEFAULT CURRENT_TIMESTAMP, ende DATETIME DEFAULT CURRENT_TIMESTAMP)"
        self.db.sql_command(sql)
        #Tabelle wird erstellt, falls nicht vorhanden
        sql = "CREATE TABLE IF NOT EXISTS koch_log (koch_id INTEGER, rezept_id INTEGER, type INTEGER, info TEXT, engines Text, sensors Text, zeit DATETIME DEFAULT CURRENT_TIMESTAMP)"
        self.db.sql_command(sql)
        #Start des Kochvorgangs wird in koch_log_id eingetragen
        sql = "INSERT INTO koch_log_id (start) VALUES ('%s')" % time.time()
        self.db.sql_command(sql)
        #Koch_ID wird abgefragt
        sql = "SELECT last_insert_rowid() FROM koch_log_id"
        self.db.sql_command(sql)
        self.id = self.db.sql_return()[0]
        #types: 0 = Start von Brauvorgang, 1 = Ende von Brauvorgang, 2 = Statusmeldung, 3 = Fehler
        #Erster Eintrag: Start des Brauvorgangs
        sql = "INSERT INTO koch_log (koch_id,rezept_id, type, info, engines, sensors, zeit) VALUES ('%s','%s', '%s', '%s', '%s', '%s', '%s')" % (self.id,self.rezept_id, 0, "Start des Brauvorgangs", self.get_engines_info(), self.get_sensors_info(), time.time())
        self.db.sql_command(sql)
#Ein neuer Eintrag
    def input(self, db_type, db_info):
        sql = "INSERT INTO koch_log (koch_id,rezept_id, type, info, engines, sensors, zeit) VALUES ('%s','%s', '%s', '%s', '%s', '%s', '%s')" % (self.id,self.rezept_id, db_type, db_info, self.get_engines_info(), self.get_sensors_info(), time.time())
        self.db.sql_command(sql)
#Engine-Position hohlen
    def get_engines_info(self):
        daten = []
        for x in range(len(self.engines)):
            daten.append(x)
            daten[x]= {"name" : self.engines[x].name, "position" : self.engines[x].current_position}
        return daten
#Temperatur hohlen
    def get_sensors_info(self):
        daten = []
        for x in range(len(self.sensors)):
            daten.append(x)
            daten[x]= {"name" : self.sensors[x].sensor_name, "temperatur" : self.sensors[x].temperatur}
        return daten
