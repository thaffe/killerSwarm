class EpuckController():
    sensor_threshold = 250

    #commands
    forward = 1
    backward = 2
    left = 3
    right = 4
    stop = 5


    def __init__(self):
        self.command = self.stop
        self.lastCommand = self.stop
        self.l_speed = 1000
        self.r_speed = 1000

    def update(self,sensorValues, image):
        self.lastCommand = self.command
        self.updateAvoid(sensorValues)
        self.updateMap(sensorValues, image)

    def updateAvoid(self, sv):
        left = sv[6] + sv[7]
        right = sv[1] + sv[0]
        if left > self.sensor_threshold or right > self.sensor_threshold:
            if left > right and not self.isLastCmd(self.left):
                self.setCommand(self.right)
            elif not self.isLastCmd(self.right):
                self.setCommand(self.left)
        else:
            self.setCommand(self.forward)

    def updateMap(self, sv, image):
        return "hei"

    def setCommand(self, command):
        self.command = command
        if command == self.forward:
            self.setSpeed(1, 1)
        elif command == self.backward:
            self.setSpeed(-1, -1)
        elif command == self.right:
            self.setSpeed(1, -1)
        elif command == self.left:
            self.setSpeed(-1, 1)
        elif command == self.stop:
            self.setSpeed(0, 0)

    def setSpeed(self, left, right):
        self.l_speed = left
        self.r_speed = right

    def isLastCmd(self, command):
        return command == self.lastCommand



