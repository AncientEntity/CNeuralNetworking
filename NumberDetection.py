import random
import copy
import pygame
import datasets.mnistload
import CNeuralNetworkRyan as cnn
import pickle

pygame.init()

screen = pygame.display.set_mode((28*10,28*10))

brainFormat = cnn.BrainFormat(784,[16,16],10)


brains = []

print("(D)raw or (T)rain?")
mode = input()[0].lower()
if(mode == "d"):
    mode = "DRAW"
else:
    mode = "TRAIN"


print("(L)oad brains, (N)ew brains")
option = input()[0].lower()

if(option == "n"):
    for i in range(25):
        brains.append([cnn.NeatBrain(brainFormat),0])
elif(option == "l"):
    loadFile = open('numberdetectionbrainssaved.pickle','rb')
    brains = pickle.load(loadFile)
    loadFile.close()
    for brain in brains:
        brain[0].fitness = 0
    #if(mode == "DRAW"):
    #    brains = [brains[0]]



def DoEvolving(brains, brainFormat):
    brains = sorted(brains, key=lambda x: x[1], reverse=True)
    justBrains = []
    for brain in brains:
        b = brain[0]
        b.fitness = brain[1]
        justBrains.append(b)
    nextGen = cnn.EvolveBrains(justBrains,brainFormat=brainFormat)
    final = []
    for next in nextGen:
        final.append([next,0])
    return final

def DisplayInfo(brains,expected):
    average = 0
    index = 0
    percentCorrect = 0
    for brain in brains:
        #print("Brain: "+str(index)+ ", OUT: "+str(brain[1]))
        average += brain[1]
        index += 1
    average = average / len(brains)
    print("MEAN: "+str(average) + ", EXPECTED: "+str(expected))
    #print("EXPECTED: "+str(expected))


gen = 0
while True:
    print("Iteration "+str(gen)+" Start")

    for trial in range(100):
        testData = []
        expected = ""
        if(mode == "TRAIN"):
            chosenData = datasets.mnistload.GiveRandom()

            for char in chosenData[0]:
                if (char == "\n"):
                    continue
                else:
                    if (char == "."):
                        testData.append(0)
                    else:
                        testData.append(1)
            expected = chosenData[1]
            screen.fill((255, 255, 255))
            pygame.display.update()
            for pixel in range(28 * 28):
                if (testData[pixel] == 1):
                    pygame.draw.rect(screen, (0, 0, 0), (pixel % 28 * 10, pixel // 28 * 10, 10, 10))
                    # screen.set_at((pixel // 28, pixel % 28),(0,0,0))
            pygame.display.update()
            events = pygame.event.get()

            for event in events:
                if (event.type == pygame.KEYDOWN):
                    if (event.key == pygame.K_SPACE):
                        print("SAVING")
                        saveFile = open('numberdetectionbrainssaved.pickle', 'wb')
                        pickle.dump(brains, saveFile)
                        saveFile.close()

        elif(mode == "DRAW"):
            isDrawing = True
            screen.fill([255,255,255])
            while isDrawing:
                events = pygame.event.get()
                pos = pygame.mouse.get_pos()
                if(pygame.mouse.get_pressed()[0] == True):
                    pygame.draw.rect(screen,[0,0,0],[pos[0]-14,pos[1]-14,14,14])
                pygame.display.update()
                for event in events:
                    if(event.type == pygame.KEYDOWN):
                        if(event.key == pygame.K_SPACE):
                            isDrawing = False
                            img = screen.subsurface(0,0,28*10,28*10)
                            img = pygame.transform.scale(img,(28,28))
                            for x in range(28):
                                for y in range(28):
                                    #print(img.get_at((x,y)))
                                    if(img.get_at((x,y))[0] == 255):
                                        testData.append(1)
                                    else:
                                        testData.append(0)
                            #expected = int(input("Suppose to be: ")[0])

        brainCount = 0
        modeAnswer = []
        for i in range(10):
            modeAnswer.append(0)

        #print(len(testData))
        index = 0
        for brain in brains:
            brainCount += 1
            #neuronIndex = 0
            #for neuron in brain[0].inputs:
            #    #print(neuronIndex)
            #    neuron.value = testData[neuronIndex]
            #    neuronIndex += 1
            out = brain[0].IterateBrain(testData)
            if(out.index(max(out)) == expected):
                brain[1] += 1000
            modeAnswer[out.index(max(out))] += 1
            #for i in range(10):
            #    modeAnswer[i] += out[i]
            #print(brains[index][1])
            index += 1
        if(mode == "TRAIN"):
            #print("Trial: " + str(trial) + " Hivemind Believes: " + str(modeAnswer), end=" ")  # + " All: "+str(allRight),end=" ")
            print("Trial: " + str(trial) + " Hivemind Believes: " + str(modeAnswer.index(max(modeAnswer))), end=" ")  # + " All: "+str(allRight),end=" ")
            #print("Trial: "+str(trial) + " Hivemind Believes: "+str(modeAnswer.index(max(modeAnswer))) + " %: "+str(modeAnswer[expected]/brainCount*100) ,end=" ") #+ " All: "+str(allRight),end=" ")
            DisplayInfo(brains, expected)
            #print(modeAnswer)
        elif(mode == "DRAW"):
            print("Is It: "+ " Hivemind Believes: " + str(modeAnswer))
    if(mode == "TRAIN"):
        brains = DoEvolving(brains,brainFormat)
    gen += 1