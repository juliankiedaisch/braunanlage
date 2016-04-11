from time import sleep, time
import sqlite3
class kochen():

    def __init__(self, engines, dc):
        self.engines = engines
        self.dc = dc

    def kallibrieren(self):
        #Hier werden die Werte für 30, 40, 50, 60, 70, 80, 90 und 99° ermittelt.
        #Dabei wird die Testflüssigkeit immer maximal erhitzt und dann wird die Einstellung versucht zu ermitteln,
        #um die Temperatur zu halten
        test_temps = [30, 40, 50, 60, 70, 80, 90, 99]
        #Hier werden die ermittelten Daten eingetragen
        daten = []
        #Alle Temperaturen werden gecheckt
