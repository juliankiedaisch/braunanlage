import thread
import time

class test_kochen():

    def __init__ (self,  motoren):
        self.status = 0
        self.sensor = self.return_sensor()
        self.start_test(motoren)
#Temperatursensor wird kreiert:
    def return_sensor(self):
        daten = type("daten", (object,), dict())()
        setattr(daten, "temperatur", float(0))
        return daten
#Jeder Motorstellung wird eine Temperatur zugeordnet
    def stellung_to_temp(self, engine, start_temp, end_temp):
    #Kallibrieren der Motoren, Endtemperatur soll bei Stellung 80% erreicht sein
        motor_temp_stellung = []
        engine_max = engine.max_position
        engine_min = engine.min_position
        gesamt = abs(engine_max-engine_min)
        start = int(engine_min)
        end = int(engine_max)
        daten = type("daten", (object,), dict())()
        #Alle moeglichen Motorstellungen werden abgerufen
        for x in range(start, end+1):
            setattr(daten, str(x), str(float(start_temp + self.get_temp_to_stellung(x-start, gesamt, start_temp, end_temp))))
            print str(float(start_temp + self.get_temp_to_stellung(x, gesamt, start_temp, end_temp)))
        return daten
    def get_temp_to_stellung(self, m_stellung, m_gesamt, t_start, t_end):
        gesamt_motor = m_gesamt
        gesamt_temp = abs((t_start-t_end))
        steigung = float(gesamt_temp)/float(gesamt_motor)
        stellung = int(round(steigung*float(m_stellung)))
        return stellung
    def start_test(self, motoren):
        thread.start_new_thread(self.start_test_thread, (motoren,),)
    def start_test_thread(self, motoren):
    #Informationen ueber die Motoren werden gesammelt, Motorstellung wird einer Temperatur zugeordnet
        motor_list = []
        for x in range(len(motoren)):
            motor_list.extend([self.stellung_to_temp(motoren[x], 18, 100 )])
    #Status wird auf 1 gesetzt
        self.status = 1
    #Temperaturen werden auf 18 Grad gesetzt:
        self.sensor.temperatur = 18
    #Solange der Status 1 ist, wird das Testkochen ausgefuehrt
        while self.status == 1:
            for x in range(len(motor_list)):
                #Motoren sind zu weit eingestellt
                if (float(getattr(motor_list[x], str(motoren[x].current_position)))-(self.sensor.temperatur))>0.1:
                    self.sensor.temperatur += 0.0005*(float(getattr(motor_list[x], str(motoren[x].current_position)))-self.sensor.temperatur)
                elif (float(getattr(motor_list[x], str(motoren[x].current_position)))-(self.sensor.temperatur))<0.1:
                    self.sensor.temperatur += 0.0005*(float(getattr(motor_list[x], str(motoren[x].current_position)))-self.sensor.temperatur)
            time.sleep(4)

    #Motorenstellung mit einer Temperatur gleichsetzen
