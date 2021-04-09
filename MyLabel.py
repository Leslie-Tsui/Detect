import os
from PyQt5.QtWidgets import *
from Util import DButil
from DButil import MyDButil
from PyQt5.QtGui import QPixmap, QPalette, QImage, QIcon, QPainter, QPen, QCursor, QFont
from PyQt5.QtCore import Qt, QRect



class MyLabel(QLabel):
    def __init__(self, *args, **kw):
        super().__init__(*args, **kw)
        self.setContextMenuPolicy(Qt.CustomContextMenu)
        self.customContextMenuRequested.connect(self.mouseReleaseEvent)  # 开放右键策略
        self.rects = {}

    Newfile = './'
    x0 = 0
    y0 = 0
    x1 = 0
    y1 = 0
    flag = False
    order = None
    isLeftPressed = False
    rect_temp = None
    lable_line = None  # 添加文本框

    # def rightMenuShow(self, pos):  # 添加右键菜单
    #     menu = QMenu(self)
    #     menu.addAction(QAction('保存', menu))
    #     menu.addAction(QAction('重画', menu))
    #     menu.addAction(QAction('退出', menu))
    #     menu.triggered.connect(self.menuSlot)
    #     menu.exec_(QCursor.pos())

    # 右键菜单事件
    def menuSlot(self, act):
        if act.text() == '保存':
            flag = self.saveSample()
            if flag:
                print('保存')
            else:
                print("保存失败")
        if act.text() == '重画':
            self.rects = {}  # 点击重画后，将rects字典清空
            full_path = '.\\info.txt'
            file = open(full_path, 'a')  # 覆盖写入的模式
            file.write("")
            file.close()
            print('重画')
        if act.text() == '退出':
            print('退出')

    # def continuecreateRoi(self):
    #     fname, ok = QFileDialog.getOpenFileName(self, '选择图片', '.bmp', ("Images (*.bmp *.jpg *.tif *.raw)"))
    #     image = QImage(fname)
    #     h = image.width()
    #     w = image.height()
    #     self.label.resize(h, w)
    #     self.label.setPixmap(QPixmap.fromImage(image))  # 加载图片
    #     self.label.setCursor(Qt.CrossCursor)

    # 鼠标点击事件
    def mousePressEvent(self, event):
        if event.buttons() == Qt.LeftButton:  # 左击表示创建矩形框
            self.flag = True
            self.x0 = event.x()
            self.y0 = event.y()
        if event.buttons() == Qt.RightButton:  # 右击显示菜单,保存
            self.flag = False

    def mouseMoveEvent(self, event):
        if self.flag:
            self.x1 = event.x()
            self.y1 = event.y()
            self.update()

    # 回车事件
    def returnPressed(self):
        print("这是回车获取的标签文本框内容", str((self.lable_line.text())))
        print("这是回车获取的初始数据文本框内容", str((self.data_line.text())))
        self.order = str((self.lable_line.text()))
        self.origin_data = str((self.data_line.text()))
        self.rects.update({str(self.order): [(self.order), list(self.rect_temp.getRect()), self.origin_data]})
        self.update()

    # 鼠标释放事件
    def mouseReleaseEvent(self, event):
        menu = QMenu(self)
        if self.flag:
            rect = QRect(self.x0, self.y0, abs(self.x1 - self.x0), abs(self.y1 - self.y0))
            self.rect_temp = rect
            # self.rect.append(rect)
            # dict(self.rects)[str(self.order)] = [(self.order),[rect]]
            # self.update()
            self.lable_line = QLineEdit(self)  # 添加标签的文本框
            self.data_line = QLineEdit(self)  # 添加原始数据的文本框

            self.lable_line.setPlaceholderText("输入序号，回车保存")  # 给文本框设置背景文字
            self.data_line.setPlaceholderText("输入此标签下的原始数据")

            self.lable_line.editingFinished.connect(self.returnPressed)
            self.data_line.editingFinished.connect(self.returnPressed)
            self.lable_line.setFocus()

            action_label_line = QWidgetAction(menu)
            action_data_line = QWidgetAction(menu)

            action_label_line.setDefaultWidget(self.lable_line)
            action_data_line.setDefaultWidget(self.data_line)
            menu.addAction(action_label_line)
            menu.addAction(action_data_line)
            menu.exec_(QCursor.pos())
        else:
            menu.addAction(QAction('保存', menu))
            menu.addAction(QAction('继续添加模板', menu))
            menu.addAction(QAction('重画', menu))
            menu.addAction(QAction('退出', menu))
            menu.triggered.connect(self.menuSlot)
            menu.exec_(QCursor.pos())

    # 保存模板事件
    def saveSample(self):  # 保存模板
        flag = False
        table_name, ok = QInputDialog().getText(QWidget(), '创建模板', '输入新模板名:')
        sql1 = "drop table if exists " + table_name + ";"
        sql2 = "create table " + table_name + "(label_id varchar(255) not null,x0 varchar(255),y0 varchar(255),x1 varchar(255),y1 varchar(255),origin_data varchar(255));"
        print(sql1)
        print(sql2)

        dbutil = DButil.MyDButil()
        flag = dbutil.update(sql1)
        flag = dbutil.update(sql2)
        print(flag)
        if flag:
            QMessageBox.information(self, "操作提示", "保存模板名字成功", QMessageBox.Yes | QMessageBox.No)
        else:
            QMessageBox.information(self, "操作提示", "保存模板名字失败", QMessageBox.Yes | QMessageBox.No)

        for key, value in dict(self.rects).items():
            sql = "insert into " + table_name + " values('" + key + "','" + str(value[1][0]) + "','" + str(
                value[1][1]) + "','" + str(value[1][2]) + "','" + str(value[1][3]) + "','" + str(value[2]) + "');"
            flag = dbutil.update(sql)
            if not flag:
                break;
        return flag  # 返回输入的

    # 绘制事件
    def paintEvent(self, event):
        super(MyLabel, self).paintEvent(event)
        painter = QPainter(self)
        painter.setPen(QPen(Qt.red, 4, Qt.SolidLine))
        painter.setFont(QFont('Decorative', 20))
        rect_temp = QRect(self.x0, self.y0, abs(self.x1 - self.x0), abs(self.y1 - self.y0))
        # rect_temp = QRect(699,1156,1314-699,1216-1156)
        painter.drawRect(rect_temp)

        for key, value in dict(self.rects).items():
            print("key", key, "value", value)
            # painter.drawRect(QRect(rectangle))
            # painter.drawText(QRect(rectangle).x() + 20, QRect(rectangle).y() + 50, str(self.rect.index(rectangle) + 1))
            painter.drawRect(QRect(value[1][0], value[1][1], value[1][2], value[1][3]))
            painter.drawText(QRect(value[1][0], value[1][1], value[1][2], value[1][3]).x() + 20,
                             QRect(value[1][0], value[1][1], value[1][2], value[1][3]).y() + 50, key)
