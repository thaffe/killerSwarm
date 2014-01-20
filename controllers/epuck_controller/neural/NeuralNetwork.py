import Neuron


class NeuralNetwork:

    def __init__(self, inputCount, outputCount = 1, weights = 0, min = -1, max = 1):
        self.inputs = [Neuron([]) for i in range(inputCount)]
        self.outputs = []
        for i in range(outputCount):
            inputs = []
            for j in range(inputCount):
                inputs.append(Neuron.Input(self.inputs[j], weights[i][j]))

            self.outputs.append(Neuron(inputs, min, max))

    def update(self, inputs):
        for i in range(len(inputs)):
            self.inputs[i].output = inputs[i]

        result = []

        for output in self.outputs:
            result.append(output.update())

        return result
