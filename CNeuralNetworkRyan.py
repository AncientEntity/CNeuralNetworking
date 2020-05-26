import random
import copy
import math

def sigmoid(x):
    #print(x)
    return 1 / (1 + math.exp(-x))

def ReLU(x):
    if(x < 0):
        return 0
    else:
        return x

class BrainFormat:
    def __init__(self,inLayer,hidden, output):
        self.inputLayer = inLayer #Neuron count in input layer
        self.hiddenLayers = hidden  #Neuron count in each hidden layer
        self.outputLayer = output #Neuron count in each output layer

class Neuron:
    def __init__(self,layer=-1):
        self.value = 0
        self.connectionWeights = []
        self.layer = layer
        self.bias = random.uniform(-5,5)

class NeatBrain:
    def __init__(self,format=None):
        self.inputs = []#[Neuron(-1),Neuron(-1),Neuron(-1),Neuron(-1),Neuron(-1)] 
        self.layers = []#[[Neuron(0)]]
        self.out = []#[Neuron(-2)]
        self.active = True
        self.fitness = 0
        self.autoAddFitness = True
        self.baseFormat = format
        if(format != None):
            for i in range(format.inputLayer):
                self.inputs.append(Neuron(-1))
            index = 0
            for layer in format.hiddenLayers:
                self.layers.append([])
                for neuron in range(layer):
                    self.layers[len(self.layers)-1].append(Neuron(index))
                index += 1
            for i in range(format.outputLayer):
                self.out.append(Neuron(-2))
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
        value -= neuron.bias
        neuron.value = ReLU(value)
        return value
    def IterateBrain(self,inputValues=None):

        #Set input neuron's values
        if(inputValues != None):
            index = 0
            for neuron in self.inputs:
                neuron.value = ReLU(inputValues[index])
                index += 1
        
        for layer in self.layers:
            for neuron in layer:
                v = self.SimulateNeuron(neuron)
        outData = []
        for neuron in self.out:
            val = self.SimulateNeuron(neuron)
            outData.append(val)
        if(self.autoAddFitness):
            self.IncreaseFitness()
        return outData
    def MutateBrain(self):
        for neuron in self.inputs:
            for i in range(len(neuron.connectionWeights)):
                neuron.connectionWeights[i] += random.uniform(-1,1)
        for neuron in self.out:
            for i in range(len(neuron.connectionWeights)):
                neuron.connectionWeights[i] += random.uniform(-1,1)
                neuron.bias += random.uniform(-1,1)
        for layer in self.layers:
            for neuron in layer:
                for i in range(len(neuron.connectionWeights)):
                    neuron.connectionWeights[i] += random.uniform(-1,1)
                    neuron.bias += random.uniform(-1,1)
    def IncreaseFitness(self):
        self.fitness += 1
    #def RenderBrain(self,x,y):
    #    inputNames = ["Altitude","Bottom Altitude","Top Altitude","Distance","Velocity"]
    #    index = 0
    #    for neuron in self.inputs:
    #        pygame.draw.circle(screen,[int(sigmoid(neuron.value) * 100),100,100],[x,y  + 15*index],8)
    #        screen.blit(smallFont.render(inputNames[index],True, [0,0,0]),[x-100,y + 15*index])
    #        index += 1
    #    index = 0
    #    for layer in self.layers:
    #        for neuron in layer:
    #            pygame.draw.circle(screen,[int(sigmoid(neuron.value) * 100),100,100],[x+40,y + 15*index],8)
    #            secondaryIndex = 0
    #            for previousLayer in self.GetSpecificLayer(neuron.layer-1):
    #                #color = [255,0,0]
    #                color = [int(sigmoid(previousLayer.value) * 255), 0, 0]
    #                pygame.draw.line(screen,color,[x,y  + 15*secondaryIndex],[x+40,y + 15*index])
    #                secondaryIndex += 1
    #            index += 1
    #    index = 0
    #    for neuron in self.out:
    #        pygame.draw.circle(screen,[int(sigmoid(neuron.value) * 100),100,100],[x+80,y + 15*index],8)
    #        secondaryIndex = 0
    #        for previousLayer in self.GetSpecificLayer(neuron.layer - 1):
    #            #color = [255, 0, 0]
    #            color = [int(sigmoid(previousLayer.value) * 255), 0, 0]
    #            pygame.draw.line(screen, color, [x+40, y + 15 * secondaryIndex], [x + 80, y + 15 * index])
    #            secondaryIndex += 1
    #        index += 1

def EvolveBrains(brains, makeActive=True, brainFormat=None):
    global lastBrains
    brains = sorted(brains,key=lambda x: x.fitness, reverse=True)
    selectedBrains = brains[0:10]

    for i in range(10):
        rando = random.randint(0,9)
        brainomanic = copy.deepcopy(selectedBrains[rando])
        brainomanic.MutateBrain()
        brainomanic.active = True
        brainomanic.fitness = 0
        selectedBrains.append(brainomanic)
    #if(brainFormat != None):
    #    for i in range(5):
    #        selectedBrains.append(NeatBrain(brainFormat))
    return selectedBrains



