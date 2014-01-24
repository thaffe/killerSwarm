import math
import random

from controller import *
import neural.NeuralNetwork as NN





#sensor names
sensors = ["fmr", "fr", "r", "br", "bl", "l", "fl", "fml"]


class EpuckController(DifferentialWheels):
    dist_threshold = 200
    #robots constants
    num_dist_sensors = 8
    num_light_sensors = 8
    num_leds = 9
    cam_update_rate = 1
    max_speed = 1000

    #Neural nets constants
    avoid_weight = 4
    food_weight = 0.4
    robot_weight = 3
    anti_robot_weight = 3
    robot_found_weight = 1

    wander_time = 150
    wander_frequence = 1.0 / 2000.0
    team_change_frequence = 1.0 / 2500.0
    turn_frequence = 1.0 / 200.0

    def __init__(self):
        DifferentialWheels.__init__(self)

        self.timestep = int(self.getBasicTimeStep())
        self.camera = self.getCamera('camera')
        self.camera.enable(self.cam_update_rate * self.timestep)
        self.leds = [self.getLED("led" + str(x)) for x in range(self.num_leds)]

        self.speed = [0, 0]
        self.wander = 0
        self.turn = 0

        self.neuralNet = NN.NeuralNetwork()

        self.team = random.random() >= 0.5

        for i in range(self.num_dist_sensors):
            sensor = self.getDistanceSensor("ps" + str(i))
            sensor.enable(self.timestep)
            self.neuralNet.append(name="ds-" + sensors[i], post_update=self.dist_pre_update,
                                  data=sensor)

        for i in range(self.num_light_sensors):
            sensor = self.getLightSensor("ls" + str(i))
            sensor.enable(self.timestep)
            self.neuralNet.append(name="ls-" + sensors[i], post_update=self.light_pre_update,
                                  data=sensor)

        for i in range(8):
            self.neuralNet.append(name="c-" + str(i), post_update=self.cam_pre_update, data=i)

        for i in range(8):
            self.neuralNet.append(name="anti_c-" + str(i), post_update=self.cam_anti_pre_update, data=i)

        self.camera_teammates = [x for x in range(8)]
        self.camera_anti_teammates = [x for x in range(8)]
        self.update_cam = self.cam_update_rate

        self.neuralNet.append(name="avoid-r", weights={
            "ds-fl": 2,
            "ds-fml": 2,
            "ds-fmr": -2,
            "ds-fr": -2
        })

        self.neuralNet.append(name="avoid-l", weights={
            "ds-fl": -2,
            "ds-fml": -2,
            "ds-fmr": 2,
            "ds-fr": 2
        })

        self.neuralNet.append(name="food-r", weights={
            "ls-fmr": -1,
            "ls-fr": -1,
            "ls-r": -1,
            "ls-br": -1,
            "ls-bl": 1,
            "ls-l": 1,
            "ls-fl": 1,
            "ls-fml": 1
        })

        self.neuralNet.append(name="food-l", weights={
            "ls-fmr": 1,
            "ls-fr": 1,
            "ls-r": 1,
            "ls-br": 1,
            "ls-bl": -1,
            "ls-l": -1,
            "ls-fl": -1,
            "ls-fml": -1
        })

        self.neuralNet.append(name="robot-l", weights={
            "c-0": 3,
            "c-1": 2,
            "c-2": 2,
            "c-3": -1,
            "c-4": -1,
            "c-5": -2,
            "c-6": -2,
            "c-7": -3,
        })

        self.neuralNet.append(name="robot-r", weights={
            "c-0": -3,
            "c-1": -2,
            "c-2": -2,
            "c-3": -1,
            "c-4": -1,
            "c-5": 2,
            "c-6": 2,
            "c-7": 3,
        })

        self.neuralNet.append(name="anti_robot-l", weights={
            "anti_c-0": -3,
            "anti_c-1": -2,
            "anti_c-2": -2,
            "anti_c-3": -1,
            "anti_c-4": -1,
            "anti_c-5": 2,
            "anti_c-6": 2,
            "anti_c-7": 3,
        })

        self.neuralNet.append(name="anti_robot-r", weights={
            "anti_c-0": 3,
            "anti_c-1": 2,
            "anti_c-2": 2,
            "anti_c-3": -1,
            "anti_c-4": -1,
            "anti_c-5": -2,
            "anti_c-6": -2,
            "anti_c-7": -3,
        })

        self.neuralNet.append(name="robot-found", pre_update=self.robot_found_preupdate, weights={
            "c-0": 0,
            "c-1": self.robot_found_weight,
            "c-2": self.robot_found_weight,
            "c-3": self.robot_found_weight,
            "c-4": self.robot_found_weight,
            "c-5": self.robot_found_weight,
            "c-6": self.robot_found_weight,
            "c-7": 0
        })

        self.neuralNet.append(name="surrounded", weights={
            "ds-fmr": 0,
            "ds-fr": 0,
            "ds-r": 4,
            "ds-br": 2,
            "ds-bl": 2,
            "ds-l": 4,
            "ds-fl": 0,
            "ds-fml": 0
        })

        self.neuralNet.append(name="left", pre_update=self.wheel_pre_update, weights={
            "avoid-l": self.avoid_weight,
            "food-l": self.food_weight,
            "robot-l": self.robot_weight,
            "anti_robot-l": self.anti_robot_weight,
            "robot-found": 0,
            "surrounded": 0
        }, post_update=self.wheel_post_update, data=0, always_update=True)

        self.neuralNet.append(name="right", pre_update=self.wheel_pre_update, weights={
            "avoid-r": self.avoid_weight,
            "food-r": self.food_weight,
            "robot-r": self.robot_weight,
            "anti_robot-r": self.anti_robot_weight,
            "robot-found": 0,
            "surrounded": 0
        }, post_update=self.wheel_post_update, data=1, always_update=True)

    def dist_pre_update(self, neuron):
        x = neuron.data.getValue()
        neuron.output = 0 if math.isnan(x) or x < self.dist_threshold else x / 4096

    def light_pre_update(self, neuron):
        x = neuron.data.getValue()
        neuron.output = 0 if math.isnan(x) else x / 4200

    def cam_pre_update(self, neuron):
        #update camera_teammates array
        if self.update_cam >= self.cam_update_rate:
            self.update_cam = 0
            self.camera_teammates = self.get_camera_teammates()
            self.camera_anti_teammates = self.get_cameara_anti_team()

        neuron.output = self.camera_teammates[neuron.data]

    def cam_anti_pre_update(self, neuron):
        neuron.output = self.camera_anti_teammates[neuron.data]

    def wheel_pre_update(self, neuron):
        #if left wheel
        #else right wheel
        if self.wander <= 0:
            found = neuron.inputs["robot-found"].neuron.output
            avoid = max(0, self.avoid_weight - 3 * self.avoid_weight * found**2)
            robot = max(0, self.robot_weight - self.robot_weight * found**2)
            food = self.food_weight + 8 * found**2

            if self.getName() == "e-puck1":
                print("found",found,"avoid",avoid,"robot",robot,"food",food)

            if neuron.data == 0:
                neuron.inputs["avoid-l"].weight = avoid
                neuron.inputs["robot-l"].weight = robot
                neuron.inputs["food-l"].weight = food
            else:
                neuron.inputs["avoid-r"].weight = avoid
                neuron.inputs["robot-r"].weight = robot
                neuron.inputs["food-r"].weight = food

    def wheel_post_update(self, neuron):
        self.speed[neuron.data] = neuron.output

    def robot_found_preupdate(self, neuron):
        neuron.memory = min(0.98, max(0, neuron.output) ** 2.0)
        return

    def run(self):
        step_counter = 0
        self.set_green_leds(1) if self.team else self.set_red_leds(1)
        while True:
            # self.update_sensors()
            self.update_cam += 1
            step_counter += 1
            surrounded = self.neuralNet.neurons["surrounded"].output
            found = self.neuralNet.neurons["robot-found"].output
            if surrounded < 0.6 and random.random() < self.team_change_frequence:
                self.team = not self.team
                self.set_red_leds(0 if self.team else 1)
                self.set_green_leds(1 if self.team else 0)

            if not self.turn and self.wander <= 0:
                self.check_stagnation()
            else:
                self.wander -= 1

            self.neuralNet.update(step_counter)
            #and self.neuralNet.neurons["robot-l"].output < 0.01 and self.neuralNet.neurons["robot-r"].output < 0.01
            if found < 0.01 and random.random() < self.turn_frequence:
                if self.getName() == "e-puck1":
                    print "turning!!!!!!!!!!!!!!!"
                self.turn = 75
                right = self.speed[0] > self.speed[1]
                self.setSpeed(
                    500 if right else -500,
                    -500 if right else 500
                )
            elif found > 0 or self.turn == 0:
                self.turn = 0
                self.setSpeed(
                    self.max_speed * max(-1, min(1 - 2 * self.speed[0], 1)),
                    self.max_speed * max(-1, min(1 - 2 * self.speed[1], 1))
                )
            else:
                self.turn -= 1

            if self.step(self.timestep) == -1: break

    def check_stagnation(self):
        surrounded = self.neuralNet.neurons["surrounded"].output

        if random.random() < self.wander_frequence * (1 - surrounded) and surrounded < 0.9:
            print ("Wandering of", self.getName())
            self.neuralNet.set_weight("left", "avoid-l", self.avoid_weight)
            self.neuralNet.set_weight("right", "avoid-r", self.avoid_weight)

            self.neuralNet.set_weight("left", "food-l", 0.2)
            self.neuralNet.set_weight("right", "food-r", 0.2)

            self.neuralNet.set_weight("left", "robot-l", 0)
            self.neuralNet.set_weight("right", "robot-r", 0)

            self.wander = 100 + 60 * random.random()

    def get_camera_teammates(self):
        return self.get_camera_index(1 if self.team else 0)

    def get_cameara_anti_team(self):
        return self.get_camera_index(0 if self.team else 1)

    def get_camera_index(self, color_index):
        img = self.camera.getImageArray();
        camera_teammates = [0 for i in range(self.camera.getWidth() / 2)]

        for x in range(0, self.camera.getWidth(), 2):
            col = x / 2
            for y in range(0, self.camera.getHeight()):
                camera_teammates[col] += math.floor(
                    img[x][y][color_index] / max(1, (img[x][y][1 - color_index] + img[x][y][2]))) / (
                                             255 * 6) + math.floor(
                    img[x + 1][y][color_index] / max(1, (img[x + 1][y][1 - color_index] + img[x + 1][y][2]))) / (
                                             255 * 6)
            if not self.team:
                camera_teammates[col] *= 4

        return camera_teammates

    def set_green_leds(self, value):
        self.leds[8].set(value)

    def set_red_leds(self, value):
        for i in range(0, 7):
            self.leds[i].set(value)


controller = EpuckController()
controller.run()