import math


class Neuron:
    output = 0

    def __init__(self, name, inputs, pre_update=None, post_update=None):
        self.name = name
        self.inputs = inputs
        self.pre_update = pre_update
        self.post_update = post_update

        self.x = 0
        self.output = 0

    def update(self, timestep):
        if self.pre_update:
            self.pre_update(self)

        self.x *= 0.5
        for input in self.inputs:
            if input.neuron.timestep != timestep:
                input.neuron.update(timestep)
            self.x += input.neuron.output * input.weight

        self.output = 2 / (1 + math.exp(-self.x)) - 1
        self.timestep = timestep

        if self.post_update:
            self.post_update(self)
        return self.output


class Input:
    def __init__(self, neuron, weight):
        self.neuron = neuron
        self.weight = weight
        self.activated = True