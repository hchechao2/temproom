# -*- coding: utf-8 -*-
"""
Created on Sat Dec 30 15:21:17 2017

@author: Lenovo
"""

import sys
from PyQt5.QtWidgets import (QLabel, QCheckBox, QPushButton, QVBoxLayout,QHBoxLayout,
 QApplication, QWidget,QLineEdit,QMessageBox,QDesktopWidget,QFormLayout)
import DataBaseRelated
from PyQt5 import QtCore,QtGui
import qdarkstyle
import temproom
import random

class CreateWindow(QWidget):
    currentuser=''
    font = QtGui.QFont("Times", 12, QtGui.QFont.Bold)
    def __init__(self,username):
        super().__init__()
        self.setWindowIcon(QtGui.QIcon('1.png'))
        self.init_ui(username)

    def init_ui(self,username):
        self.l1 = QLabel('房间号')
        self.l2 = QLabel('密钥')
        
        roomnumber = random.randint(1000, 9999)
        try:
            cur, conn = DataBaseRelated.ini()
        except:
            a = QMessageBox(self)
            a.setFont(self.font)
            a.setText("请检查网络连接")
            a.setWindowModality(QtCore.Qt.WindowModal)
            a.setIcon(QMessageBox.NoIcon)
            a.setDefaultButton(QMessageBox.Yes)
            if a.exec() == 1024:
                return 0
        while DataBaseRelated.search_room(roomnumber,cur):
            roomnumber = str(random.randint(1000, 9999))
        conn.close()
            
        self.le1 = QLabel(str(roomnumber))
        self.le2 = QLineEdit()
        self.le2.setEchoMode(QLineEdit.Password)
        self.b2 = QPushButton('创建新房间')

        self.setFont(self.font)
        self.l1.setFont(self.font)
        self.l2.setFont(self.font)
        self.b2.setFont(self.font)


        layout=QFormLayout()
        layout.setSpacing(15)
        layout.addRow(self.l1,self.le1)
        layout.addRow(self.l2,self.le2)
        v_box = QVBoxLayout()

        h_box = QHBoxLayout()
        # h_box2 = QHBoxLayout()

        # h_box1.addWidget(self.l1)
        # h_box1.addWidget(self.le1)
        # v_box.addLayout(h_box1)


        # h_box.addStretch()
        h_box.addWidget(self.b2)
        # v_box.addLayout(h_box2)

        v_box.addLayout(layout)
        v_box.addLayout(h_box)
        self.setLayout(v_box)
        # self.setLayout(v_box)
        self.currentuser=username
        self.setWindowTitle('创建新房间,'+self.currentuser)
        self.setStyleSheet(qdarkstyle.load_stylesheet_pyqt5())

        self.b2.clicked.connect(self.btn2_clk)

        self.resize(250,150)
        self.center()
        self.show()

    def center(self):

        qr = self.frameGeometry()
        cp = QDesktopWidget().availableGeometry().center()
        qr.moveCenter(cp)
        self.move(qr.topLeft())


    def closeEvent(self, event):
        self.hide()

    def btn2_clk(self):
        roomnumber = str(self.le1.text())
        keyintoroom = str(self.le2.text())

        if keyintoroom.isdigit()==False:
            a = QMessageBox(self)
            a.setText("密匙应当为4位数字！")
            a.setFont(self.font)
            a.setWindowModality(QtCore.Qt.WindowModal)

            a.setIcon(QMessageBox.NoIcon)
            a.setDefaultButton(QMessageBox.Yes)

            if a.exec() == 1024:
                self.le2.clear()

        elif len(keyintoroom) != 4:
            a = QMessageBox(self)
            a.setText("密匙应当为4位数字！")
            a.setFont(self.font)
            a.setWindowModality(QtCore.Qt.WindowModal)

            a.setIcon(QMessageBox.NoIcon)
            a.setDefaultButton(QMessageBox.Yes)

            if a.exec() == 1024:
                self.le2.clear()
                
        else:
            try:
                cur, conn = DataBaseRelated.ini()
            except:
                a = QMessageBox(self)
                a.setFont(self.font)
                a.setText("请检查网络连接")
                a.setWindowModality(QtCore.Qt.WindowModal)

                a.setIcon(QMessageBox.NoIcon)
                a.setDefaultButton(QMessageBox.Yes)

                # buttonReply = a.(self, 'temproom', "您已经在线了，请勿重复登录", QMessageBox.Yes)

                if a.exec() == 1024:
                    return 0
            # cur, conn = DataBaseRelated.ini()
            roomnumber = int(self.le1.text())
            keyintoroom = int(self.le2.text())
            if not DataBaseRelated.search_room(roomnumber,cur):
                DataBaseRelated.newroom(roomnumber,keyintoroom,self.currentuser,cur,conn)
                a = QMessageBox(self)
                a.setText("注册成功!请牢记密码:"+str(keyintoroom))
                a.setFont(self.font)
                a.setWindowModality(QtCore.Qt.WindowModal)

                a.setIcon(QMessageBox.NoIcon)
                a.setDefaultButton(QMessageBox.Yes)

                if a.exec() == 1024:
                    self.le2.clear()
                    self.hide()
                DataBaseRelated.useroffline(self.currentuser, roomnumber, cur, conn)
                self.hide()
            else:
                a = QMessageBox(self)
                a.setText("这个房间被别人用啦!")
                a.setFont(self.font)
                a.setWindowModality(QtCore.Qt.WindowModal)

                a.setIcon(QMessageBox.NoIcon)
                a.setDefaultButton(QMessageBox.Yes)

                if a.exec() == 1024:
                    self.le2.clear()

            conn.close()

if __name__=='__main__':
    app = QApplication(sys.argv)
    a_window = CreateWindow()
    sys.exit(app.exec_())
