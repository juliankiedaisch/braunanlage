from time import sleep
import RPi.GPIO as GPIO
from python import database

class engine ():
    def __init__(self, gpios, engine, dc):
        #Datenbank fuer die motorsteuerung
        self.engine_db = "engine.db"
        self.engine = engine
        # Verwendete Pins am Rapberry Pi
        #A=22
        #B=23
        #C=24
        #D=25
        self.A = gpios[0]
        self.B = gpios[1]
        self.C = gpios[2]
        self.D = gpios[3]
        self.time = 0.002
        self.dc = dc
        self.db = database.database(self.engine_db)
		#Tables werden erstellt, falls sie noch nicht existiert:
        sql = "CREATE TABLE IF NOT EXISTS engines (id INTEGER PRIMARY KEY, name TEXT, current_position INTEGER, max_position INTEGER, min_position INTEGER)"
        self.db.sql_command(sql)
		#Der Motor wird eingetragen, falls er noch nicht existiert
        sql = "INSERT INTO engines (name,current_position, max_position, min_position) SELECT '%s', '%s', 0, 0 WHERE NOT EXISTS(SELECT 1 FROM engines WHERE name = '%s')" % (self.engine, 0, self.engine)
        self.db.sql_command(sql)
		#ID des Motors wird abgefragt
        sql = "SELECT id, min_position, max_position FROM engines WHERE name='%s'" % self.engine
        self.db.sql_command(sql)
        fetch = self.db.sql_return()
        self.id = fetch[0]
        self.min_position = fetch[1]
        self.max_position = fetch[2]
    def get_engine_position(self):
        sql = "SELECT current_position FROM engines WHERE id='%s'" % self.id
        self.db.sql_command(sql)
        return self.db.sql_return()[0]
	#Motor drehen lassen
	#p_type=0: Relative Aenderung der Position
	#p_type=1: Absolute Aenderung der Position
    def set_engine_position(self, position, p_type):
        #Aktuelle Position des Motors wird ermittelt
        old = self.get_engine_position()
        #Relative Aenderung
        if p_type==0:
            new = int(old) + int(position)
            #Ist die Aenderung innerhalb der erlaubten Parametern?
            if (new<self.max_position and new>self.min_position):
                sql = "UPDATE engines SET current_position='%s' WHERE id = '%s'" % (new, self.id)
                self.db.sql_command(sql)
                self.roll_engine(old, new)
    	#Absolute Aenderung
        elif p_type==1:
            new = int(position)
            #Ist die Aenderung innerhalb der erlaubten Parametern?
            if (new<self.max_position and new>self.min_position):
                sql = "UPDATE engines SET current_position='%s' WHERE id = '%s'" % (new, self.id)
                self.db.sql_command(sql)
                self.roll_engine(old, new)

    def set_engine_parameter(self, position, max_min):
        #Aktuelle Position des Motors wird ermittelt
        old = self.get_engine_position()
        #Neue Position wird errechnet
        new = int(old) + int(position)
        #min_position
        if max_min==0:
            sql = "UPDATE engines SET min_position='%s' WHERE id = '%s'" % (new, self.id)
            self.db.sql_command(sql)
            self.roll_engine(old, new)
    	#max_position
        elif max_min==1:
            sql = "UPDATE engines SET max_position='%s' WHERE id = '%s'" % (new, self.id)
            self.db.sql_command(sql)
            self.roll_engine(old, new)
    #GPIOS werden auf Grundeinstellung aktiviert
    def start_GPIOS(self):
        GPIO.setmode(GPIO.BCM)
        GPIO.setup(self.A,GPIO.OUT)
        GPIO.setup(self.B,GPIO.OUT)
        GPIO.setup(self.C,GPIO.OUT)
        GPIO.setup(self.D,GPIO.OUT)
        GPIO.output(self.A, False)
        GPIO.output(self.B, False)
        GPIO.output(self.C, False)
        GPIO.output(self.D, False)
# Schritte 1 - 8 festlegen
    def Step1(self):
        GPIO.output(self.D, True)
        sleep (self.time)
        GPIO.output(self.D, False)
    def Step2(self):
        GPIO.output(self.D, True)
        GPIO.output(self.C, True)
        sleep (self.time)
        GPIO.output(self.D, False)
        GPIO.output(self.C, False)
    def Step3(self):
        GPIO.output(self.C, True)
        sleep (self.time)
        GPIO.output(self.C, False)
    def Step4(self):
        GPIO.output(self.B, True)
        GPIO.output(self.C, True)
        sleep (self.time)
        GPIO.output(self.B, False)
        GPIO.output(self.C, False)
    def Step5(self):
        GPIO.output(self.B, True)
        sleep (self.time)
        GPIO.output(self.B, False)
    def Step6(self):
        GPIO.output(self.A, True)
        GPIO.output(self.B, True)
        sleep (self.time)
        GPIO.output(self.A, False)
        GPIO.output(self.B, False)
    def Step7(self):
        GPIO.output(self.A, True)
        sleep (self.time)
        GPIO.output(self.A, False)
    def Step8(self):
        GPIO.output(self.D, True)
        GPIO.output(self.A, True)
        sleep (self.time)
        GPIO.output(self.D, False)
        GPIO.output(self.A, False)
    def roll_engine(self, old, new):
        schritte = abs(int(old) - int(new))
        #old<new
        if new>old:
            self.start_GPIOS()
            for i in range (schritte):
                self.Step1()
                self.Step2()
                self.Step3()
                self.Step4()
                self.Step5()
                self.Step6()
                self.Step7()
                self.Step8()
                self.dc.data_input( self.name, self.get_engine_position())
            GPIO.cleanup()
        elif new>old:
            self.start_GPIOS()
            for i in range (schritte):
                self.Step8()
                self.Step7()
                self.Step6()
                self.Step5()
                self.Step4()
                self.Step3()
                self.Step2()
                self.Step1()
                self.dc.data_input( self.name, self.get_engine_position())
            GPIO.cleanup()
