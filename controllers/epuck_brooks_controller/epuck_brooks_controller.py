import math
import random
from epuck_basic import EpuckBasic

class cmd():
    forward = 1
    stop = 3
    turn_right = 4
    turn_left = 5
    soft_turn_left = 5
    soft_turn_right = 6
    unknown = 7


class EpuckBrooksController(EpuckBasic):
    dist_threshold = 0.3
    light_threshold = 0.1
    stagnation_threshold = 0.01

    def __init__(self):
        EpuckBasic.__init__(self)
        self.basic_setup() # defined for EpuckBasic
        self.dist_val = []
        self.light_val = []
        self.last_data = None
        self.current_cmd = cmd.stop
        self.suggested_cmd = cmd.stop
        self.counter = 0
        self.stagnation_count = 100 + 200 * random.random()
        self.layers = [self.search, self.retrieval, self.stagnation]
        self.is_retriving = False
        self.lights_order = [4, 5, 6, 7, 0, 1, 2, 3]

    def update_sensors(self):
        self.dist_val = [((0 if math.isnan(x) else x) / 4096) for x in self.get_proximities()]
        self.light_val = [((0 if math.isnan(x) else x) / 4096) for x in self.get_lights()]
        # get lights in the same order as proximity
        self.light_val = [self.light_val[x] for x in self.lights_order]

    def run(self):
        while True:
            self.update_sensors()

            for layer in self.layers:
                self.suggested_cmd = layer()

            self.do_suggested()
            if self.step(self.timestep) == -1: break

    def search(self):
        c = self.get_light_cmd()
        return c if c != cmd.unknown else self.get_dist_cmd()

    def retrieval(self):
        self.is_retriving = False
        for i in range(0, self.num_dist_sensors):
            if self.dist_val[i] > self.dist_threshold and self.light_val[i] > self.light_threshold:
                self.is_retriving = True
                break
        if not self.is_retriving:
            return self.suggested_cmd

        c = self.get_light_cmd()
        return c if c != cmd.unknown else cmd.forward

    def stagnation(self):
        #sjekker om det har skjedd none endringer de siste rundene
        if self.is_retriving and self.is_stagnation():
            self.backward()
            self.turn_left() if random.random() < 0.5 else self.turn_right()
            self.forward(1, 2)
            self.mode = self.search
            return cmd.forward
        else:
            return self.suggested_cmd

    def is_stagnation(self):
        #sjekker om det har skjedd none endringer de siste rundene
        if self.last_data:
            fl = abs(self.dist_val[0] - self.last_data[0])
            fr = abs(self.dist_val[7] - self.last_data[1])

            surrounded = self.get_surroundedness()
            if (fl < self.stagnation_threshold and fr < self.stagnation_threshold and surrounded < 0.15) or surrounded < 0.06:
                self.counter += 1
                if self.counter > self.stagnation_count:
                    self.stagnation_count = 100 + 200 * random.random()
                    self.counter = 0
                    return True
        self.last_data = [self.dist_val[0], self.dist_val[7]]

        return False


    def get_light_cmd(self):
        left = sum(self.light_val[:4])
        right = sum(self.light_val[4:])
        if abs(left - right) > self.light_threshold:
            if left < right:
                return cmd.soft_turn_left
            else:
                return cmd.soft_turn_right

        return cmd.unknown

    def get_dist_cmd(self):
        #Hvis man ikke har registrert nok lys kjores en unngaa vegger ting istede
        left = sum(self.dist_val[6:8])
        right = sum(self.dist_val[0:2])
        if left > self.dist_threshold or right > self.dist_threshold:
            if left > right and not self.is_last_cmd(cmd.turn_left):
                return cmd.turn_right
            elif not self.is_last_cmd(cmd.turn_right):
                return cmd.turn_left
        else:
            return cmd.forward

        return self.current_cmd

    def get_surroundedness(self):
        return sum(self.dist_val[2:6]) / 4

    def do_suggested(self):
        if self.suggested_cmd == self.current_cmd: return
        self.current_cmd = self.suggested_cmd
        c = self.current_cmd

        if c == cmd.forward:
            self.set_wheel_speeds(1, 1)
        elif c == cmd.turn_left:
            self.set_wheel_speeds(-1, 1)
        elif c == cmd.turn_right:
            self.set_wheel_speeds(1, -1)
        elif c == cmd.soft_turn_left:
            self.set_wheel_speeds(0.2, 1)
        elif c == cmd.soft_turn_right:
            self.set_wheel_speeds(1, 0.2)
        else:
            self.set_wheel_speeds(0, 0)

    def is_last_cmd(self, command):
        return command == self.current_cmd


controller = EpuckBrooksController()
controller.run()