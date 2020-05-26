from mnist import MNIST
import random
import os

dir_path = os.path.dirname(os.path.realpath(__file__))

mndata = MNIST(dir_path)

images, labels = mndata.load_training()


def GiveRandom():
    index = random.randrange(0, len(images))  # choose an index ;-)
    return (mndata.display(images[index]),labels[index])

#print(GiveRandom())

print("MNIST LOADER READY")
