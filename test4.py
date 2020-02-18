"""
        利用torch训练神经网络举例，参考https://pytorch.org/tutorials/beginner/nn_tutorial.html
        使用mnist数据集进行训练，其图片为0-9数字灰度图，每行代表一张图片，训练集维度为50000*784
        网络只包含了线性层和一个激活层
        引入 nn.Module和nn.Parameter 改进代码
"""
from pathlib import Path
import requests
import pickle
import gzip
import matplotlib.pyplot as plt
from matplotlib import pyplot
import numpy as np
import torch
import math
from torch import nn
"""
        导入mnist数据集
"""
FILENAME = "mnist.pkl.gz"
DATA_PATH = Path("data")
PATH = DATA_PATH / "mnist"

with gzip.open((PATH / FILENAME).as_posix(), "rb") as f:
        ((x_train, y_train), (x_valid, y_valid), _) = pickle.load(f, encoding="latin-1")


#plt.imshow(x_train[0].reshape((28, 28)), cmap="gray")
#plt.show()
#print(x_train.shape)
#print(y_train)
#print((y_train.shape))

#将numpy转换为tensor
x_train,y_train,x_valid,y_valid=map(torch.tensor,(x_train,y_train,x_valid,y_valid))
n,c=x_train.shape
weights=torch.randn(784,10)/math.sqrt(784)
#print(weights.shape)
weights.requires_grad_()
bias=torch.zeros(10,requires_grad=True)


"""
    定义激活函数和损失函数
    如果我们的网络中使用 negative log likelihood loss 作为损失函数， 
    log softmax activation 作为激活函数 （即我们上面实现的损失函数与激活函数）。
    在pytorch中我们直接使用函数 F.cross_entropy 便可实现上面两个函数的功能
"""
import torch.nn.functional as F
loss_func=F.cross_entropy
#def model(xb):
 #   return xb@weights+bias

bs=64#bitch size
xb=x_train[0:bs]
#print(xb.shape)
#preds=model(xb)
yb = y_train[0:bs]

"""
    定义计算准确度的函数
"""
def accuracy(out, yb):
    preds = torch.argmax(out, dim=1)  # 返回每行中最大元素所在列的位置
    return (preds == yb).float().mean()


#print('未训练前的损失函数',loss_func(model(xb), yb))
#print('未训练前的准确率', accuracy(model(xb), yb))
"""
    定义网络模型
"""
class Mnist_Logistic(nn.Module):
    def __init__(self):
        super().__init__()
        #self.weights=nn.parameter
        #self.bias=nn.parameter(torch.zero(10))
        self.weights = nn.Parameter(torch.randn(784, 10) / math.sqrt(784))#注意这里的Parameter的首字母因为大写？
        self.bias = nn.Parameter(torch.zeros(10))
    def forward(self,xb):
        return xb@self.weights+self.bias

model = Mnist_Logistic()
print('未训练前的损失函数',loss_func(model(xb), yb))#注意此处的model(xb)表示的是线性层的输出，而test3中的表示激活层的输出
#print('未训练前的准确率', accuracy(model(xb), yb))


"""
        开始循环训练模型
        1.选择一个mini bitch
        2.用模型得到预测结果
        3.计算损失函数值
        4.loss.backward()更新模型的梯度，在这里是权值（weights）和偏移（bias）
        5.用梯度去更新权值和偏移
"""
lr=0.9#学习率
epochs=10
def fit():
    for epoch in range(epochs):
        for i in range((n-1)//bs+1):
            start_i=i*bs
            end_i=start_i+bs
            xb=x_train[start_i:end_i]
            yb=y_train[start_i:end_i]
            pred=model(xb)
            loss=loss_func(pred,yb)

            loss.backward()
            with torch.no_grad():
                for p in model.parameters():
                    p-=p.grad*lr
                model.zero_grad()

fit()
print('训练后的损失函数',loss_func(model(xb), yb))
#print('训练后的准确率', accuracy(model(xb), yb))
