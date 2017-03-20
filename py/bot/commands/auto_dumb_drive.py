from wpilib.command import Command
from wpilib.timer import Timer


class AutoDumbDrive(Command):

    def __init__(self, robot, time=0, speed=0.5, dont_stop=False):
        super().__init__()
        self.robot = robot
        self.requires(self.robot.drive_train)

        self.time = time
        self.speed = speed
        self.dont_stop = dont_stop

    def initialize(self):
        print('start auto_dumb_driving', self.speed, self.time, Timer.getFPGATimestamp())
        self.start_time = Timer.getFPGATimestamp()

    def execute(self):
        # if self.isFinished():
        #     print('exec is finished')
        #     self.robot.drive_train.drive(0, 0)
        # else:
        self.robot.drive_train.drive(self.speed, 0)

    def isFinished(self):
        if self.dont_stop:
            return False

        # print('check_done', Timer.getFPGATimestamp())
        return Timer.getFPGATimestamp() - self.start_time > \
            self.time

    def end(self):
        print('end auto dumb', self.speed, Timer.getFPGATimestamp())
        self.robot.drive_train.stop()

    def interrupted(self):
        print('interrupted auto')
        self.end()
