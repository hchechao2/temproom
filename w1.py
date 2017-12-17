# -*- coding=utf-8 -*-


"""
file: w1.py
"""
import sys
from PyQt5.QtWidgets import (QLabel, QCheckBox, QPushButton, QVBoxLayout,QHBoxLayout, QApplication, 
    QWidget,QLineEdit,QMessageBox,QDesktopWidget,QFormLayout)
import DataBaseRelated,w2


class Window(QWidget):

    def __init__(self):
        super().__init__()

        self.init_ui()

    def init_ui(self):
        self.l1 = QLabel('用户名')
        self.l2 = QLabel('密码')
        self.le1 = QLineEdit()
        self.le2 = QLineEdit()
        self.b1 = QPushButton('登录')
        self.b2 = QPushButton('注册')
        #self.setGeometry(200,200,200,200)
        layout=QFormLayout()
        layout.addRow(self.l1,self.le1)
        layout.addRow(self.l2,self.le2)
        
        v_box = QVBoxLayout()
        h_box = QHBoxLayout()

        h_box.addWidget(self.b1)
        h_box.addWidget(self.b2)

        v_box.addLayout(layout)
        v_box.addLayout(h_box)

        self.setLayout(v_box)
        self.setWindowTitle('用户登录')

        self.b1.clicked.connect(self.btn1_clk)
        self.b2.clicked.connect(self.btn2_clk)

        self.resize(250,150)
        self.center()
        self.show()

    def center(self):

        qr = self.frameGeometry()
        cp = QDesktopWidget().availableGeometry().center()
        qr.moveCenter(cp)
        self.move(qr.topLeft())

    def btn1_clk(self):
        username=str(self.le1.text())
        password=str(self.le2.text())
        cur,conn=DataBaseRelated.ini()
        if DataBaseRelated.signin(username,password,cur)==0:
                self.hide()
                self.window2=w2.Window(username)
                self.window2.show()

        elif DataBaseRelated.signin(username,password,cur)==1:
            buttonReply = QMessageBox.question(self, 'temproom', "密码错误，请重新登录", QMessageBox.Yes)
            if buttonReply==QMessageBox.Yes:
                self.show()

        elif DataBaseRelated.signin(username,password,cur)==2:
            buttonReply = QMessageBox.question(self, 'temproom', "不存在此用户，请注册", QMessageBox.Yes)
            if buttonReply == QMessageBox.Yes:
                self.show()
        conn.close()

    def btn2_clk(self):
        username = self.le1.text()
        password = self.le2.text()
        cur, conn = DataBaseRelated.ini()
        if not DataBaseRelated.search_username(username,cur):
            DataBaseRelated.signup(username,password,cur,conn)
            buttonReply = QMessageBox.question(self, 'temproom', "注册成功！", QMessageBox.Yes)
            if buttonReply == QMessageBox.Yes:
                self.hide()
                self.window2 = w2.Window(username)
                self.window2.show()

        else:
            buttonReply = QMessageBox.question(self, 'temproom', "用户名已被占用，请重新注册", QMessageBox.Yes)
            if buttonReply == QMessageBox.Yes:
                self.show()
        conn.close()



if __name__=='__main__':
    app = QApplication(sys.argv)
    a_window = Window()
    sys.exit(app.exec_())