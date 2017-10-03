from wpilib.command import Command
from wpilib import PIDController

DEBUG = True


class AutoRotate(Command):

    MAX_SPEED = 0.3
    TOLERANCE = 0.5  # degrees
    # TOLERANCE_BUFFER = 1  # iterations

    PIDF = (0.1, 0, 0, 0)

    def __init__(self, robot, degrees):
        super().__init__()
        self.robot = robot
        self.requires(self.robot.drive_train)
        self.desired_angle = degrees

    def initialize(self):
        print('auto_rotate#initialize, desired: ', self.desired_angle)
        self.robot.drive_train.reset_auto_drive()

        self.controller = PIDController(*self.PIDF,
                                        source=self.get_pid_source,
                                        output=self.set_pid_output)
        self.controller.setInputRange(-180, 180)
        self.controller.setOutputRange(-self.MAX_SPEED, self.MAX_SPEED)
        self.controller.setContinuous(True)

        # Wrap around
        current_yaw = self.robot.navx.get_yaw()
        goal = current_yaw + self.desired_angle
        if goal > 180:
            goal = goal - 360
        elif goal < -180:
            goal = goal + 360

        self.controller.setSetpoint(goal)
        self.controller.enable()

        # Start not moving
        self.speed = 0

    def get_pid_source(self):
        yaw = self.robot.navx.get_yaw()
        print('yaw', yaw)
        return yaw

    def set_pid_output(self, speed):
        self.speed = speed

    def execute(self):
        if DEBUG:
            print('auto_rotate#execute, pid speed: {}, avg_err: {}'.format(
                  self.speed, self.controller.getAvgError()))

        self.robot.drive_train.drive(self.speed, 1)

    def is_on_target(self):
        return self.controller.AbsoluteTolerance_onTarget(self.TOLERANCE)

    def isFinished(self):
        return self.is_on_target()

    def end(self):
        self.controller.disable()
        self.robot.drive_train.stop()
        print('autorotate', self.desired_angle, 'completed')

    def interrupted(self):
        self.end()
