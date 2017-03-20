from wpilib.command import CommandGroup, WaitCommand


class RunCommandAfterTime(CommandGroup):
    def __init__(self, command, time=0):
        super().__init__()
        self.addSequential(WaitCommand(time))
        self.addSequential(command)
