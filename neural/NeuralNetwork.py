import Neuron

class NeuralNetwork:

    def __init__(self, inputCount, invisibleLayers = 0, outputCount = 1, weights = 0, min = -1, max = 1):
        self.inputs = Neuron[inputCount]
        self.invisibleLayers = invisibleLayers

        #if invisibleLayers:
            #TODO: implement

        self.outputs = Neuron[outputCount]
        for i in range(outputCount):
            self.outputs[i] = Neuron(self.inputs, min, max)


    def update(self, inputs):
        result = []

        #if self.invisibleLayers:
            #TODO: implement

        for output in self.outputs:
            result.append(output.update())

        return result
