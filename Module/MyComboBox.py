import PyQt5
from PyQt5.QtCore import *
from PyQt5.QtWidgets import *

from DButil import MyDButil


class Combox(QComboBox):
    singnal = pyqtSignal(str)
    def __init__(self, parent=None):
        super(Combox, self).__init__(parent)

    # def getItem(self):
    #     db = MyDButil()
    #     sql = "show tables from ocr;"
    #     result = db.fetch_all(sql)
    #     return result



    def showPopup(self):
        print("触发pop函数")
        self.singnal.emit("发射信号")
        super(Combox, self).showPopup()
        # self.clear()
        # items = []
        # items.clear()
        # self.addItem("请选择一个模板")
        # result = self.getItem()
        # for item in result:
        #     items.append(item[0])
        # self.addItems(items)
        #
        # QComboBox.showPopup(self)