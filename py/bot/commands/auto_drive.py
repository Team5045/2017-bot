from wpilib.command import Command
from wpilib import Timer


class AutoDrive(Command):

    def __init__(self, robot, distance=float('inf'), speed=1, dont_stop=False):
        super().__init__()
        self.robot = robot
        self.requires(self.robot.drive_train)

        self.distance = distance
        self.speed = speed
        self.dont_stop = dont_stop

    def initialize(self):
        self.robot.drive_train.reset_auto_drive()
        self.robot.drive_train.set_max_speed(self.speed)
        self.execute()
        Timer.delay(0.02)  # Wait for signal to be sent

    def execute(self):
        self.robot.drive_train.auto_drive(self.distance)

    def isFinished(self):
        if self.dont_stop:
            return False

        return self.robot.drive_train.get_auto_drive_within_tolerance()

    def end(self):
        print('end autodrive')
        self.robot.drive_train.stop()

    def interrupted(self):
        print('interrupted autodrive')
        self.end()
