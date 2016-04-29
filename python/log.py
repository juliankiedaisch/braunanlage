import time
from python import database

class log():
    def __init__(self, db):
        self.db = database.database(db)
#Gibt eine Liste mit den Log-Dateien zurueck, die von diesem Rezept vorhanden sind
    def get_log_liste(self, rezept_id):
        sql = "SELECT koch_id, status, start FROM koch_log_id WHERE rezept_id='%s'" % rezept_id
        self.db.sql_command(sql)
        all_return = self.db.sql_return_all()
        data = []
        for row in all_return:
            data2 = []
            for x in range(3):
                data2.extend([str(row[x])])
            if row[3]:
                data2.extend([str(time.strftime("%d.%B %Y", time.gmtime(row[3])))])
            data.extend([data2])
        return data
#Gibt den Log eines Brauvorgangs zurueck
    def get_log_vorgang(self, koch_id):
        sql = "SELECT type, info, engines, sensors, zeit, start FROM koch_log AS C JOIN koch_log_id AS R ON C.koch_id = R.koch_id WHERE koch_id='%s'" % koch_id
        self.db.sql_command(sql)
        all_return = self.db.sql_return_all()
        data = []
        for row in all_return:
            data2 = []
            for x in range(5):
                data2.extend([str(row[x])])
            if row[5]:
                data2.extend([str(time.strftime("%d.%B %Y", time.gmtime(row[3])))])
            data.extend([data2])
        return data
class koch_log():
    def __init__(self, db, rezept_id, engines, sensors):
        self.db = database.database(db)
        self.rezept_id = rezept_id
        self.engines = engines
        self.sensors = sensors
        #Tabelle wird erstellt, falls nicht vorhanden
        sql = "CREATE TABLE IF NOT EXISTS koch_log_id (koch_id INTEGER PRIMARY KEY, rezept_id INTEGER, status INTEGER, start DATETIME DEFAULT CURRENT_TIMESTAMP)"
        self.db.sql_command(sql)
        #Tabelle wird erstellt, falls nicht vorhanden
        sql = "CREATE TABLE IF NOT EXISTS koch_log (koch_id INTEGER, type INTEGER, info TEXT, engines Text, sensors Text, zeit DATETIME DEFAULT CURRENT_TIMESTAMP)"
        self.db.sql_command(sql)
        self.id = self.start_new_koch_log()
        #types: 0 = Start von Brauvorgang, 1 = Ende von Brauvorgang, 2 = Statusmeldung, 3 = Fehler
        #Erster Eintrag: Start des Brauvorgangs
        self.input_koch_log(0,"Start des Brauvorgangs")
    def start_new_koch_log(self):
        #Start des Kochvorgangs wird in koch_log_id eingetragen. Status wird 1 (aktiv) gesetzt
        sql = "INSERT INTO koch_log_id (rezept_id, status) VALUES ('%s', '%s')" % (self.rezept_id, 1)
        self.db.sql_command(sql)
        #Koch_ID wird abgefragt und im return zurueck gegeben
        sql = "SELECT last_insert_rowid() FROM koch_log_id"
        self.db.sql_command(sql)
        return self.db.sql_return()[0]
#Ein neuer Eintrag
    def input_koch_log(self, db_type, db_info):
        sql = "INSERT INTO koch_log (koch_id, type, info, engines, sensors, zeit) VALUES ('%s', '%s', '%s', '%s', '%s', '%s')" % (self.id, db_type, db_info, self.get_engines_info(), self.get_sensors_info(), time.time())
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
