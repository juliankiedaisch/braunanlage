import time
from python import database

class log():
    def __init__(self, db):
        self.db = database.database(db)
        #Tabelle wird erstellt, falls nicht vorhanden
        sql = "CREATE TABLE IF NOT EXISTS koch_log_id (koch_id INTEGER PRIMARY KEY, rezept_id INTEGER, status INTEGER, start DATETIME DEFAULT CURRENT_TIMESTAMP)"
        self.db.sql_command(sql)
        #Tabelle wird erstellt, falls nicht vorhanden
        sql = "CREATE TABLE IF NOT EXISTS koch_log (koch_id INTEGER, type INTEGER, info TEXT, engines Text, sensors Text, zeit DATETIME DEFAULT CURRENT_TIMESTAMP)"
        self.db.sql_command(sql)
#Alle Logs werden aufgelistet
    def log_liste_all(self):
        sql = "SELECT koch_id, biername, name, status, start FROM koch_log_id INNER JOIN rezept ON rezept_id=rezept.id INNER JOIN biertypen ON rezept.biertyp=biertypen.id"
        self.db.sql_command(sql)
        all_return = self.db.sql_return_all()
        data = []
        for row in all_return:
            data2 = []
            for x in range(5):
                data2.extend([str(row[x])])
            if row[4]:
            #Zeit wird auf GMT +1 gesetzt
                data2[x] = str(time.strftime("%d.%m.%Y - %H:%M", time.gmtime(row[4]+60*60*2)))
            data.extend([data2])
        return data
#Gibt eine Liste mit den Log-Dateien zurueck, die von diesem Rezept vorhanden sind
    def log_liste_rezept(self, rezept_id):
        sql = "SELECT koch_id, status, start FROM koch_log_id WHERE rezept_id='%s'" % rezept_id
        self.db.sql_command(sql)
        all_return = self.db.sql_return_all()
        data = []
        for row in all_return:
            data2 = []
            for x in range(3):
                data2.extend([str(row[x])])
            if row[2]:
                data2[x] = str(time.strftime("%d.%m.%Y - %H:%M", time.gmtime(row[2]+60*60*2)))
            data.extend([data2])
        return data
#Gibt den Log eines Brauvorgangs zurueck
    def log_vorgang(self, koch_id):
        sql = "SELECT type, info, engines, sensors, zeit, start FROM koch_log AS C JOIN koch_log_id AS R ON C.koch_id = R.koch_id WHERE C.koch_id='%s'" % koch_id
        self.db.sql_command(sql)
        all_return = self.db.sql_return_all()
        data = []
        for row in all_return:
            data2 = []
            for x in range(6):
                data2.extend([str(row[x])])
            if x==5:
                data2[x] = str(time.strftime("%H:%M:%S", time.gmtime(row[4]-row[5])))
                print data2[x]
            data.extend([data2])
        return data
#loescht alle Loggs
    def delete_log(self,rezept_id):
        sql = "SELECT koch_id FROM koch_log_id WHERE rezept_id=%s" % rezept_id
        self.db.sql_command(sql)
        all_return = self.db.sql_return_all()
        for row in all_return:
            sql="DELETE FROM koch_log WHERE koch_id=%s" % row[0]
            self.db.sql_command(sql)
        #Status wird auf 0 gesetzt - status=geloescht
        sql = "UPDATE koch_log_id SET status=0 WHERE rezept_id=%s" % rezept_id
        self.db.sql_command(sql)
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
        sql = """INSERT INTO koch_log_id (rezept_id, status, start) VALUES ('%s', '%s', %s)""" % (self.rezept_id, 1, time.time())
        self.db.sql_command(sql)
        #Koch_ID wird abgefragt und im return zurueck gegeben
        sql = "SELECT last_insert_rowid() FROM koch_log_id"
        self.db.sql_command(sql)
        return self.db.sql_return()[0]
#Ein neuer Eintrag
    def input_koch_log(self, db_type, db_info):
        sql = """INSERT INTO koch_log (koch_id, type, info, engines, sensors, zeit) VALUES (%r,%r,"%r","%r","%r",%r)""" % (self.id, db_type, db_info, self.get_engines_info(), self.get_sensors_info(), time.time())
        self.db.sql_command(sql)
#Engine-Position hohlen
    def get_engines_info(self):
        daten = []
        for x in range(len(self.engines)):
            daten.append(x)
            daten[x]= [self.engines[x].name, self.engines[x].current_position_prozent]
        return daten
#Temperatur hohlen
    def get_sensors_info(self):
        daten = []
        for x in range(len(self.sensors)):
            daten.append(x)
            daten[x]= [self.sensors[x].sensor_name, self.sensors[x].temperatur]
        return daten
