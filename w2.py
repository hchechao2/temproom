# -*- coding=utf-8 -*-


"""
file: w2.py
"""
import sys
from PyQt5.QtWidgets import (QLabel, QCheckBox, QPushButton, QVBoxLayout,QHBoxLayout,
 QApplication, QWidget,QLineEdit,QMessageBox,QDesktopWidget,QFormLayout)
import DataBaseRelated
import temproom

class Window(QWidget):
    currentuser=''

    def __init__(self,username):
        super().__init__()

        self.init_ui(username)

    def init_ui(self,username):
        self.l1 = QLabel('房间号')
        self.l2 = QLabel('密钥')
        self.le1 = QLineEdit()
        self.le2 = QLineEdit()
        self.b1 = QPushButton('进入房间')
        self.b2 = QPushButton('创建新房间')

        layout=QFormLayout()
        layout.addRow(self.l1,self.le1)
        layout.addRow(self.l2,self.le2)
        v_box = QVBoxLayout()

        h_box = QHBoxLayout()
        # h_box2 = QHBoxLayout()

        # h_box1.addWidget(self.l1)
        # h_box1.addWidget(self.le1)
        # v_box.addLayout(h_box1)


        h_box.addStretch()
        h_box.addWidget(self.b1)
        h_box.addWidget(self.b2)
        # v_box.addLayout(h_box2)

        v_box.addLayout(layout)
        v_box.addLayout(h_box)
        self.setLayout(v_box)
        # self.setLayout(v_box)
        self.currentuser=username
        self.setWindowTitle('Temproom-欢迎您,'+self.currentuser)

        self.b1.clicked.connect(self.btn1_clk)
        self.b2.clicked.connect(self.btn2_clk)

        self.resize(250,120)
        self.center()
        self.show()

    def center(self):

        qr = self.frameGeometry()
        cp = QDesktopWidget().availableGeometry().center()
        qr.moveCenter(cp)
        self.move(qr.topLeft())

    def btn1_clk(self):
        roomnumber = int(self.le1.text())
        keyintoroom = int(self.le2.text())
        cur, conn = DataBaseRelated.ini()
        if DataBaseRelated.getinroom(self.currentuser, roomnumber, keyintoroom, cur, conn)==0:
            self.hide()
            self.window3 = temproom.Dialog(self.currentuser,roomnumber)
            self.window3.show()

        elif DataBaseRelated.getinroom(self.currentuser, roomnumber, keyintoroom, cur, conn)==1:
            buttonReply = QMessageBox.question(self, 'temproom', "房间密钥错误，请核对后输入", QMessageBox.Yes)
            if buttonReply == QMessageBox.Yes:
                self.show()

        elif DataBaseRelated.getinroom(self.currentuser, roomnumber, keyintoroom, cur, conn) ==2:
            buttonReply = QMessageBox.question(self, 'temproom', "不存在此房间，请新建", QMessageBox.Yes)
            if buttonReply == QMessageBox.Yes:
                self.show()

        conn.close()
    def btn2_clk(self):
        roomnumber = int(self.le1.text())
        keyintoroom = int(self.le2.text())
        cur, conn = DataBaseRelated.ini()

        if not DataBaseRelated.search_room(roomnumber,cur):
            DataBaseRelated.newroom(roomnumber,keyintoroom,self.currentuser,cur,conn)
            self.hide()
            self.window3 = temproom.Dialog(self.currentuser, roomnumber)
            self.window3.show()

        else:
            buttonReply = QMessageBox.question(self, 'temproom', "房间已被占用，请重新建立", QMessageBox.Yes)
            if buttonReply == QMessageBox.Yes:
                self.show()



        conn.close()
if __name__=='__main__':
    app = QApplication(sys.argv)
    a_window = Window()
    sys.exit(app.exec_())