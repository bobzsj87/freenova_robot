import RPi.GPIO as GPIO
import time

class Line_Tracking:
    def __init__(self):
        self.IR01 = 16
        self.IR02 = 20
        self.IR03 = 21
        GPIO.setmode(GPIO.BCM)
        GPIO.setup(self.IR01, GPIO.IN)
        GPIO.setup(self.IR02, GPIO.IN)
        GPIO.setup(self.IR03, GPIO.IN)

    def run(self):
        while True:
            self.LMR=0x00
            if GPIO.input(self.IR01)==True:
                self.LMR=(self.LMR | 4)
            if GPIO.input(self.IR02)==True:
                self.LMR=(self.LMR | 2)
            if GPIO.input(self.IR03)==True:
                self.LMR=(self.LMR | 1)
            print("{0:3b}".format(self.LMR))
            time.sleep(0.1)
            
# Main program logic follows:
if __name__ == '__main__':
    print ('Program is starting ... ')
    infrared=Line_Tracking()
    try:
        infrared.run()
    except KeyboardInterrupt:  # When 'Ctrl+C' is pressed, the child program  will be  executed.
        print ("\nEnd of program")
