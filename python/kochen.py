from time import sleep, time
import sqlite3

class kochen():
    def __init__(self, engines, sensors, dc):
        self.engines = engines
        self.sensors = sensors
        self.dc = dc
        self.koch_status = "warte..."
    def kalibrieren(self):
        # Hier werden die Temperaturen ermittelt.
        # Dabei wird die Testfluessigkeit immer maximal erhitzt und dann wird die Einstellung versucht zu ermitteln,
        # um die Temperatur zu halten
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
            while abs(zeit2-zeit1)<600:
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
            daten.append(self.get_engines_position())
            #print daten
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
            position.append(self.engines[x].current_position)
        return position
#Aktuelle Position in Prozent angeben.
    def get_engine_position_prozent(self):
        position = 0
        for x in range(len(self.engines)):
            position += self.engines[x].current_position_prozent
        return round(position/len(self.engines))
