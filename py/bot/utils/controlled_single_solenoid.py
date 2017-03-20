import wpilib


class ControlledSingleSolenoid(object):
    def __init__(self, port):
        self.solenoid = wpilib.Solenoid(port)
        self.state = self.solenoid.get()

    def set(self, state):
        if state != self.state:
            self.state = state
            self.solenoid.set(self.state)

    def get(self):
        return self.state

    def toggle(self):
        self.set(not self.state)

    def deploy(self):
        self.set(True)

    def retract(self):
        self.set(False)
