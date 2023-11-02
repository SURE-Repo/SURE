import torch
import torch.nn as nn

from torchvision import models

    
class Siamese(nn.Module):
    def __init__(self):
        super(Siamese, self).__init__()
        self.alexnet = models.alexnet()
        self.alexnet.classifier = nn.Sequential()


        self.fully_connect1 = torch.nn.Linear(9216, 512)

        self.relu = torch.nn.ReLU()
        self.fully_connect2 = torch.nn.Linear(512, 1)

    def forward(self, x):
        x1, x2 = x
        #------------------------------------------#

        #------------------------------------------#
        x1 = self.alexnet.features(x1)
        x2 = self.alexnet.features(x2)
        #-------------------------#

        #-------------------------#     
        x1 = torch.flatten(x1, 1)
        x2 = torch.flatten(x2, 1)
        x = torch.abs(x1 - x2)
        #-------------------------#

        #-------------------------#

        x = self.relu(self.fully_connect1(x))
        x = self.fully_connect2(x)
        return x