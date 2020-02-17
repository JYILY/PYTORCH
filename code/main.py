from PyQt5.QtWidgets import QApplication, QMainWindow,QWidget
from PyQt5.QtGui import QPixmap, QPainter, QPen, QColor
from PyQt5.QtCore import Qt, QPoint, QSize
from PyQt5 import QtCore, QtGui, QtWidgets
from PIL import Image, ImageQt
import UI

import torch
import torch.nn as nn
import torch.nn.functional as F
import numpy as np
import sys

class CNN(nn.Module):   
    def __init__(self):
        super(CNN,self).__init__()
        self.cv_mp1 = nn.Sequential(
            nn.Conv2d(1,20,5,1),
            nn.MaxPool2d(2,2)
        )
        self.cv_mp2 = nn.Sequential(
            nn.Conv2d(20,50,3,1),
            nn.MaxPool2d(2,2)
        )
        self.fc1=nn.Linear(50*5*5,256)
        self.fc2=nn.Linear(256,64)
        self.fc3=nn.Linear(64,10)
    
    def forward(self,x):
        x = F.relu(self.cv_mp1(x))
        x = F.relu(self.cv_mp2(x))
        x = x.view(x.size(0),-1)
        x = F.relu(self.fc1(x))
        x = F.relu(self.fc2(x))
        x = self.fc3(x)
        return x

class Linear(nn.Module):   
    def __init__(self):
        super(Linear,self).__init__()
        self.fc = nn.Sequential(
            nn.Linear(784,256),
            nn.ReLU(),
            nn.Linear(256,98),
            nn.ReLU(),
            nn.Linear(98,10)
        )
    
    def forward(self,x):
        x = x.view(x.size(0),784)
        return self.fc(x)

cnn = CNN()
cnn.load_state_dict(torch.load('../module/CNN.pkl'))
linear = Linear()
linear.load_state_dict(torch.load('../module/linear.pkl'))

def identify():
	img = ui.paintBoard.toImage()
	pil_img = ImageQt.fromqimage(img)
	pil_img = pil_img.resize((28, 28), Image.ANTIALIAS).convert('L')
	img_array = np.array(pil_img.convert('L')).reshape(1,1,28,28)/255.0
	img_tensor = torch.from_numpy(img_array).float()
	p = None
	if ui.pushButton_3.text() == 'CNN':
		p = F.softmax(cnn(img_tensor),dim=1)
	else :
		p = F.softmax(linear(img_tensor),dim=1)
	plist = p.tolist()[0]
	result = p.argmax(dim=1).item()

	ui.label_7.setText(str(result))

	ui.label_00.setText("0:   %.2f"%(plist[0]))
	ui.label_11.setText("1:   %.2f"%(plist[1]))
	ui.label_22.setText("2:   %.2f"%(plist[2]))
	ui.label_33.setText("3:   %.2f"%(plist[3]))
	ui.label_44.setText("4:   %.2f"%(plist[4]))
	ui.label_55.setText("5:   %.2f"%(plist[5]))
	ui.label_66.setText("6:   %.2f"%(plist[6]))
	ui.label_77.setText("7:   %.2f"%(plist[7]))
	ui.label_88.setText("8:   %.2f"%(plist[8]))
	ui.label_99.setText("9:   %.2f"%(plist[9]))

if __name__ == '__main__':
	app = QApplication(sys.argv)
	MainWindow = QMainWindow()
	ui = UI.Ui_MainWindow()
	ui.setupUi(MainWindow)
	MainWindow.show()
	ui.pushButton.clicked.connect(identify)

	sys.exit(app.exec_())