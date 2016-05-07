from python import database, log
import sqlite3
import time

class biertyp():
    def __init__(self, db):
        db_user = "rezept"
        db_pwd = "rezept"
        self.db = database.database(db_user,db_pwd,db)
        sql = "CREATE TABLE IF NOT EXISTS biertypen (id INTEGER PRIMARY KEY, name TEXT)"
        self.db.sql_command(sql)
    #Table fuer die Rezepte wird eingerichtet
        sql = "CREATE TABLE IF NOT EXISTS rezept (id INTEGER PRIMARY KEY, biername TEXT, biertyp INTEGER, kochzeit INTEGER, nachguss INTEGER, erstellung INTEGER)"
        self.db.sql_command(sql)
    def delet_biertyp(self, id):
    #Zuerst wird geschaut, ob der Biertyp noch verwendet wird
        sql = "SELECT * FROM rezept WHERE biertyp='%s'" % id
        self.db.sql_command(sql)
    #Kein Eintrag fuer den Biertyp. Biertyp wird geloescht
        if not self.db.sql_return():
            sql = "DELETE FROM biertypen WHERE id='%s'" % id
            self.db.sql_command(sql)
            return [self.show_all_biertypen(), 1,"Der Biertyp wurde gel&ouml;scht!"]
    #Biertyp wird noch verwendet: Keine Loeschung!
        else:
            return [self.show_all_biertypen(), 2,"Der Biertyp konnte nicht gel&ouml;scht werden, da er immer noch f&uuml;r mindestens ein Rezept verwendet wird. Diese(s) Rezept(e) m&uuml;ssen erst ge&auml;ndert werden bevor der Biertyp gel&ouml;scht werden kann!"]
    def add_biertyp(self, name):
    #Zuerst wird geschaut, ob der Biertyp bereits existiert
        sql = "SELECT * FROM biertypen WHERE name='%s'" % name
        self.db.sql_command(sql)
    #Kein Eintrag fuer den Biertyp. Biertyp wird erstellt!
        if not self.db.sql_return():
            sql = "INSERT INTO biertypen (name) SELECT '%s' WHERE NOT EXISTS(SELECT 1 FROM biertypen WHERE name = '%s')" % (name, name)
            self.db.sql_command(sql)
            return [self.show_all_biertypen(), 1,"Der Biertyp '"+ name +"' wurde erstellt!"]
    #Biertyp existiert bereits. Kein Eintrag
        else:
            return [self.show_all_biertypen(), 2,"Der Biertyp konnte nicht erstellt werden, da es bereits einen Biertyp '"+ name+ "' gibt."]
#Ausgabe fuer den Select wird vorbereitet
    def show_all_biertypen(self):
        sql = "SELECT * FROM biertypen"
        self.db.sql_command(sql)
        all_return = self.db.sql_return_all()
        data = []
        for row in all_return:
            data2 = []
            for x in range(len(row)):
                data2.extend([str(row[x])])
            data.extend([data2])
        return data

class rezept():

    def __init__(self, db):
    #Verbindung zur Datenbank wird aufgebaut
        self.db = database.database(db)
    #Verbindung zum Log wird hergestellt
        self.log = log.log(db)
    #Table fuer die Rezepte wird eingerichtet
        sql = "CREATE TABLE IF NOT EXISTS rezept (id INTEGER PRIMARY KEY, biername TEXT, biertyp INTEGER, kochzeit INTEGER, nachguss INTEGER, erstellung DATETIME DEFAULT CURRENT_TIMESTAMP)"
        self.db.sql_command(sql)
    #Table fuer die Maischphasen wird eingerichtet
        sql = "CREATE TABLE IF NOT EXISTS maischphasen (id INTEGER PRIMARY KEY, rezept_id INTEGER, zeit INTEGER, temperatur INTEGER)"
        self.db.sql_command(sql)
    #Table fuer die Hopfenbeigabe wird eingerichtet
        sql = "CREATE TABLE IF NOT EXISTS hopfenbeigabe (id INTEGER PRIMARY KEY, rezept_id INTEGER, zeit INTEGER, name TEXT)"
        self.db.sql_command(sql)

    def delete_rezept(self, rezept_id):
        print "delete"
    #Alte Maischzeiten werden geloescht
        sql = "DELETE FROM maischphasen WHERE rezept_id='%s'" % rezept_id
        self.db.sql_command(sql)
    #Alte Hopfenbeigaben werden geloescht
        sql = "DELETE FROM hopfenbeigabe WHERE rezept_id='%s'" % rezept_id
        self.db.sql_command(sql)
    #Der Eintrag in rezept wird geloescht
        sql = "DELETE FROM rezept WHERE id='%s'" % rezept_id
        self.db.sql_command(sql)
    #Alle Loggs werden geloescht
        self.log.delete_log(rezept_id)
    #Neue Selectliste wird uebergebenen
        return self.get_rezept_liste()
    def make_rezept(self, data):
        maischphasen = data["maischphasen"]
        hopfenbeigabe = data["hopfenbeigabe"]
    #REZEPT VERAENDERN: Rezept soll veraendert werden
        if self.is_int(data["rezept_id"]) == True:
            print "update"
        #Alte Maischzeiten werden geloescht
            sql = "DELETE FROM maischphasen WHERE rezept_id='%s'" % data["rezept_id"]
            self.db.sql_command(sql)
        #Alte Hopfenbeigaben werden geloescht
            sql = "DELETE FROM hopfenbeigabe WHERE rezept_id='%s'" % data["rezept_id"]
            self.db.sql_command(sql)
        #Der Eintrag in rezept wird geaendert
            sql = "UPDATE rezept SET biername='%s', biertyp='%s', kochzeit='%s', nachguss='%s' WHERE id='%s'" % (data["biername"], data["biertyp"], data["kochzeit"], data["nachguss"], data["rezept_id"])
            self.db.sql_command(sql)
        #Maischphasen eintragen
            for x in range(len(maischphasen)):
                sql = "INSERT INTO maischphasen (rezept_id, zeit, temperatur) VALUES ('%s', '%s', '%s')" % (data["rezept_id"], maischphasen[x][0], maischphasen[x][1])
                self.db.sql_command(sql)
        #Hopfenzugaben werden eingetragen
            for x in range(len(hopfenbeigabe)):
                sql = "INSERT INTO hopfenbeigabe (rezept_id, zeit, name) VALUES ('%s', '%s', '%s')" % (data["rezept_id"], hopfenbeigabe[x][0], hopfenbeigabe[x][1])
                self.db.sql_command(sql)
    #NEUES REZEPT: Es soll ein neuer Eintrag gemacht werden
        else:
            print "new"
        #Der erste Eintrag in rezept wird gemacht, um danach die ID zu bekommen fuer Maisch und Hopfenphasen
            sql = "INSERT INTO rezept (biername, biertyp, kochzeit, nachguss, erstellung) VALUES ('%s', '%s', '%s', '%s', '%s')" % (data["biername"], data["biertyp"], data["kochzeit"], data["nachguss"], time.time())
            self.db.sql_command(sql)
        #Rezept_ID wird abgefragt
            sql = "SELECT last_insert_rowid() FROM rezept"
            self.db.sql_command(sql)
            rezept_id = self.db.sql_return()[0]
        #Maischphasen eintragen
            for x in range(len(maischphasen)):
                sql = "INSERT INTO maischphasen (rezept_id, zeit, temperatur) VALUES ('%s', '%s', '%s')" % (rezept_id, maischphasen[x][0], maischphasen[x][1])
                self.db.sql_command(sql)
                print maischphasen[x][0]
        #Hopfenzugaben werden eingetragen
            for x in range(len(hopfenbeigabe)):
                sql = "INSERT INTO hopfenbeigabe (rezept_id, zeit, name) VALUES ('%s', '%s', '%s')" % (rezept_id, hopfenbeigabe[x][0], hopfenbeigabe[x][1])
                self.db.sql_command(sql)
    #Neue Selectliste wird uebergebenen
        return self.get_rezept_liste()
#Funktion zur ueberpruefung ob ein Wert ein Integer ist
    def is_int(self, value):
        try:
            int(value)
            return True
        except ValueError:
            return False
#REZEPT wird ausgelesen und ausgegeben
    def get_rezept(self, rezept_id):
    #Checken ob rezept_id ein Integer ist
        if self.is_int(rezept_id)==True:
        #Datei fuer den Return wird vorbereitet
            Rezept = {"rezept_id" : {}, "maischphasen" : {}, "hopfenbeigabe": {}, "biertyp" : {}, "biername" : {}, "kochzeit" : {}, "nachguss" : {}}
            sql = "SELECT * FROM rezept WHERE id = '%s'" % rezept_id
            self.db.sql_command(sql)
        #Rezeptinformationen
            daten = self.db.sql_return()
            Rezept["rezept_id"] = rezept_id
            Rezept["biername"] = daten[1]
            Rezept["biertyp"] = daten[2]
            Rezept["kochzeit"] = daten[3]
            Rezept["nachguss"] = daten[4]
        #Hopfenzugaben werden aus der Datenbank gelesen
            sql = "SELECT zeit, name FROM hopfenbeigabe WHERE rezept_id = '%s'" % rezept_id
            self.db.sql_command(sql)
            all_return = self.db.sql_return_all()
            data = []
            for row in all_return:
                data2 = []
                for x in range(len(row)):
                    data2.extend([str(row[x])])
                data.extend([data2])
            Rezept["hopfenbeigabe"] = data
        #Maischzeiten werden aus der Datenbank gelesen
            sql = "SELECT zeit, temperatur FROM maischphasen WHERE rezept_id = '%s'" % rezept_id
            self.db.sql_command(sql)
            all_return = self.db.sql_return_all()
            data = []
            for row in all_return:
                data2 = []
                for x in range(len(row)):
                    data2.extend([str(row[x])])
                data.extend([data2])
            Rezept["maischphasen"] = data
            return Rezept
#Gibt eine Liste fuer den Select raus
    def get_rezept_liste(self):
        sql = "SELECT rezept.id, biername, name, erstellung FROM rezept INNER JOIN biertypen ON rezept.biertyp=biertypen.id"
        self.db.sql_command(sql)
        all_return = self.db.sql_return_all()
        data = []
        for row in all_return:
            data2 = []
            for x in range(3):
                data2.extend([str(row[x])])
            if row[3]:
                data2.extend([str(time.strftime("%d.%B %Y", time.gmtime(row[3])))])
                print str(time.strftime("%d.%B %Y", time.gmtime(row[3])))
            data.extend([data2])
        return data
