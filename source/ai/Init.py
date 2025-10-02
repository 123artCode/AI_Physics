import Model as M
import torch
import torch.nn as nn
import torch.optim as optim
import matplotlib.pyplot as plt
import torchvision
import torchvision.transforms as transforms
import numpy as np
import json


print("Init starting")



# transform = transforms.Compose(
#     [transforms.ToTensor(),
#     transforms.Normalize((0.5, 0.5, 0.5), (0.5, 0.5, 0.5))])

# trainset = torchvision.datasets.CIFAR10(root='./data', train=True, download=True, transform=transform)
# testset = torchvision.datasets.CIFAR10(root='./data', train=False, download=True, transform=transform)


# classes = ('plane', 'car', 'bird', 'cat',
#     'deer', 'dog', 'frog', 'horse', 'ship', 'truck')


# def imshow(img):
#     img = img / 2 + 0.5
#     npimg = img.numpy()
#     plt.imshow(np.transpose(npimg, (1, 2, 0)))









def best_accuracy():
    with open('best_accuracy.json', 'r') as f:
        return float(json.load(f))

def update_best_accuracy(accuracy, net):
    with open('best_accuracy.json', "w", encoding="utf-8") as f:
        json.dump(str(accuracy), f, ensure_ascii=False, indent=4)

    torch.save(net.state_dict(), "model")


print("Init finished!")
