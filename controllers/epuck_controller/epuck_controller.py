import math
import random
import sys
import neural.NeuralNetwork as NN
import neural.Neuron
from epuck_basic import EpuckBasic

class cmd():
    #commands
    forward = 1
    stop = 3
    turn_right = 4
    turn_left = 5
    soft_turn_left = 5
    soft_turn_right = 6
    unknown = 7

def cmd_name(c):
    if c == cmd.forward : return "Forward"
    if c == cmd.stop : return "stop"
    if c == cmd.turn_left : return "turn_left"
    if c == cmd.turn_right : return "turn_right"
    if c == cmd.soft_turn_left : return "soft_turn_left"
    if c == cmd.soft_turn_right : return "soft_turn_right"
    if c == cmd.unknown : return "unknown"


class action():
    retrive = 1
    search = 1


class MapObject():
    def __init__(self, color, moveable):
        self.color = color
        self.moveable = moveable


class EpuckController(EpuckBasic):
    dist_threshold = 0.3
    light_threshold = 0.1
    stagnation_threshold = 0.001
    def __init__(self,
                 tempo=1.0,
                 e_thresh=125,
                 nvect=True,
                 cvect=True,
                 svect=True,
                 band='bw',
                 concol=1.0,
                 snapshow=True,
                 ann_cycles=1,
                 agent_cycles=5,
                 act_noise=0.1,
                 tfile="redman4"):
        EpuckBasic.__init__(self)
        self.basic_setup() # defined for EpuckBasic
        self.dist_val = []
        self.light_val = []
        self.last_data = None
        self.current_cmd = cmd.stop
        self.suggested_cmd = cmd.stop
        self.mode = self.search
        self.counter = 0
        self.stagnation_count = 100 + 300 * random.random()
        self.searhNN = NN.NeuralNetwork(8,0,2)

    def update_sensors(self):
        self.dist_val = [((0 if math.isnan(x) else x) / 4096) for x in self.get_proximities()]
        self.light_val = [((0 if math.isnan(x) else x) / 4096) for x in self.get_lights()]
        # fix to get lights in the same order as proximity
        lights_order = [4, 5, 6, 7, 0, 1, 2, 3]
        self.light_val = [self.light_val[x] for x in lights_order]

    def run(self):
        while True:
            self.update_sensors()
            self.check_mode()
            # self.set_leds(1)
            self.suggested_cmd = self.mode()

            self.do_suggested()
            if self.step(self.timestep) == -1: break

    def check_mode(self):
        if self.mode == self.stagnation : return
        self.mode = self.search
        #itererer over distanse og sjekker om man er intil et objekt,
        # sjekker ogsaa om det lyser fra objektet
        for i in range(0,self.num_dist_sensors):
            if self.dist_val[i] > self.dist_threshold and self.light_val[i] > self.light_threshold :
                self.mode = self.retrieval
                break

        #sjekker om det har skjedd none endringer de siste rundene
        if self.last_data and self.mode == self.retrieval:
            fl = self.dist_val[0] - self.last_data[0]
            fr = self.dist_val[7] - self.last_data[1]

            if self.dist_val[2] + self.dist_val[5] < self.dist_threshold :
                self.counter += 1
                if self.counter > self.stagnation_count:
                    print("Staggnation:",self.counter)
                    self.stagnation_count = 100+300*random.random()
                    self.counter = 0
                    self.mode = self.stagnation

        self.last_data = [self.dist_val[0], self.dist_val[7]]

    def search(self):
        self.searhNN.update();
        c = self.get_light_cmd()
        return c if c != cmd.unknown else self.get_dist_cmd()

    def retrieval(self):
        c = self.get_light_cmd()
        return c if c != cmd.unknown else cmd.forward

    def stagnation(self):
        self.backward()
        self.turn_left() if random.random() < 0.5 else self.turn_right()
        self.forward(1,2)
        self.mode = self.search
        return cmd.forward

    def get_light_cmd(self):
        left = sum(self.light_val[:4])
        right = sum(self.light_val[4:])
        diff = left - right
        if abs(diff) > self.light_threshold:
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

    def do_suggested(self):
        if self.suggested_cmd == self.current_cmd : return
        # print ("Performing cmd:", cmd_name(self.suggested_cmd))
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



controller = EpuckController(tempo=1.0, band='gray')
controller.run()