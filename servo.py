import RPi.GPIO as GPIO
import time
import pigpio
import os

class Servo:
    '''
        0 = clench: 90 = open, 125 = close
        1 = lift: 90 = low, 150 = high

    '''
    def __init__(self):
        self.channels = (7, 8, 25)
        self.PwmServo = pigpio.pi()
        for c in self.channels:
            self.PwmServo.set_mode(c, pigpio.OUTPUT) 
            self.PwmServo.set_PWM_frequency(c, 50)
            self.PwmServo.set_PWM_range(c, 4000)


        self.cur = [-1, -1, -1]
        self._angle_range = {
                0: (70, 125),
                1: (90, 150),
                2: (0, 180)
            }

    def angle_range(self, channel, init_angle):

        ar = self._angle_range[channel]
        return max(ar[0], min(init_angle, ar[1]))
        
    def setServoPwm(self, channel, angle):
        angle = self.angle_range(channel, angle)
        self.PwmServo.set_PWM_dutycycle(self.channels[channel], 80+(400/180)*angle)

        self.cur[channel] = angle

    def move(self, channel, angle):

        if self.cur[channel] == -1:
            # not initialized
            return
        angle = self.angle_range(channel, angle)
        
        #print('channel {} moving to {}'.format(channel, angle))
        
        while self.cur[channel] != angle:
            self.setServoPwm(channel, self.cur[channel] + (1 if angle > self.cur[channel] else -1))
            
            time.sleep(0.01)
            

    def initialize(self):
        self.setServoPwm(0, 90)
        self.setServoPwm(1, 150)


    def up_down(self, up=True):
        channel = 1
        self.setServoPwm(channel, self.cur[channel] + (5 if up else -5))
    
    def close_open(self, close=True):
        channel = 0
        self.setServoPwm(channel, self.cur[channel] + (5 if close else -5))
        

if __name__ == '__main__':
    servo = Servo() 
    servo.initalize()
    
    while True:
        try:
            i = input('input for 0, 1 value:')
            for idx, val in enumerate(i.split()):
                servo.move(idx, int(val))
        except KeyboardInterrupt:
            print('bye!')
            break

