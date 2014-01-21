import math

class Neuron:

    output = 0

    def __init__(self, inputs, min = -1, max = 1):
        self.min = min
        self.max = max
        self.inputs = inputs
        self.x = 0
        self.output = 0

    def update(self):
        self.x *= 0.5
        for input in self.inputs:
            self.x += input.neuron.output * input.weight

        self.output = 2 / (1 + math.exp(-self.x)) - 1
        return self.output


class Input:

    def __init__(self, neuron, weight):
        self.neuron = neuron
        self.weight = weight