from time import sleep
import RPi.GPIO as GPIO

class gpio_manager():

    def __init__(self):
        self.engines = []
    def start_progress(self, name):
        if name in self.engines:
            return False
        else:
            self.engines.append(name)
            return True
    def end_progress(self, name):
        self.engines.remove(name)
        if len(self.engines) == 0:
            GPIO.cleanup()
    def is_in_progress(self, name):
        if name in self.engines:
            return False
        else:
            return True

class engine ():
    def __init__(self, gpios, engine, dc, gpiomanager):
        self.name = engine
        self.gpiomanager = gpiomanager
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
    def roll_engine(self, schritte):
    #Solange noch ein weiterer Prozess laeuft, soll gewartet werden
        while(self.gpiomanager.start_progress(self.name)==False):
            sleep(0.1)
        #Position fuer die Schrittweise uebergabe an den Clienten und die db
        position = 0
        #old<new
        if schritte>0:
            self.start_GPIOS()
            for i in range (abs(schritte)):
                self.Step1()
                self.Step2()
                self.Step3()
                self.Step4()
                self.Step5()
                self.Step6()
                self.Step7()
                self.Step8()
                #Aktuelle Position wird eingetragen
                position += 1
        elif schritte<0:
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
                #Aktuelle Position wird eingetragen
                position -= 1

        self.gpiomanager.end_progress(self.name)
        return position
