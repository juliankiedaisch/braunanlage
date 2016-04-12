from python import database
import sqlite3

class biertyp():
    def __init__(self, db):
        self.db = database.database(db)
        sql = "CREATE TABLE IF NOT EXISTS biertypen (id INTEGER PRIMARY KEY, name TEXT)"
        self.db.sql_command(sql)
    def delet_biertyp(self, id):
        sql = "DELETE FROM biertypen WHERE id='%s'" % id
        self.db.sql_command(sql)
    def add_biertyp(self, name):
        sql = "INSERT INTO biertypen (name) SELECT '%s' WHERE NOT EXISTS(SELECT 1 FROM biertypen WHERE name = '%s')" % (name, name)
        self.db.sql_command(sql)



class rezept():

    def __init__(self, db):
    #Verbindung zur Datenbank wird aufgebaut
        self.db = database.database(db)
    #Table fuer die Rezepte wird eingerichtet
        sql = "CREATE TABLE IF NOT EXISTS rezept (id INTEGER PRIMARY KEY, name TEXT, biertyp INTEGER, kochzeit INTEGER, nachguss INTEGER)"
        self.db.sql_command(sql)
    #Table fuer die Maischphasen wird eingerichtet
        sql = "CREATE TABLE IF NOT EXISTS maischphasen (id INTEGER PRIMARY KEY, rezept_id INTEGER, zeit INTEGER, temperatur INTEGER)"
        self.db.sql_command(sql)
    #Table fuer die Hopfenbeigabe wird eingerichtet
        sql = "CREATE TABLE IF NOT EXISTS hopfenzugabe (id INTEGER PRIMARY KEY, rezept_id INTEGER, zeit INTEGER, name TEXT)"
        self.db.sql_command(sql)

    def neues_rezept(self, data):
        biertyp = data[0]
        biername = data[1]
        maischphasen = data[2]
        nachguss = data[3]
        kochzeit = data[4]
        hopfenzugabe = data[5]
    #Der erste Eintrag in rezept wird gemacht, um danach die ID zu bekommen fuer Maisch und Hopfenphasen
        sql = "INSERT INTO rezept (name, biertyp, kochzeit, nachguss) VALUES ('%s', '%s', '%s', '%s')" % (biername, biertyp, kochzeit, nachguss)
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
        for x in range(len(hopfenzugabe)):
            sql = "INSERT INTO hopfenzugabe (rezept_id, zeit, name) VALUES ('%s', '%s', '%s')" % (rezept_id, hopfenzugabe[x][0], hopfenzugabe[x][1])
            self.db.sql_command(sql)

    #TEST
        sql = "SELECT * FROM rezept"
        self.db.sql_command(sql)
        print self.db.sql_return()
        sql = "SELECT * FROM maischphasen"
        self.db.sql_command(sql)
        for row in self.db.sql_return_all():
            for x in range(len(row)):
                print row[x]
        sql = "SELECT * FROM hopfenzugabe"
        self.db.sql_command(sql)
        for row in self.db.sql_return_all():
            for x in range(len(row)):
                print row[x]
