from wpilib.command import Command


class DepositGear(Command):

    def __init__(self, robot):
        super().__init__()
        self.robot = robot
        self.requires(self.robot.gear_manipulator)

    def initialize(self):
        self.robot.gear_manipulator.open()

    def execute(self):
        pass

    def isFinished(self):
        return False  # Runs until interrupted

    def end(self):
        self.robot.gear_manipulator.close()

    def interrupted(self):
        self.end()
