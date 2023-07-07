#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Author   : xianxiafan
# @Date     : 2023/7/7 15:49
# @File     : pyqt5_demo.py
# @Desc     : pyqt5demo
import sys
from MyFirstUI import *


class MyWindow(QtWidgets.QMainWindow, Ui_MainWindow):
    def __init__(self):
        super(MyWindow, self).__init__()
        self.setupUi(self)

    # 定义按钮单击事件
    def onclickA(self):
        print("Hello W")
        self.Label1.setText("Hello world")


if __name__ == '__main__':
    app = QtWidgets.QApplication(sys.argv)
    win = MyWindow()
    win.Btn1.clicked.connect(win.onclickA)  # 设置Btn1点击事件
    win.show()
    sys.exit(app.exec_())
