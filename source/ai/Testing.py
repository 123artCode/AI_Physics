import torch
from Init import *

def testing():
    print("Starting testing")

    correct = 0
    total = 0
    with torch.no_grad():
        for data in testloader:
            images, labels = data
            outputs = net(images)
            _, predicted = torch.max(outputs.data, 1)
            total += labels.size(0)
            correct += (predicted == labels).sum().item()
            print(str(correct) + "   of   " + str(total))
    print('Accuracy of the network on the 10000 test images: %d %%' % (100 * correct / total))
    print("Testing done")



def observed_testing():

    correct = 0
    total = 0
    print("Starting observed testing!")
    with torch.no_grad():
        for data in testloader:
            if input("Do observed testing? To stop press N and then enter") == "N":
                print("end")
                exit
            images, labels = data
            outputs = net(images)
            _, predicted = torch.max(outputs.data, 1)
            total += labels.size(0)
            correct += (predicted == labels).sum().item()
            print(predicted)
            imshow(images)
            plt.show()
            print(str(correct) + "   of   " + str(total))
        print('Accuracy of the network on the 10000 test images: %d %%' % (100 * correct / total))
    print("end")


        