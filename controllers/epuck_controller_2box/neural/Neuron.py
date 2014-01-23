import math


class Neuron:
    output = 0

    def __init__(self, name, inputs, pre_update=None, post_update=None, always_uppdate=False, data=None):
        self.name = name
        self.inputs = inputs
        self.pre_update = pre_update
        self.post_update = post_update
        self.always_update = always_uppdate
        self.data = data
        self.memory = 0.5
        self.step_counter = 0
        self.x = 0
        self.output = 0

    def update(self, step_counter):
        if self.pre_update:
            self.pre_update(self)


        self.x *= self.memory
        for key in self.inputs:
            input = self.inputs[key]
            if input.neuron.step_counter != step_counter:
                input.neuron.update(step_counter)
            self.x += input.neuron.output * input.weight

        self.output = 2 / (1 + math.exp(-self.x)) - 1
        self.step_counter = step_counter

        if self.post_update:
            self.post_update(self)
        return self.output


class Input:
    def __init__(self, neuron, weight):
        self.neuron = neuron
        self.weight = weight
        self.activated = True