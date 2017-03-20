from wpilib.command import PIDCommand


class AutoRotate(PIDCommand):

    MIN_SPEED = 0.1
    MAX_SPEED = 0.5
    TOLERANCE = 2  # Degrees

    P_ = 3.0
    I_ = 0.5
    D_ = 0

    def __init__(self, robot, degrees):
        super().__init__(self.P_, self.I_, self.D_, period=.05)
        self.robot = robot
        self.requires(self.robot.drive_train)
        self.desired_angle = degrees

    def initialize(self):
        print('auto_rotate#initialize, desired: ', self.desired_angle)
        self.robot.navx.reset()
        self.robot.navx.reset()
        # self.controller = self.getPIDController()
        self.controller.setInputRange(-180, 180)
        self.controller.setContinuous(True)
        self.controller.setToleranceBuffer(5)
        self.setSetpoint(self.desired_angle)

        if self.desired_angle >= 0:
            self.curve = 1
        else:
            self.curve = -1

        # Start not moving
        self.speed = 0

    def returnPIDInput(self):
        yaw = self.robot.navx.get_yaw()
        print('get yaw', yaw)
        return yaw

    def is_on_target(self):
        return self.controller.AbsoluteTolerance_onTarget(self.TOLERANCE)

    def usePIDOutput(self, speed):
        print('auto_rotate#execute, pid speed: {}, avg_err: {}'.format(
              speed, self.controller.getAvgError()))
        clamped = abs(max(self.MIN_SPEED, min(self.MAX_SPEED, speed)))  # Clamp
        if speed == 0:
            final_speed = 0
        else:
            final_speed = (speed / abs(speed)) * clamped
        print('driving at', final_speed)
        self.robot.drive_train.drive(final_speed, self.curve)

    def isFinished(self):
        return self.is_on_target()

    def end(self):
        self.robot.drive_train.stop()

    def interrupted(self):
        self.end()
