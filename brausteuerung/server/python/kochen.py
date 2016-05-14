from time import sleep, time
from python import database
import sqlite3

class kochen():
    def __init__(self, engines, sensors, dc, db):
        self.engines = engines
        self.sensors = sensors
        self.dc = dc
        self.koch_status = "warte..."
        #Datenbank wird initialisiert
        db_user = "kochen"
        db_pwd = "kochen"
        self.db = database.database(db_user,db_pwd,db)
    def kalibrieren(self):
        # Hier werden die Temperaturen ermittelt.
        # Dabei wird die Testfluessigkeit immer maximal erhitzt und dann wird die Einstellung versucht zu ermitteln,
        # um die Temperatur zu halten

        #Datenbank wird entfernt, falls sie schon existiert
        sql = "DROP TABLE IF EXISTS newton"
        self.db.sql_command(sql)
        #Datenbank fuer die Daten wird initialisiert
        sql = "CREATE TABLE IF NOT EXISTS newton (name TEXT, xwerte TEXT, ywerte TEXT)"
        self.db.sql_command(sql)
        test_temps = [30, 40, 50, 60, 70, 80, 90, 99]
        #Hier werden die ermittelten Daten eingetragen
        daten = []
        #Alle Temperaturen werden gecheckt
        for steps in range(0, 8):
            ziel_temp = float(test_temps[steps])
            current_temp = self.get_middle_temp()
            #Alle Motoren werden voll aufgedreht
            self.engines_on_full()
            #Laeuft solange die Temperatur noch nicht erreicht wurde
            while ziel_temp>current_temp:
                self.koch_status = "Warten bis Zieltemperatur erreicht wurde."
                self.dc.put(["kalibrieren", [round(current_temp, 2), ziel_temp, self.get_engine_position_prozent(), self.koch_status]])
                sleep(10)
                #print current_temp
                current_temp = self.get_middle_temp()
            #Alle Motoren werden abgedreht
            self.engines_out_full()
            #Laufvariable
            zeit1 = time()
            zeit2 = time()
            last_temp = current_temp
            self.koch_status = "Zieltemperatur erreicht."
            #Die Temperatur soll 10 Minuten gehalten werden
            while abs(zeit2-zeit1)<120:
                sleep(4)
                #Aktuelle Zeit wird ermittelt
                zeit2 = time()
                current_temp = self.get_middle_temp()
                self.koch_status = "Zieltemperatur seit %s Sekunden gehalten" % round(abs(zeit1-zeit2))
                #Temperatur ist gesunken
                if (ziel_temp-current_temp)>0.1:
                    #Vergangene Zeit wird zurueckgesetzt
                    zeit1 = time()
                    self.engines_on_seq()
                    self.koch_status = "Temperatur zu nierdrig"
                    #print ("too much: ?", current_temp)
                #Temperatur ist gestiegen
                elif (current_temp-ziel_temp)>0.1:
                    #Vergangene Zeit wird zurueckgesetzt
                    zeit1 = time()
                    self.engines_out_seq()
                    self.koch_status = "Temperatur zu hoch"
                    #print ("too less: ?", current_temp)
                else:
                    if(last_temp-current_temp)>0 and (ziel_temp-current_temp)>0:
                        self.engines_on_seq()
                    elif(last_temp-current_temp)<0 and (ziel_temp-current_temp)<0:
                        self.engines_out_seq()
                last_temp = current_temp
                #Rueckgabe an den Client:
                self.dc.put(["kalibrieren", [round(current_temp, 2), ziel_temp, self.get_engine_position_prozent(), self.koch_status]])
            daten.append([ziel_temp, self.get_engines_position()])
        ergebnis = self.div_diff(daten)
        print ergebnis
        #Daten werden in die Datenbank geschrieben:
        sql = "INSERT INTO newton (name, xwerte, ywerte) VALUES ('%s', '%s', '%s')" % (ergebnis[0], ergebnis[1], ergebnis[2])
        self.db.sql_command(sql)
    #Newton Verfahren - Die Koeffizienten werden berechnet
    def div_diff(self,daten):
        counter = len(daten[0][1])
        ergebnis = []
        for xx in range(counter):
            x = []
            y = []
            y.append([])
            name = daten[0][1][xx][0]
            for xy in range(len(daten)):
                x.append(daten[xy][0])
                y[0].append(daten[xy][1][xx][1])
            #Dividierende Differenz
            for n in range(1, len(daten)):
                y.append([])
                for o in range(len(daten)-n):
                    y[n].append((float(y[n-1][o+1])-float(y[n-1][o]))/(float(x[o+1]) - float(x[o])))
            ergebnis.append((name, x, y))
    #Ergebnis wird als List zurueck gegeben. Dabei steht jeder EIntrag fuer einen Motor. [0]= Name , [1] = Xwerte, [2] = Ywerte
        return ergebnis
    #Newton Verfahren - Zu einem beliebigen x (value) wird eine Position berechnet und gerundet zurueckgegeben
    def newton_pol(self, value, x,y):
        ergebnis = y[0][0]
        for a in range(1,len(y)):
            ze = 1
            for b in range(0,a):
                ze = ze*(value - x[b])
            ergebnis +=y[a][0]*ze
        return round(ergebnis)
#Mittlere Temperatur wird ermittelt
    def get_middle_temp(self):
        temp = 0
        for x in range(len(self.sensors)):
            temp += float(self.sensors[x].temperatur)
        return (temp/len(self.sensors))
#Alle Motoren werden voll aufgedreht
    def engines_on_full(self):
        for x in range(len(self.engines)):
            self.engines[x].engine_on()
#Alle Motoren werden ein Stueck weiter auf gedreht
    def engines_on_seq(self):
        for x in range(len(self.engines)):
            self.engines[x].set_engine_position(1, 0)
#Alle Motoren werden voll abgedreht
    def engines_out_full(self):
        for x in range(len(self.engines)):
            self.engines[x].engine_out()
#Alle Motoren werden ein Stueck zurueck gedreht
    def engines_out_seq(self):
        for x in range(len(self.engines)):
            self.engines[x].set_engine_position(-1, 0)
#Aktuelle Position der Motoren wird erfasst
    def get_engines_position(self):
        position = []
        for x in range(len(self.engines)):
            position.append([self.engines[x].name, self.engines[x].current_position])
        return position
#Aktuelle Position in Prozent angeben.
    def get_engine_position_prozent(self):
        position = 0
        for x in range(len(self.engines)):
            position += self.engines[x].current_position_prozent
        return round(position/len(self.engines))
