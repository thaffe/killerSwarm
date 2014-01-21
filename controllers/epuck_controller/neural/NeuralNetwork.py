import Neuron

class NeuralNetwork:

    def __init__(self, weights = 0, min = -1, max = 1):
        self.inputCount = len(weights[0])
        self.outputCount = len(weights)
        self.inputs = [Neuron.Neuron([]) for i in range(self.inputCount)]
        self.outputs = []
        for i in range(self.outputCount):
            inputs = []
            for j in range(self.inputCount):
                inputs.append(Neuron.Input(self.inputs[j], weights[i][j]))

            self.outputs.append(Neuron.Neuron(inputs))

    def update(self, inputs):
        for i in range(len(inputs)):
            self.inputs[i].output = inputs[i]

        result = []

        for output in self.outputs:
            result.append(output.update())

        return result
