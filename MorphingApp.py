import sys
import numpy as np
import scipy
import imageio
import os
from PIL import Image, ImageDraw

from scipy.spatial import Delaunay
from scipy import interpolate

from PySide.QtCore import *
from PySide.QtGui import *

from MorphingGUI import *

import Morphing

from pathlib import Path

class MorphingApp(QMainWindow, Ui_MainWindow):

    def __init__(self, parent=None):
        super(MorphingApp, self).__init__(parent)
        self.setupUi(self)

        self.startPoints = []
        self.startPointsNP = []
        self.endPoints = []
        self.endPointsNP = []
        self.startFilePath = ''
        self.endFilePath = ''

        self.startScene = QGraphicsScene(self.displayStartImage)
        self.startSceneTri = QGraphicsScene(self.displayStartImage)
        self.endScene = QGraphicsScene(self.displayEndImage)
        self.endSceneTri = QGraphicsScene(self.displayStartImage)
        self.blendScene = QGraphicsScene(self.displayBlendImage)

        self.alphaSlider.setRange(0, 20)
        self.alphaSlider.setSingleStep(1)
        self.alpha = 0

        self.LoadStartImage.clicked.connect(self.loadStartImageFlag)
        self.LoadEndImage.clicked.connect(self.loadEndImageFlag)
        self.showTriangles.stateChanged.connect(self.showDelaunay)
        self.alphaSlider.valueChanged.connect(self.getAlpha)
        self.blendButton.clicked.connect(self.loadBlendImage)

        self.startImageImRead = []
        self.endImageImRead = []

        self.scalexStart = 0
        self.scaleyStart = 0
        self.scalexEnd = 0
        self.scaleyEnd = 0
        self.startTempCoor = []
        self.endTempCoor = []


        self.showTriangles.setDisabled(True)
        self.alphaSlider.setDisabled(True)
        self.displayAlpha.setDisabled(True)
        self.blendButton.setDisabled(True)

        self.startImageFlag = False
        self.startPointsExist = True
        self.endImageFlag = False
        self.endPointsExist = True
        self.nextPair = True
        self.selectionPending = False
        self.removePointEnable = False

    def loadStartImageFlag(self):
        self.startFilePath, _ = QFileDialog.getOpenFileName(self, caption='Open PNG or JPEG file ...')

        if not self.startFilePath:
            return

        input_path = Path(self.startFilePath + '.txt')
        if input_path.exists():
            self.startPointsExist = True

        else:
            self.startPointsExist = False

        self.loadStartImage()

    def loadStartImage(self):

        startPixMap = QPixmap(self.startFilePath)
        self.scalexStart = self.displayStartImage.width() / startPixMap.width()
        self.scaleyStart = self.displayStartImage.height() / startPixMap.height()

        self.startScene.addPixmap(startPixMap.scaled(self.displayStartImage.size(), QtCore.Qt.KeepAspectRatio))
        self.startSceneTri.addPixmap(startPixMap.scaled(self.displayStartImage.size(), QtCore.Qt.KeepAspectRatio))
        self.displayStartImage.setHorizontalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
        self.displayStartImage.setVerticalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
        self.displayStartImage.setScene(self.startSceneTri)

        if self.startPointsExist == True:
            with open(self.startFilePath + '.txt', 'r') as myFile:
                lines = myFile.readlines()

            for line in lines:
                (x, y) = line.split()
                x = self.scalexStart * float(x)
                y = self.scaleyStart * float(y)
                self.startScene.addEllipse(x, y, 2, 2, QPen(Qt.red, 2), Qt.SolidPattern)
                self.startSceneTri.addEllipse(x, y, 2, 2, QPen(Qt.red, 2), Qt.SolidPattern)
                self.startPoints.append((x,y))

        self.displayStartImage.mousePressEvent = self.getMouseStart
        self.displayStartImage.keyPressEvent = self.removePointStart

        self.startImageFlag = True
        if self.endImageFlag == True:
            self.enableWidgets()

    def loadEndImageFlag(self):
        self.endFilePath, _ = QFileDialog.getOpenFileName(self, caption='Open PNG or JPEG file ...')

        if not self.endFilePath:
            return

        input_path = Path(self.endFilePath + '.txt')
        if input_path.exists():
            self.endPointsExist = True

        else:
            self.endPointsExist = False

        self.loadEndImage()


    def loadEndImage(self):
        endPixMap = QPixmap(self.endFilePath)
        self.scalexEnd = self.displayEndImage.width() / endPixMap.width()
        self.scaleyEnd = self.displayEndImage.height() / endPixMap.height()

        self.endScene.addPixmap(endPixMap.scaled(self.displayEndImage.size(), QtCore.Qt.KeepAspectRatio))
        self.endSceneTri.addPixmap(endPixMap.scaled(self.displayEndImage.size(), QtCore.Qt.KeepAspectRatio))
        self.displayEndImage.setHorizontalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
        self.displayEndImage.setVerticalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
        self.displayEndImage.setScene(self.endSceneTri)

        if self.endPointsExist == True:
            with open(self.endFilePath + '.txt', 'r') as myFile:
                lines = myFile.readlines()

            for line in lines:
                (x, y) = line.split()
                x = self.scalexEnd * float(x)
                y = self.scaleyEnd * float(y)
                self.endScene.addEllipse(x, y, 2, 2, QPen(Qt.red, 2), Qt.SolidPattern)
                self.endSceneTri.addEllipse(x, y, 2, 2, QPen(Qt.red, 2), Qt.SolidPattern)
                self.endPoints.append((x,y))

        self.displayEndImage.mousePressEvent = self.getMouseEnd
        self.displayEndImage.keyPressEvent = self.removePointEnd
        self.displayStartImage.mouseReleaseEvent = self.confirmSelectionWithStartImage
        self.mousePressEvent = self.confirmSelection


        self.endImageFlag = True
        if self.startImageFlag == True:
            self.enableWidgets()


    def enableWidgets(self):
        if self.startImageFlag == True and self.endImageFlag == True:
            self.showTriangles.setDisabled(False)
            self.alphaSlider.setDisabled(False)
            self.displayAlpha.setDisabled(False)
            self.blendButton.setDisabled(False)

    def showDelaunay(self):
        try:
            self.displayStartImage.setScene(self.startSceneTri)
            self.displayEndImage.setScene(self.endSceneTri)
            startTriangle = []
            endTriangle = []

            if self.showTriangles.checkState() == Qt.Checked:
                delaunayTri = Delaunay(self.startPoints).simplices


                for i in range(len(delaunayTri)):
                    for j in range(len(delaunayTri[i])):
                        index = delaunayTri[i][j]

                        startTriangle.append([self.startPoints[index][0], self.startPoints[index][1]])
                        endTriangle.append([self.endPoints[index][0], self.endPoints[index][1]])

                    self.startSceneTri.addLine(QLineF(startTriangle[0][0], startTriangle[0][1], startTriangle[1][0], startTriangle[1][1]), QPen(Qt.red, 2))
                    self.startSceneTri.addLine(QLineF(startTriangle[0][0], startTriangle[0][1], startTriangle[2][0], startTriangle[2][1]), QPen(Qt.red, 2))
                    self.startSceneTri.addLine(QLineF(startTriangle[1][0], startTriangle[1][1], startTriangle[2][0], startTriangle[2][1]), QPen(Qt.red, 2))
                    startTriangle = []
                    self.endSceneTri.addLine(QLineF(endTriangle[0][0], endTriangle[0][1], endTriangle[1][0], endTriangle[1][1]), QPen(Qt.red, 2))
                    self.endSceneTri.addLine(QLineF(endTriangle[0][0], endTriangle[0][1], endTriangle[2][0], endTriangle[2][1]), QPen(Qt.red, 2))
                    self.endSceneTri.addLine(QLineF(endTriangle[1][0], endTriangle[1][1], endTriangle[2][0], endTriangle[2][1]), QPen(Qt.red, 2))
                    endTriangle = []


            if self.showTriangles.checkState() == Qt.Unchecked:
                self.displayStartImage.setScene(self.startScene)
                self.displayEndImage.setScene(self.endScene)
        except:
            pass

    def getAlpha(self):
        self.alpha = self.alphaSlider.value() / 20
        alphaString = '{0:0.2f}'.format(self.alpha)
        self.displayAlpha.setText(alphaString)

    def loadBlendImage(self):

        self.endImageImRead = imageio.imread(self.endFilePath)
        self.startImageImRead = imageio.imread(self.startFilePath)
        self.startPointsNP = np.loadtxt(self.startFilePath + '.txt', usecols=range(2), dtype=np.float64)
        self.endPointsNP = np.loadtxt(self.endFilePath + '.txt', usecols=range(2), dtype=np.float64)


        blenderInstance = Morphing.Blender(self.startImageImRead, self.startPointsNP, self.endImageImRead, self.endPointsNP)
        myImage = blenderInstance.getBlendedImage(self.alpha)
        imageio.imwrite('blendedImage.png', myImage)
        blendPixMap = QPixmap('blendedImage.png')
        self.blendScene.addPixmap(blendPixMap.scaled(self.displayBlendImage.size(), QtCore.Qt.KeepAspectRatio))
        self.displayBlendImage.setHorizontalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
        self.displayBlendImage.setVerticalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
        self.displayBlendImage.setScene(self.blendScene)

    def getMouseStart(self, event):
        if len(self.startTempCoor) == len(self.endTempCoor) and self.nextPair == True:
            self.startSceneTri.addEllipse(event.pos().x(), event.pos().y(), 2, 2, QPen(Qt.green, 2), Qt.SolidPattern)
            self.startScene.addEllipse(event.pos().x(), event.pos().y(), 2, 2, QPen(Qt.green, 2), Qt.SolidPattern)
            self.startTempCoor.append([event.pos().x(), event.pos().y()])
            self.nextPair = False
            self.selectionPending = False
            self.removePointEnable = True

    def getMouseEnd(self, event):
        if len(self.startTempCoor) != len(self.endTempCoor):
            self.endSceneTri.addEllipse(event.pos().x(), event.pos().y(), 2, 2, QPen(Qt.green, 2), Qt.SolidPattern)
            self.endScene.addEllipse(event.pos().x(), event.pos().y(), 2, 2, QPen(Qt.green, 2), Qt.SolidPattern)
            self.endTempCoor.append([event.pos().x(), event.pos().y()])
            self.nextPair = False
            self.selectionPending = True
            self.removePointEnable = True

    def removePointStart(self, event):
        if event.key() == Qt.Key_Backspace and self.removePointEnable == True:
            self.startTempCoor.pop()
            self.startSceneTri.removeItem(self.startSceneTri.items()[0])
            self.startScene.removeItem(self.startScene.items()[0])
            self.removePointEnable = False
            self.nextPair = True

    def removePointEnd(self, event):
        if event.key() == Qt.Key_Backspace and self.removePointEnable == True:
            self.endTempCoor.pop()
            self.endSceneTri.removeItem(self.endSceneTri.items()[0])
            self.endScene.removeItem(self.endScene.items()[0])
            self.removePointEnable = False

    def confirmSelection(self, event):
        self.nextPair = True
        if self.selectionPending == True:
            self.startPoints.append([self.startTempCoor[-1][0], self.startTempCoor[-1][1]])
            self.endPoints.append([self.endTempCoor[-1][0], self.endTempCoor[-1][1]])
            self.startSceneTri.removeItem(self.startSceneTri.items()[0])
            self.startSceneTri.addEllipse(self.startPoints[-1][0], self.startPoints[-1][1], 2, 2, QPen(Qt.blue, 2), Qt.SolidPattern)
            self.startScene.removeItem(self.startScene.items()[0])
            self.startScene.addEllipse(self.startPoints[-1][0], self.startPoints[-1][1], 2, 2, QPen(Qt.blue, 2), Qt.SolidPattern)
            self.endScene.removeItem(self.endScene.items()[0])
            self.endScene.addEllipse(self.endPoints[-1][0], self.endPoints[-1][1], 2, 2, QPen(Qt.blue, 2), Qt.SolidPattern)
            self.endSceneTri.removeItem(self.endSceneTri.items()[0])
            self.endSceneTri.addEllipse(self.endPoints[-1][0], self.endPoints[-1][1], 2, 2, QPen(Qt.blue, 2), Qt.SolidPattern)

            if self.startPointsExist == True:
                with open(self.startFilePath + '.txt', 'a') as myFile1:
                    myFile1.write('\n')
                    myFile1.write('{} {}'.format(int(self.startPoints[-1][0]/self.scalexStart), int(self.startPoints[-1][1]/self.scaleyStart)))
            elif self.startPointsExist == False:
                with open(self.startFilePath + '.txt', 'a') as myFile1:
                    myFile1.write('{} {}'.format(int(self.startPoints[-1][0]/self.scalexStart), int(self.startPoints[-1][1]/self.scaleyStart)))
                    myFile1.write('\n')

            if self.endPointsExist == True:
                with open(self.endFilePath + '.txt', 'a') as myFile2:
                    myFile2.write('\n')
                    myFile2.write('{} {}'.format(int(self.endPoints[-1][0]/self.scalexEnd), int(self.endPoints[-1][1]/self.scaleyEnd)))
            elif self.endPointsExist == False:
                with open(self.endFilePath + '.txt', 'a') as myFile2:
                    myFile2.write('{} {}'.format(int(self.endPoints[-1][0]/self.scalexEnd), int(self.endPoints[-1][1]/self.scaleyEnd)))
                    myFile2.write('\n')

            if self.showTriangles.checkState() == Qt.Checked:
                self.showDelaunay()

    def confirmSelectionWithStartImage(self, event):
        self.confirmSelection(event)
        self.getMouseStart(event)




if __name__ == "__main__":
     currentApp = QApplication(sys.argv)
     currentForm = MorphingApp()

     currentForm.show()
     currentApp.exec_()