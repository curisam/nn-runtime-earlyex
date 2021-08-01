
from numpy.lib.function_base import _calculate_shapes
import torch
from torch.distributions.categorical import Categorical
import torch.nn as nn
import torch.nn.functional as F
from torch.nn.modules.conv import Conv2d
from operator import attrgetter
from torch.autograd import Variable
import sys
from torch.distributions import Categorical

class ExException(Exception):
    def __init__(self, id):
        self.id = id

class Gate(nn.Module):
    def __init__(self, id, exnet):
        super(Gate, self).__init__()
        self.exit = False
        self.exnet = exnet
        self.id = id

    def forward(self, x):
        # prev_2 = self.id -3
        # prev_1 = self.id -2
        # prev_0 = self.id -1
        
        # if self.exnet.eenet and self.id > 0:
        #     m = self.exnet.exactly[self.id-1]
        #     if m.conf > 0.9:
        #         raise ExException(self.id)

        # if self.exnet.consensus and self.id > 2:
        #     acc_2  = self.exnet.exactly[prev_2].acc
        #     acc_1  = self.exnet.exactly[prev_1].acc
        #     acc_0  = self.exnet.exactly[prev_0].acc
            
        #     TTT = acc_2 * acc_1 * acc_0
        #     FTT = (1-acc_2)*(acc_1)*(acc_0)
        #     TFT = (acc_2)*(1-acc_1)*(acc_0)
        #     TTF = (acc_2)*(acc_1)*(1-acc_0)
        #     prob_ = TTT + FTT + TFT + TTF

        #     if prob_ >= self.exnet.threshold:

        #         pred_2 = self.exnet.exactly[prev_2].pred
        #         pred_1 = self.exnet.exactly[prev_1].pred
        #         pred_0 = self.exnet.exactly[prev_0].pred

        #         _, pred_2 = torch.max(pred_2,1)
        #         _, pred_1 = torch.max(pred_1,1)
        #         _, pred_0 = torch.max(pred_0,1)

        #         pred_stack = torch.column_stack((pred_0,pred_1,pred_2))
        #         count = [torch.bincount(i) for i in pred_stack]
                
        #         _pred = torch.zeros([x.shape[0]])
        #         for n, m in enumerate(count):
        #             if m.max() != 1:
        #                 _pred[n] = torch.argmax(m)
        #             else:
        #                 #_pred[n] = pred_stack[n,0]
        #                 return x

        #         self.exnet._pred = _pred
        #         raise ExException(self.id)

        if self.exit:
            raise ExException(self.id)
        return x

class ExAct(nn.Module):
    def __init__(self,activation="relu", num_class=10, id=0, exnet=None ):
        super(ExAct, self).__init__()
        self.id = id
        self.branch = False
        self.branch_uninitialized = True
        self.num_class = num_class
        self.exnet = exnet

        self.activation = nn.ReLU()    
        self.hidden = 32
        self.size = 32
        self.expansion = self.size * self.size
        
        self.tim = 1.0
        self.acc = 1.0

        self.loss = 0.0

        self.sigmoid = nn.Sigmoid()

        self.classifier = nn.Linear(self.hidden * self.expansion, self.num_class)

        self.threshold = 0.16


    def t_prepare(self, acc):
        self.acc = acc

    def exbranch_setup(self, input):

        batch, channel, width, height = input.shape
        print(input.shape)
        self.refit = nn.Sequential(
            nn.Conv2d(in_channels=channel, out_channels=self.hidden, kernel_size=1, bias=False)
            ,nn.AdaptiveAvgPool2d((self.size, self.size))
        ).cuda()
        

   
    
    def forward(self, x , open=None):
        x = self.activation(x)
    
        if self.branch:
            if self.branch_uninitialized:
                self.exbranch_setup(x)
                self.branch_uninitialized = False
            x0 = self.refit(x)
            x0 = x0.view(x0.size(0), -1)
            self.pred = self.classifier(x0)
            self.p = self.sigmoid(self.pred)
            self.conf = -1 * torch.nansum((self.p) * torch.log(self.p),dim=1) / self.num_class
            self.sum_conf = torch.sum(self.conf) 

            if self.exnet.test_mode:
                assert x.shape[0] < 2
                if self.conf[0] < self.threshold:
                    #print("gate: ",self.id," entropy: {:.2f}",self.id, self.conf[0])
                    if not ((self.id + 1) is self.exnet.ex_num):
                        self.exnet.set_exit(self.id + 1 , True)    
        return x

