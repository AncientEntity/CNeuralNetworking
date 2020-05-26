import random
import copy

class Neuron:
    def __init__(self,layer=-1):
        self.value = 0
        self.connectionWeights = []
        self.layer = layer

class NeatBrain:
    def __init__(self):
        self.inputs = [Neuron(-1),Neuron(-1),Neuron(-1)]
        self.layers = [[Neuron(0)]]
        self.out = [Neuron(-2)]
    def GetSpecificLayer(self,index):
        if(index == -1):
            return self.inputs
        elif(index == -2):
            return self.out
        elif(index == -3):
            return self.layers[len(self.layers)-1]
        else:
            return self.layers[index]
    def SimulateNeuron(self,neuron):
        if(neuron.layer == -1):
            return -1
        value = 0.0
        previousLayer = self.GetSpecificLayer(neuron.layer-1)
        #print(previousLayer)
        while len(neuron.connectionWeights) < len(previousLayer):
            neuron.connectionWeights.append(random.uniform(-1,1))
        #print(neuron.connectionWeights)
        index = 0
        for weight in neuron.connectionWeights:
            value += weight * previousLayer[index].value
            index+=1
        neuron.value = value
        return value
    def IterateBrain(self):
        for layer in self.layers:
            for neuron in layer:
                v = self.SimulateNeuron(neuron)
        outData = []
        for neuron in self.out:
            val = self.SimulateNeuron(neuron)
            outData.append(val)
        return outData
    def MutateBrain(self):
        for neuron in self.inputs:
            for i in range(len(neuron.connectionWeights)):
                neuron.connectionWeights[i] += random.uniform(-0.1,0.1)
        for neuron in self.out:
            for i in range(len(neuron.connectionWeights)):
                neuron.connectionWeights[i] += random.uniform(-0.1,0.1)
        for layer in self.layers:
            for neuron in layer:
                for i in range(len(neuron.connectionWeights)):
                    neuron.connectionWeights[i] += random.uniform(-0.1,0.1)

brains = []

for i in range(100):
    brains.append([NeatBrain(),0])

def DisplayInfo(brains,expected):
    average = 0
    index = 0
    for brain in brains:
        #print("Brain: "+str(index)+ ", OUT: "+str(brain[1]))
        average += brain[1][0]
        index += 1
    average = average / len(brains)
    print("MEAN: "+str(average) + ", EXPECTED: "+str(expected))


def EvolveBrains(brains, testData):
    brains = sorted(brains,key=lambda x: x[1], reverse=True)
    best = []
    for i in range(10):
        index = brains.index(min(brains, key=lambda x: abs(x[1][0]-testData[3])))
        best.append(brains[index])
        brains.pop(index)

    for i in range(90):
        c = copy.deepcopy(best[random.randint(0,9)])
        c[0].MutateBrain()
        #print(c)
        best.append(c)

    return best

testData = []
testData.append([0,1,1,0])
testData.append([0,1,0,0])
testData.append([1,1,1,1])
testData.append([1,0,0,1])
testData.append([0,0,1,0])



while True:
    for iteration in range(len(testData)):
        print("Iteration "+str(iteration)+" Start")
        index = 0
        for brain in brains:
            neuronIndex = 0
            #print(brain)
            for neuron in brain[0].inputs:
                neuron.value = testData[iteration][neuronIndex]
                neuronIndex += 1
            out = brain[0].IterateBrain()
            brains[index][1] = out
            index += 1
        DisplayInfo(brains, testData[iteration][3])
        brains = EvolveBrains(brains,testData[iteration])
