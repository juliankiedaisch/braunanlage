from time import sleep
import RPi.GPIO as GPIO

class engine():

    def __init__(self, position)
        GPIO.setmode(GPIO.BCM)
        # Verwendete Pins am Rapberry Pi
        #A=22
        #B=23
        #C=24
        #D=25
        self.engin_position = 0
        self.A = position[0]
        self.B = position[1]
        self.C = position[2]
        self.D = position[3]
        self.time = 0.002
        # Pins aus Ausgänge definieren
        GPIO.setup(self.A,GPIO.OUT)
        GPIO.setup(self.B,GPIO.OUT)
        GPIO.setup(self.C,GPIO.OUT)
        GPIO.setup(self.D,GPIO.OUT)
        GPIO.output(self.A, False)
        GPIO.output(self.B, False)
        GPIO.output(self.C, False)
        GPIO.output(self.D, False)

    def get_engine_position(self):
        return self.engin_position
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

    def warm_up(self, schritte)
        for i in range (schritte):
            self.Step1()
            self.Step2()
            self.Step3()
            self.Step4()
            self.Step5()
            self.Step6()
            self.Step7()
            self.Step8()
            self.engin_position += 1
        GPIO.cleanup()

    def cool_down(self, schritte)
        for i in range (schritte):
            self.Step8()
            self.Step7()
            self.Step6()
            self.Step5()
            self.Step4()
            self.Step3()
            self.Step2()
            self.Step1()
            self.engin_position -= 1
        GPIO.cleanup()
