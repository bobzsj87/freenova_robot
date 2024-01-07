import RPi.GPIO as GPIO
import time
import pigpio

class Motor:
    def __init__(self):
        self.pwm1 = 24
        self.pwm2 = 23
        self.pwm3 = 5
        self.pwm4 = 6         
        self.PwmServo = pigpio.pi()
        self.PwmServo.set_mode(self.pwm1, pigpio.OUTPUT) 
        self.PwmServo.set_mode(self.pwm2, pigpio.OUTPUT) 
        self.PwmServo.set_mode(self.pwm3, pigpio.OUTPUT) 
        self.PwmServo.set_mode(self.pwm4, pigpio.OUTPUT)         
        self.PwmServo.set_PWM_frequency(self.pwm1, 50)
        self.PwmServo.set_PWM_frequency(self.pwm2, 50)
        self.PwmServo.set_PWM_frequency(self.pwm3, 50)
        self.PwmServo.set_PWM_frequency(self.pwm4, 50)        
        self.PwmServo.set_PWM_range(self.pwm1, 4095)
        self.PwmServo.set_PWM_range(self.pwm2, 4095)
        self.PwmServo.set_PWM_range(self.pwm3, 4095)
        self.PwmServo.set_PWM_range(self.pwm4, 4095)
    
    def turn_wheel(self, duty, s1, s2):
        duty = max(-4095, min(4095, duty))
        if duty > 0:
            self.PwmServo.set_PWM_dutycycle(s1, 0)
            self.PwmServo.set_PWM_dutycycle(s2, duty)
        else:
            self.PwmServo.set_PWM_dutycycle(s1, abs(duty))
            self.PwmServo.set_PWM_dutycycle(s2, 0)


    def left_Wheel(self, duty):
        self.turn_wheel(duty, self.pwm1, self.pwm2)

    def right_Wheel(self, duty):
        correction = 1

        if abs(duty) > 3000:
            correction = 0.65
        elif abs(duty) > 2000:
            correction = 0.75
        elif abs(duty) > 1000:
            correction = 0.85
        
        duty = duty * correction # hardware bias
        self.turn_wheel(duty, self.pwm3, self.pwm4)

    def setMotorModel(self, duty1, duty2):
        self.left_Wheel(duty1)
        self.right_Wheel(duty2)
        
    def stop(self):
        self.setMotorModel(0, 0)

    def move(self, mode, ftime=0.1, fspeed=2000, ttime=0.1, tspeed=2000, stop=True):
        if mode == 'f':
            self.setMotorModel(fspeed, fspeed)
            time.sleep(ftime)
        elif mode == 'b':
            self.setMotorModel(-fspeed, -fspeed)
            time.sleep(ftime)
        elif mode == 'r':
            self.setMotorModel(tspeed, -tspeed)
            time.sleep(ttime)
        elif mode == 'l':
            self.setMotorModel(-tspeed, tspeed)
            time.sleep(ttime)

        if stop:
            self.stop()


