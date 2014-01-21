import math
import random
import neural.NeuralNetwork as NN
from epuck_basic import EpuckBasic

sensors = ["fmr", "fr", "r", "br", "bl", "l", "fl", "fml"]


class EpuckController(EpuckBasic):
    dist_threshold = 200
    light_threshold = 0.1
    stagnation_threshold = 0.001

    avoid_weight = 4
    food_weight = 0.5
    robot_weight = 3
    robot_found_weight = 1

    wander_time = 150
    wander_frequence = 1.0/2000.0

    def __init__(self):
        EpuckBasic.__init__(self)
        self.basic_setup() # defined for EpuckBasic

        self.counter = 0
        self.neuralNet = NN.NeuralNetwork()

        for i in range(self.num_dist_sensors):
            self.neuralNet.append(name="ds-" + sensors[i], post_update=self.dist_pre_update, data=self.dist_sensors[i])

        for i in range(self.num_light_sensors):
            self.neuralNet.append(name="ls-" + sensors[i], post_update=self.light_pre_update,
                                  data=self.light_sensors[i])

        for i in range(8):
            self.neuralNet.append(name="c-" + str(i), post_update=self.cam_pre_update, data=i)

        self.greens = [x for x in range(8)]
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

        self.neuralNet.append(name="robot-found", pre_update=self.robot_found_preupdate, weights={
            "c-0": -self.robot_found_weight,
            "c-1": self.robot_found_weight,
            "c-2": self.robot_found_weight,
            "c-3": self.robot_found_weight,
            "c-4": self.robot_found_weight,
            "c-5": self.robot_found_weight,
            "c-6": self.robot_found_weight,
            "c-7": -self.robot_found_weight,
        })

        self.neuralNet.append(name="left", pre_update=self.wheel_pre_update, weights={
            "avoid-l": self.avoid_weight,
            "food-l": self.food_weight,
            "robot-l": self.robot_weight,
            "robot-found": 0
        }, post_update=self.wheel_post_update, data=0, always_update=True)

        self.neuralNet.append(name="right", pre_update=self.wheel_pre_update, weights={
            "avoid-r": self.avoid_weight,
            "food-r": self.food_weight,
            "robot-r": self.robot_weight,
            "robot-found": 0
        }, post_update=self.wheel_post_update, data=1, always_update=True)
        self.speed = [0, 0]
        self.wander = 0

    def dist_pre_update(self, neuron):
        x = neuron.data.getValue()
        neuron.output = 0 if math.isnan(x) or x < self.dist_threshold else x / 4096

    def light_pre_update(self, neuron):
        x = neuron.data.getValue()
        neuron.output = 0 if math.isnan(x) else x / 4200

    def cam_pre_update(self, neuron):
        #update camera greens array
        if self.update_cam >= self.cam_update_rate:
            self.update_cam = 0
            self.greens = self.get_camera_greens()

        neuron.output = self.greens[neuron.data]

    def wheel_pre_update(self, neuron):
        #if left wheel
        #else right wheel
        if self.wander <= 0:
            if random.random() < self.wander_frequence:
                print ("Wandering of",self.getName())
                avoid = self.avoid_weight
                food = 0
                robot = 0
                self.wander = self.wander_time
            else:
                found = neuron.inputs["robot-found"].neuron.output
                avoid = max(0, self.avoid_weight - 3*self.avoid_weight * found)
                robot = max(0, self.robot_weight - self.robot_weight * found)
                food = self.food_weight + 4*found
                # if self.getName() == "e-puck1":
                #     print("found",found,"avoid",avoid,"robot",robot,"food",food)

            if neuron.data == 0:
                neuron.inputs["avoid-l"].weight = avoid
                neuron.inputs["robot-l"].weight = robot
                neuron.inputs["food-l"].weight = food
            else:
                neuron.inputs["avoid-r"].weight = avoid
                neuron.inputs["robot-r"].weight = robot
                neuron.inputs["food-r"].weight = food
        else:
            self.wander -= 1

    def wheel_post_update(self, neuron):
        self.speed[neuron.data] = neuron.output

    def robot_found_preupdate(self, neuron):
        neuron.memory = min(0.99, max(0,neuron.output)**1.9)
        return

    def run(self):
        self.set_leds(1)
        step_counter = 0
        while True:
            # self.update_sensors()
            self.update_cam += 1
            step_counter += 1

            self.neuralNet.update(step_counter)
            self.set_wheel_speeds(max(-1,min(1 - 2*self.speed[0], 1)), max(-1,min(1 - 2*self.speed[1], 1)))

            if self.step(self.timestep) == -1: break

    def get_camera_greens(self):
        img = self.camera.getImageArray();
        greens = [0 for i in range(self.camera.getWidth() / 2)]
        for x in range(0, self.camera.getWidth(), 2):
            col = x / 2
            for y in range(0, self.camera.getHeight()):
                greens[col] += math.floor(img[x][y][1] / max(1, (img[x][y][0] + img[x][y][2]))) / (
                    255 * 6) + math.floor(img[x + 1][y][1] / max(1, (img[x + 1][y][0] + img[x + 1][y][2]))) / (255 * 6)

        return greens


controller = EpuckController()
controller.run()