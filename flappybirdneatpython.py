import pygame
import time
import os
import random
import copy
import math

pygame.init()
screen = pygame.display.set_mode((288*2,512))

images = []
images.append(pygame.image.load("imgs//bg.png"))
images.append(pygame.image.load("imgs//base.png"))
images.append(pygame.image.load("imgs//pipe.png"))
images.append(pygame.image.load("imgs//bird1.png"))


defaultFont = pygame.font.Font('freesansbold.ttf',25)
smallFont = pygame.font.Font('freesansbold.ttf',12)

birds = []
pipes = []
topPipes = []
bottomPipes = []
pipeTimer = 0 #in frames
gen = 0
timeScale = 5
score = 0

def sigmoid(x):
    #print(x)
    return 1 / (1 + math.exp(-x))

def ReLU(x):
    if(x < 0):
        return 0
    else:
        return x

class Neuron:
    def __init__(self,layer=-1):
        self.value = 0
        self.connectionWeights = []
        self.layer = layer
        self.bias = random.uniform(-5,5)

class NeatBrain:
    def __init__(self):
        self.inputs = [Neuron(-1),Neuron(-1),Neuron(-1),Neuron(-1),Neuron(-1)] #Height over ground, Height relative to bottom pipe's top, Height relative to top pipe's top, distance to next pipe, current velocity y
        self.layers = [[Neuron(0)]]
        self.out = [Neuron(-2)]
        self.active = True
        self.fitness = 0
        for i in range(random.randint(0,10)):
            self.layers[0].append(Neuron(0))
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
            neuron.connectionWeights.append(random.uniform(-10,10))
        #print(neuron.connectionWeights)
        index = 0
        for weight in neuron.connectionWeights:
            value += weight * previousLayer[index].value
            index+=1
        value -= neuron.bias
        neuron.value = ReLU(value)
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
                neuron.connectionWeights[i] += random.uniform(-10,10)
        for neuron in self.out:
            for i in range(len(neuron.connectionWeights)):
                neuron.connectionWeights[i] += random.uniform(-10,10)
                neuron.bias += random.uniform(-10,10)
        for layer in self.layers:
            for neuron in layer:
                for i in range(len(neuron.connectionWeights)):
                    neuron.connectionWeights[i] += random.uniform(-10,10)
                    neuron.bias += random.uniform(-10,10)
    def IncreaseFitness(self):
        self.fitness += 1
    def RenderBrain(self,x,y):
        inputNames = ["Altitude","Bottom Altitude","Top Altitude","Distance","Velocity"]
        index = 0
        for neuron in self.inputs:
            pygame.draw.circle(screen,[int(sigmoid(neuron.value) * 100),100,100],[x,y  + 15*index],8)
            screen.blit(smallFont.render(inputNames[index] + ": "+str(neuron.value)[0:5],True, [0,0,0]),[x-150,y + 15*index])
            index += 1
        index = 0
        for layer in self.layers:
            for neuron in layer:
                pygame.draw.circle(screen,[int(sigmoid(neuron.value) * 100),100,100],[x+40,y + 15*index],8)
                secondaryIndex = 0
                for previousLayer in self.GetSpecificLayer(neuron.layer-1):
                    #color = [255,0,0]
                    color = [int(sigmoid(previousLayer.value) * 255), 0, 0]
                    pygame.draw.line(screen,color,[x,y  + 15*secondaryIndex],[x+40,y + 15*index])
                    secondaryIndex += 1
                index += 1
        index = 0
        for neuron in self.out:
            pygame.draw.circle(screen,[int(sigmoid(neuron.value) * 100),100,100],[x+80,y + 15*index],8)
            secondaryIndex = 0
            for previousLayer in self.GetSpecificLayer(neuron.layer - 1):
                #color = [255, 0, 0]
                color = [int(sigmoid(previousLayer.value) * 255), 0, 0]
                pygame.draw.line(screen, color, [x+40, y + 15 * secondaryIndex], [x + 80, y + 15 * index])
                secondaryIndex += 1
            index += 1

def DisplayInfo(birds):
    average = 0
    fitnessScores = []
    index = 0
    for bird in birds:
        #print("Brain: "+str(index)+ ", OUT: "+str(brain[1]))
        average += bird.brain.fitness
        fitnessScores.append(bird.brain.fitness)
        index += 1
    average = average / len(birds)
    return("GEN:  "+str(gen + 1)+" MEAN: "+str(int(average)) + " MIN: "+str(min(fitnessScores)) + " MAX: "+str(max(fitnessScores)))


def EvolveBrains(birds):
    birds = sorted(birds,key=lambda x: x.brain.fitness, reverse=True)
    selectedBrains = []
    best = []

    for i in range(10):
        braino = copy.deepcopy(birds[i].brain)
        braino.fitness = 0
        braino.active = True
        selectedBrains.append(braino)
    for brain in selectedBrains:
        birdoman = Bird(50,200)
        birdoman.brain = copy.deepcopy(brain)
        birdoman.alive = True
        best.append(birdoman)
    for i in range(90):
        rando = random.randint(0,9)
        brainomanic = copy.deepcopy(selectedBrains[rando])
        brainomanic.MutateBrain()
        new = Bird(50,200)
        new.alive = True
        new.brain = brainomanic
        #if(random.randint(0,100) <= 5):
        #    new.brain = NeatBrain()
        best.append(new)



    return best


class Bird:
    def __init__(self,x,y):
        self.alive = True
        self.brain = None
        self.x = x
        self.y = y
        self.xSpeed = 0
        self.ySpeed = 0
    def Update(self):
        self.x += self.xSpeed * timeScale
        self.y += self.ySpeed * timeScale
        self.ySpeed += 0.01 * timeScale
        self.brain.inputs[4].value = ReLU(-self.ySpeed)
        self.brain.inputs[0].value = ReLU(600 - self.y)
        if(len(pipes) != 0):
            try:
                self.brain.inputs[1].value = ReLU(self.y - self.ClosestPipe().y)
            except:
                self.brain.inputs[1].value = 0
        else:
            self.brain.inputs[1].value = 0
        self.brain.inputs[0].value = ReLU(self.y)
        if(len(pipes) != 0):
            try:
                self.brain.inputs[2].value = ReLU(self.ClosestPipe(False).y - self.y)
            except:
                self.brain.inputs[2].value = 0
        else:
            self.brain.inputs[2].value = 0
        if(len(pipes) != 0):
            try:
                self.brain.inputs[3].value = ReLU(self.ClosestPipe(False,offset=75).x - self.x)
            except:
                self.brain.inputs[3].value = 0
        else:
            self.brain.inputs[3].value = 0
        actions = self.brain.IterateBrain()
        self.brain.IncreaseFitness()
        if(actions[0] >= 1):
            self.Jump()
        #for event in pygame.event.get():
        #    if(event.type == pygame.KEYDOWN):
        #        if(event.key == pygame.K_w):
        #            self.Jump()
        if(self.y <= 0 or self.y >= 600):
            self.DoDie()
    def Draw(self):
        screen.blit(images[3],[self.x,self.y])
        #self.brain.RenderBrain(400, 350)
    def Jump(self):
        self.ySpeed = -1.0
    def ClosestPipe(self, top=True,offset=75):
        minSoFar = 999999
        closest = None
        pipesToSearch = []
        if(top):
            pipesToSearch = topPipes
        else:
            pipesToSearch = bottomPipes
        for pipe in pipesToSearch:
            if(self.x <= pipe.x+offset):
                #means it hasnt passed yet
                if(pipe.x - self.x <= minSoFar):
                    closest = pipe
                    minSoFar = pipe.x-self.x
            #print(minSoFar)
        return closest
    def DoDie(self):
        self.alive = False
        self.brain.active = False

class Pipe:
    def __init__(self,x,y):
        self.x = x
        self.y = y
        self.rotation = 0
        self.xSpeed = -0.5
        self.hasGivenScore = False
        self.originalY = y;
    def Update(self):
        self.x += self.xSpeed * timeScale
        self.y = self.originalY + math.cos(self.x/ 100) * 90;

        #Collision
        for bird in birds:
            if((bird.x >= self.x and bird.x <= self.x+52) or (bird.x+53 >= self.x and bird.x+53 <= self.x+52)):
                if((bird.y >= self.y and bird.y <= self.y+320) or (bird.y+38 >= self.y and bird.y+38 <= self.y+320)):
                    bird.DoDie()
                if(self.hasGivenScore == False):
                    global score
                    score+=1
                    self.hasGivenScore = True
        if(self.x < -500):
            try:
                global pipes
                pipes.remove(self)
                bottomPipes.remove(self)
                topPipes.remove(self)
            except:
                pass
    def Draw(self):
        screen.blit(pygame.transform.rotate(images[2],self.rotation),[self.x,self.y])

def Update():
    global pipeTimer, birds, pipes, gen, topPipes, bottomPipes
    #Pipes
    pipeTimer -= 1
    if(pipeTimer <= 0):
        pipeTimer = 125
        offset = random.randint(0,256)
        topPipe = Pipe(650,offset-250)
        topPipe.rotation = 180
        bottomPipe = Pipe(650,offset+250)
        pipes.append(bottomPipe)
        pipes.append(topPipe)
        topPipes.append(topPipe)
        bottomPipes.append(bottomPipe)
    for pipe in pipes:
        pipe.Update()
    anyStillAlive = False
    for bird in birds:
        if(bird.alive == True):
            bird.Update()
            anyStillAlive = True
    if(anyStillAlive == False):
        out = DisplayInfo(birds)
        print("Current Generation: " + str(gen) + " " + out)
        birds = EvolveBrains(birds)
        pipes = []
        topPipes = []
        bottomPipes = []
        gen += 1
        pipeTimer = 0



def Draw():
    #Background
    screen.fill([255,255,255])
    screen.blit(images[0], [0, 0])
    screen.blit(images[0], [288, 0])
    #ground
    screen.blit(images[1], [0, 440])
    screen.blit(images[1], [336, 440])

    #Pipes
    for pipe in pipes:
        pipe.Draw()
    birdsAlive = False
    for bird in birds:
        if(bird.alive == True):
            bird.Draw()
            if(birdsAlive == False):
                bird.brain.RenderBrain(400, 350)
            birdsAlive = True
    text = defaultFont.render(DisplayInfo(birds),True, [0,0,0])
    screen.blit(text,[10,10])

    pygame.display.update()

for i in range(100):
    b = Bird(50,200)
    b.brain = NeatBrain()
    birds.append(b)

drawing = True
while True:
    events = pygame.event.get()
    Update()

    for event in events:
        if(event.type == pygame.KEYDOWN):
            if(event.key == pygame.K_SPACE):
                if(drawing):
                    drawing = False
                else:
                    drawing = True
            if(event.key == pygame.K_g):
                for bird in birds:
                    bird.alive = False
                    bird.brain.active = False

    if(drawing):
        Draw()