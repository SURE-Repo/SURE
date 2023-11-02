import torch
import torch.nn as nn

from torchvision import models
from torch.autograd import Variable

    
class Siamese(nn.Module):
    def __init__(self):
        super(Siamese, self).__init__()
        self.resnet18 = models.resnet18()
        self.resnet18.fc = nn.Sequential()

        self.fully_connect1 = torch.nn.Linear(512, 512)

        self.relu = torch.nn.ReLU()
        self.fully_connect2 = torch.nn.Linear(512, 1)

    def forward(self, x):
        x1, x2 = x
        #------------------------------------------#

        #------------------------------------------#
        x1 = self.resnet18(x1)
        x2 = self.resnet18(x2)
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