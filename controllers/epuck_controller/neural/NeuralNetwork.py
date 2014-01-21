import Neuron


class NeuralNetwork:

    def __init__(self):
        self.neurons = {}

    def append(self, name, weights=[], pre_update=None, post_update=None, always_update=False):
        inputs = []
        for weight in weights:
            inputs.append(Neuron.Input(self.neurons[weight.neuron_id], weight.value))

        self.neurons[name] = Neuron.Neuron(inputs, pre_update, post_update, always_update)

    def update(self, timestep):
        for neuron in self.neurons:
            if neuron.timestep != timestep and neuron.always_update:
                neuron.update(timestep)