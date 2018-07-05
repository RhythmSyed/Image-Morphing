# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'MorphingGUI.ui'
#
# Created: Tue Apr 17 12:10:29 2018
#      by: pyside-uic 0.2.15 running on PySide 1.2.2
#
# WARNING! All changes made in this file will be lost!

from PySide import QtCore, QtGui

class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        MainWindow.setObjectName("MainWindow")
        MainWindow.resize(955, 843)
        self.centralwidget = QtGui.QWidget(MainWindow)
        self.centralwidget.setObjectName("centralwidget")
        self.LoadStartImage = QtGui.QPushButton(self.centralwidget)
        self.LoadStartImage.setGeometry(QtCore.QRect(20, 10, 161, 27))
        self.LoadStartImage.setObjectName("LoadStartImage")
        self.LoadEndImage = QtGui.QPushButton(self.centralwidget)
        self.LoadEndImage.setGeometry(QtCore.QRect(520, 10, 161, 27))
        self.LoadEndImage.setObjectName("LoadEndImage")
        self.startingImageLabel = QtGui.QLabel(self.centralwidget)
        self.startingImageLabel.setGeometry(QtCore.QRect(160, 340, 131, 17))
        self.startingImageLabel.setObjectName("startingImageLabel")
        self.endingImageLabel = QtGui.QLabel(self.centralwidget)
        self.endingImageLabel.setGeometry(QtCore.QRect(670, 340, 131, 17))
        self.endingImageLabel.setObjectName("endingImageLabel")
        self.showTriangles = QtGui.QCheckBox(self.centralwidget)
        self.showTriangles.setGeometry(QtCore.QRect(410, 340, 141, 22))
        self.showTriangles.setObjectName("showTriangles")
        self.alphaSlider = QtGui.QSlider(self.centralwidget)
        self.alphaSlider.setGeometry(QtCore.QRect(100, 370, 741, 20))
        self.alphaSlider.setOrientation(QtCore.Qt.Horizontal)
        self.alphaSlider.setObjectName("alphaSlider")
        self.alphaLabel = QtGui.QLabel(self.centralwidget)
        self.alphaLabel.setGeometry(QtCore.QRect(50, 370, 62, 17))
        self.alphaLabel.setObjectName("alphaLabel")
        self.zeroSliderLabel = QtGui.QLabel(self.centralwidget)
        self.zeroSliderLabel.setGeometry(QtCore.QRect(100, 390, 31, 17))
        self.zeroSliderLabel.setObjectName("zeroSliderLabel")
        self.oneSliderLabel = QtGui.QLabel(self.centralwidget)
        self.oneSliderLabel.setGeometry(QtCore.QRect(830, 390, 31, 17))
        self.oneSliderLabel.setObjectName("oneSliderLabel")
        self.displayAlpha = QtGui.QLineEdit(self.centralwidget)
        self.displayAlpha.setGeometry(QtCore.QRect(860, 370, 61, 21))
        self.displayAlpha.setObjectName("displayAlpha")
        self.blendImageLabel = QtGui.QLabel(self.centralwidget)
        self.blendImageLabel.setGeometry(QtCore.QRect(440, 700, 131, 17))
        self.blendImageLabel.setObjectName("blendImageLabel")
        self.blendButton = QtGui.QPushButton(self.centralwidget)
        self.blendButton.setGeometry(QtCore.QRect(430, 740, 121, 27))
        self.blendButton.setObjectName("blendButton")
        self.displayStartImage = QtGui.QGraphicsView(self.centralwidget)
        self.displayStartImage.setGeometry(QtCore.QRect(20, 40, 400, 300))
        self.displayStartImage.setObjectName("displayStartImage")
        self.displayEndImage = QtGui.QGraphicsView(self.centralwidget)
        self.displayEndImage.setGeometry(QtCore.QRect(520, 40, 400, 300))
        self.displayEndImage.setObjectName("displayEndImage")
        self.displayBlendImage = QtGui.QGraphicsView(self.centralwidget)
        self.displayBlendImage.setGeometry(QtCore.QRect(290, 400, 400, 300))
        self.displayBlendImage.setObjectName("displayBlendImage")
        MainWindow.setCentralWidget(self.centralwidget)
        self.menubar = QtGui.QMenuBar(MainWindow)
        self.menubar.setGeometry(QtCore.QRect(0, 0, 955, 25))
        self.menubar.setObjectName("menubar")
        MainWindow.setMenuBar(self.menubar)
        self.statusbar = QtGui.QStatusBar(MainWindow)
        self.statusbar.setObjectName("statusbar")
        MainWindow.setStatusBar(self.statusbar)

        self.retranslateUi(MainWindow)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

    def retranslateUi(self, MainWindow):
        MainWindow.setWindowTitle(QtGui.QApplication.translate("MainWindow", "MainWindow", None, QtGui.QApplication.UnicodeUTF8))
        self.LoadStartImage.setText(QtGui.QApplication.translate("MainWindow", "Load Starting Image ...", None, QtGui.QApplication.UnicodeUTF8))
        self.LoadEndImage.setText(QtGui.QApplication.translate("MainWindow", "Load Ending Image ...", None, QtGui.QApplication.UnicodeUTF8))
        self.startingImageLabel.setText(QtGui.QApplication.translate("MainWindow", "Starting Image", None, QtGui.QApplication.UnicodeUTF8))
        self.endingImageLabel.setText(QtGui.QApplication.translate("MainWindow", "Ending Image", None, QtGui.QApplication.UnicodeUTF8))
        self.showTriangles.setText(QtGui.QApplication.translate("MainWindow", "Show Triangles", None, QtGui.QApplication.UnicodeUTF8))
        self.alphaLabel.setText(QtGui.QApplication.translate("MainWindow", "Alpha", None, QtGui.QApplication.UnicodeUTF8))
        self.zeroSliderLabel.setText(QtGui.QApplication.translate("MainWindow", "0.0", None, QtGui.QApplication.UnicodeUTF8))
        self.oneSliderLabel.setText(QtGui.QApplication.translate("MainWindow", "1.0", None, QtGui.QApplication.UnicodeUTF8))
        self.blendImageLabel.setText(QtGui.QApplication.translate("MainWindow", "Blending Result", None, QtGui.QApplication.UnicodeUTF8))
        self.blendButton.setText(QtGui.QApplication.translate("MainWindow", "Blend", None, QtGui.QApplication.UnicodeUTF8))

