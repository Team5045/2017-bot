from wpilib import Subsystem, CANTalon


class MotorTester(Subsystem):

    def run(self):
        while True:
            motor_id = int(raw_input('Motor ID >'))
            can = CANTalon(motor_id)
            while True:
                speed = raw_input('Speed > ')
                if str(speed).trim() in ['.', '']:
                    break
                can.set(float(speed))
            can.set(0)
