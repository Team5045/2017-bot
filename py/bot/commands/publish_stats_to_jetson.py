from wpilib.command import Command


class PublishStatsToJetson(Command):

    def __init__(self, robot):
        super().__init__()
        self.robot = robot
        self.requires(self.robot.jetson)

    def initialize(self):
        pass

    def execute(self):
        navx = self.robot.navx.get_formatted_status()
        self.robot.jetson.put_value('navx_data', navx, valueType='string')

        enc_data = self.robot.drive_train.get_encoder_distance_data()
        self.robot.jetson.put_value('left_encoder', enc_data[0],
                                    valueType='number')
        self.robot.jetson.put_value('right_encoder', enc_data[1],
                                    valueType='number')

        shooter_setpoint = self.robot.shooter.get_flywheel_setpoint()
        self.robot.jetson.put_value('shooter_setpoint', shooter_setpoint,
                                    valueType='number')

        shooter_speed = self.robot.shooter.get_flywheel_speed()
        self.robot.jetson.put_value('shooter_speed', shooter_speed,
                                    valueType='number')

        shooter_error = self.robot.shooter.get_flywheel_error()
        self.robot.jetson.put_value('shooter_error', shooter_error,
                                    valueType='number')

    def isFinished(self):
        return False

    def end(self):
        pass

    def interrupted(self):
        self.end()
