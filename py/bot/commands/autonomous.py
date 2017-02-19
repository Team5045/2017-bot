from wpilib.command import CommandGroup, Command


class NoAutonomous(Command):
    nickname = "Do nothing"

    def __init(self, robot):
        super().init()

    def end(self):
        pass

    def interrupted(self):
        pass

    def isFinished(self):
        return True


class Autonomous(CommandGroup):
    def __init__(self, robot):
        super().__init__()
        self.robot = robot


class CrossDefenseAndShootAutonomous(Autonomous):
    nickname = "Xxxx"

    def __init__(self, robot):
        super().__init__(robot)
        self.addSequential()

    def isFinished(self):
        return super().isFinished()


# List of all available autonomous commands provided in file
auto_commands = [NoAutonomous]
