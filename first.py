# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'untitled.ui'
#
# Created by: PyQt5 UI code generator 5.9.2
#
# WARNING! All changes made in this file will be lost!
import sys

from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtCore import QEvent, Qt, pyqtSignal
from PyQt5.QtGui import QMouseEvent
from PyQt5.QtWidgets import *

from DButil import MyDButil


class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        MainWindow.setObjectName("MainWindow")
        MainWindow.resize(800, 600)
        self.centralwidget = QtWidgets.QWidget(MainWindow)
        self.centralwidget.setObjectName("centralwidget")
        self.comboBox = Combox(self.centralwidget)

        self.comboBox.setGeometry(QtCore.QRect(380, 100, 131, 51))
        self.comboBox.setObjectName("comboBox")
        self.comboBox.showPopup()
        # self.comboBox.addItem("1")
        # self.comboBox.addItem("2")
        # self.comboBox.addItem("3")
        # self.comboBox.addItems(['4', '5', '6'])
        # self.comboBox.currentIndexChanged.connect(lambda :self.Writting(self.comboBox.currentIndex()))
        # self.comboBox.currentIndexChanged.connect(self.mouseDoubleClickEvent())

        MainWindow.setCentralWidget(self.centralwidget)
        self.menubar = QtWidgets.QMenuBar(MainWindow)
        self.menubar.setGeometry(QtCore.QRect(0, 0, 800, 34))
        self.menubar.setObjectName("menubar")
        MainWindow.setMenuBar(self.menubar)
        self.statusbar = QtWidgets.QStatusBar(MainWindow)
        self.statusbar.setObjectName("statusbar")
        MainWindow.setStatusBar(self.statusbar)

        self.retranslateUi(MainWindow)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

    def eventFilter(self, obj, event):
        if obj == self.comboBox:
            print("是")
            if event.type() == QEvent.MouseButtonPress:
                mouseEvent = QMouseEvent(event)
                if mouseEvent.buttons() == Qt.LeftButton:
                    print("左击")
                    self.Writting(self.comboBox.currentIndex())
        return QDialog.eventFilter(self, obj, event)

    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "MainWindow"))

    def Writting(self, tag):
        print("点到了", tag)

    def mouseDoubleClickEvent(self, event):
        if event.buttons() == Qt.LeftButton:
            print("左击")
        if event.buttons() == Qt.RightButton:
            print("右击了")
        # self.comboBox.removeItem(tag)


class Combox(QComboBox):
    singnal = pyqtSignal()

    def __init__(self, parent=None):
        super(Combox, self).__init__(parent)

    def mousePressEvent(self, QMouseEvent):

        if QMouseEvent.buttons == Qt.LeftButton:
            print("左击")
        pass

    def getItem(self):
        db = MyDButil()
        sql = "show tables from ocr;"
        result = db.fetch_all(sql)
        return result

    def showPopup(self):
        QComboBox.showPopup(self)
        self.clear()
        items = []
        items.clear()
        self.addItem("请选择一个模板")
        result = self.getItem()
        for item in result:
            items.append(item[0])
        self.addItems(items)
        QComboBox.showPopup(self)


if __name__ == '__main__':
    app = QApplication(sys.argv)
    MainWindow = QMainWindow()
    ui = Ui_MainWindow()
    ui.setupUi(MainWindow)
    MainWindow.show()
    sys.exit(app.exec_())
