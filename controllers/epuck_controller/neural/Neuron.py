import math

class Neuron:

    output = 0

    def __init__(self, inputs, min, max):
        self.min = min
        self.max = max
        self.inputs = inputs
        self.x = 0
        self.output = 0

    def update(self):
        for input in self.inputs:
            self.x += input.neuron.output * input.weight

        self.output = 1 / (1 + math.exp(-self.x))
        return self.output