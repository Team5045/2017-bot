from wpilib.command import Command


class DepositGear(Command):

    def __init__(self, robot):
        super().__init__()
        self.robot = robot
        self.requires(self.robot.gear_manipulator)
        self.is_finished = False

    def initialize(self):
        print('depositgear')
        self.robot.gear_manipulator.open_cup()
        self.is_finished = True

    def isFinished(self):
        return self.is_finished

    def end(self):
        pass

    def interrupted(self):
        self.end()
