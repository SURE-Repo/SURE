import torch
import torch.nn as nn

from torchvision import models
from torch.autograd import Variable

    
class Siamese(nn.Module):
    def __init__(self):
        super(Siamese, self).__init__()
        self.vgg16 = models.vgg16()
        self.vgg16.classifier = nn.Sequential()


        self.fully_connect1 = torch.nn.Linear(25088, 512)

        self.relu = torch.nn.ReLU()
        self.fully_connect2 = torch.nn.Linear(512, 1)

    def forward(self, x):
        x1, x2 = x
        #------------------------------------------#

        #------------------------------------------#
        x1 = self.vgg16.features(x1)
        x2 = self.vgg16.features(x2)
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