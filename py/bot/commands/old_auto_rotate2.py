from wpilib.command import Command
from wpilib import PIDController


class AutoRotate(Command):

    MIN_SPEED = 0.08
    MAX_SPEED = 0.15
    TOLERANCE = 2  # Degrees

    P_ = 3
    I_ = 0
    D_ = 0
    F_ = 0

    def __init__(self, robot, degrees):
        super().__init__()
        self.robot = robot
        self.requires(self.robot.drive_train)
        self.desired_angle = degrees

    def initialize(self):
        print('auto_rotate#initialize, desired: ', self.desired_angle)
        self.robot.navx.reset()
        self.controller = PIDController(self.P_, self.I_, self.D_, self.F_,
                                        self.get_pid_source,
                                        self.set_pid_output)
        self.controller.setInputRange(-180, 180)
        self.controller.setContinuous(True)
        self.controller.setToleranceBuffer(5)
        self.controller.setSetpoint(self.desired_angle)
        self.controller.enable()

        if self.desired_angle >= 0:
            self.curve = 1
        else:
            self.curve = -1

        # Start not moving
        self.speed = 0

    def get_pid_source(self):
        yaw = self.navx.get_yaw()
        print('get yaw', yaw)
        return yaw

    def set_pid_output(self, speed):
        self.speed = speed

    def is_on_target(self):
        return self.controller.AbsoluteTolerance_onTarget(self.TOLERANCE)

    def execute(self):
        print('auto_rotate#execute, pid speed: {}, avg_err: {}'.format(
              self.speed, self.controller.getAvgError()))
        speed = max(self.MIN_SPEED, min(self.MAX_SPEED, self.speed))  # Clamp
        self.robot.drive_train.drive(speed, self.curve)

    def isFinished(self):
        return self.is_on_target()

    def end(self):
        self.controller.disable()
        self.robot.drive_train.stop()

    def interrupted(self):
        self.end()
