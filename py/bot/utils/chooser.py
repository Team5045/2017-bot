from wpilib import SendableChooser
from wpilib.command import Subsystem


class Chooser(Subsystem):

    def __init__(self, robot):
        super().__init__()
        self.robot = robot
        self.chooser = SendableChooser()

        for i, option in enumerate(self.OPTIONS):
            if i == 0:
                self.chooser.addDefault(option, i)
            else:
                self.chooser.addObject(option, i)

        self.robot.jetson.put_value(self.KEY,
                                    self.chooser, 'data')

    def toggle(self):
        self.robot.jetson.put_value(
            self.KEY + '/selected',
            self.OPTIONS[(self.get_selected_index() + 1) % len(self.OPTIONS)],
            valueType='String')

    def get_selected_index(self):
        return self.chooser.getSelected()

    def get_selected(self):
        return self.OPTIONS[self.chooser.getSelected()]

    def on_choose(self, value):
        pass
