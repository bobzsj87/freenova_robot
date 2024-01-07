import RPi.GPIO as GPIO
import time
import socketserver

from motor import Motor
from servo import Servo
from ultrasonic import Ultrasonic


class Robot:
    def __init__(self):        
        self.motor = Motor()
        
        #self.ultra = Ultrasonic()
        
        #time.sleep(0.5)
        self.servo = Servo()
        #self.servo.initialize()
        print('servo initialized')

    
    ''' 
    def run_motor(self, distance):
        if (distance == 0): return

        if distance < 45 :
            self.motor.setMotorModel(-1000, 1000)   #Forward
            #self.stop_motor()
        else :
            self.motor.setMotorModel(SPEED, SPEED)   #Forward
            
    def run(self):
        while True:
            distance = self.get_distance()
            time.sleep(0.1)
            print("The distance is {} cm".format(distance))
            self.run_motor(distance)
    '''

    def stop_motor(self):
        self.motor.setMotorModel(0, 0)

class TCPHandler(socketserver.BaseRequestHandler):
    def __init__(self, request, client_address, server, robot=None):
        self.robot = robot
        super().__init__(request, client_address, server)

    @classmethod
    def Creator(cls, *args, **kwargs):
        def _HandlerCreator(request, client_address, server):
            cls(request, client_address, server, *args, **kwargs)
        return _HandlerCreator

    def handle(self):
        self.data = self.request.recv(1024).strip()
        s = self.data.decode()
        print(s)

        if self.robot is None:
            print('no robot initialized')
            return

        stop = s[-1] != 't'
        
        if s[:-1] == 'w:':
            self.robot.servo.up_down(True)
        elif s[:-1] == 's:':
            self.robot.servo.up_down(False)
        elif s[:-1] == 'a:':
            self.robot.servo.close_open(True)
        elif s[:-1] == 'd:':
            self.robot.servo.close_open(False)
        elif s[:-1] == 'up:':
            self.robot.motor.move('f', stop=stop)
        elif s[:-1] == 'down:':
            self.robot.motor.move('b', stop=stop)
        elif s[:-1] == 'left:':
            self.robot.motor.move('l', stop=stop)
        elif s[:-1] == 'right:':
            self.robot.motor.move('r', stop=stop)
        elif s[:-1] == 'space:':
            self.robot.motor.stop()


    '''
    def finish(self):
        print('{}:{} disconnected'.format(*self.client_address))
    '''


if __name__ == "__main__":
    HOST, PORT = "192.168.31.158", 9998
    robot = Robot()

    try:
        with socketserver.TCPServer((HOST, PORT), TCPHandler.Creator(robot)) as server:
            server.serve_forever()

    except KeyboardInterrupt:
        robot.stop_motor()


