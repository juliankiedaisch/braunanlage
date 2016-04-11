from time import sleep, time
import sqlite3

class kochen():
    def __init__(self, engines, sensors, dc):
        self.engines = engines
        self.sensors = sensors
        self.dc = dc
    def kallibrieren(self):
        # Hier werden die Temperaturen ermittelt.
        # Dabei wird die Testfluessigkeit immer maximal erhitzt und dann wird die Einstellung versucht zu ermitteln,
        # um die Temperatur zu halten
        test_temps = [30, 40, 50, 60, 70, 80, 90, 99]
        #Hier werden die ermittelten Daten eingetragen
        daten = []
        #Alle Temperaturen werden gecheckt
        for steps in range(0, 8):
            ziel_temp = test_temps[steps]
            current_temp = self.get_middle_temp()
            #Alle Motoren werden voll aufgedreht
            self.engines_on_full()
            #Laeuft solange die Temperatur noch nicht erreicht wurde
            while ziel_temp>current_temp:
                sleep(10)
                print current_temp
                current_temp = self.get_middle_temp()
            #Alle Motoren werden abgedreht
            self.engines_out_full()
            #Laufvariable
            zeit1 = time()
            zeit2 = time()
            #Die Temperatur soll 10 Minuten gehalten werden
            while (zeit1-zeit2)<600:
                sleep(1)
                #Aktuelle Zeit wird ermittelt
                zeit2 = time()
                current_temp = self.get_middle_temp()
                #Temperatur ist gesunken
                if (ziel_temp-current_temp)>0.2:
                    #Vergangene Zeit wird zurueckgesetzt
                    zeit1 = time()
                    self.engines_on_seq()
                    print ("too much: ?", current_temp)
                #Temperatur ist gestiegen
                elif (current_temp-ziel_temp)>0.2:
                    #Vergangene Zeit wird zurueckgesetzt
                    zeit1 = time()
                    self.engines_out_seq()
                    print ("too less: ?", current_temp)
            daten.append(get_engines_position())
            print daten
#Mittlere Temperatur wird ermittelt
    def get_middle_temp(self):
        temp = 0
        for x in range(len(self.sensors)):
            temp += self.sensors[x].temperatur
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
