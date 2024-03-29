from wpilib import SendableChooser
from wpilib.command import Subsystem

from bot import config
from bot.commands import autonomous


class AutoModeChooser(Subsystem):

    def __init__(self, robot):
        super().__init__()
        self.robot = robot
        self.chooser = SendableChooser()

        for i, Command in enumerate(autonomous.auto_commands):
            if i == 0:
                self.chooser.addDefault(Command.nickname, Command(self.robot))
            else:
                self.chooser.addObject(Command.nickname, Command(self.robot))

        self.robot.jetson.put_value(config.MISC_AUTO_COMMAND_DASHBOARD_KEY,
                                    self.chooser, 'data')

    def get_selected(self):
        selected = self.chooser.getSelected()
        print(selected.__class__.nickname)
        return selected
