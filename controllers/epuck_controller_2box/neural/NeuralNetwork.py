from Neuron import *


class NeuralNetwork:
    def __init__(self):
        self.neurons = {}

    def append(self, name, weights=[], pre_update=None, post_update=None, always_update=False, data=None):
        inputs = {}
        for key in weights:
            inputs[key] = Input(self.neurons[key], weights[key])
        # inputs = [ Input(self.neurons[key], weights[key]) for key in weights ]
        self.neurons[name] = Neuron(name, inputs, pre_update, post_update, always_update, data)

    def update(self, step_conuter):
        for neuron in self.neurons:
            n = self.neurons[neuron]
            if n.step_counter != step_conuter and n.always_update:
                n.update(step_conuter)