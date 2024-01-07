from Motor import Motor

from time import sleep

if __name__ == '__main__':
    motor = Motor()
    
    try:
        
        motor.setMotorModel(1000, 1000)
        sleep(3)

        motor.setMotorModel(-1000, -1000)
        sleep(3)
        
        motor.setMotorModel(1000, -1000)
        sleep(2)
    except KeyboardInterrupt:
        motor.stop()
    
    motor.stop()
