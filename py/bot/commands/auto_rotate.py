from wpilib.command import Command
from wpilib import Timer


class AutoRotate(Command):

    def __init__(self, robot, degrees=float('inf'), dont_stop=False):
        super().__init__()
        self.robot = robot
        self.requires(self.robot.drive_train)

        self.degrees = degrees
        self.dont_stop = dont_stop

    def initialize(self):
        self.robot.drive_train.reset_auto_rotate()
        self.execute()
        Timer.delay(0.02)  # Wait for signal to be sent

    def execute(self):
        self.robot.drive_train.auto_rotate(self.degrees)

    def isFinished(self):
        if self.dont_stop:
            return False

        return self.robot.drive_train.get_auto_rotate_within_tolerance()

    def end(self):
        print('end autorotate')
        self.robot.drive_train.stop()

    def interrupted(self):
        print('interrupted autorotate')
        self.end()
