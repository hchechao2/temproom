# -*- coding=utf-8 -*-


"""
file: w1.py
"""
import sys,threading
from PyQt5.QtWidgets import (QLabel, QCheckBox, QPushButton, QVBoxLayout,QHBoxLayout, QApplication,
    QWidget,QLineEdit,QMessageBox,QDesktopWidget,QFormLayout)
import qdarkstyle
from PyQt5 import QtCore,QtGui
import DataBaseRelated,w2

def check_contain_chinese(check_str):
    for ch in check_str:
        if u'\u4e00' <= ch <= u'\u9fff':
            return True
    return False

class Window(QWidget):
    font = QtGui.QFont("Times", 12, QtGui.QFont.Bold)
    def __init__(self):
        super().__init__()
        # self.setWindowIcon(QtGui.QIcon('1.png'))
        self.init_ui()

    def init_ui(self):

        self.l1 = QLabel('用户名')
        self.l2 = QLabel('密码')
        self.le1 = QLineEdit()
        self.le2 = QLineEdit()
        self.le2.setEchoMode(QLineEdit.Password)
        self.b1 = QPushButton('登录')
        self.b2 = QPushButton('注册')

        #self.b1.setFont(font1)


        self.setFont(self.font)
        self.l1.setFont(self.font)
        self.l2.setFont(self.font)
        self.b1.setFont(self.font)
        self.b2.setFont(self.font)
        # self.le2.setFont(QtGui.QFont("Times", 6, QtGui.QFont.Bold))

        #self.setGeometry(200,200,200,200)
        layout=QFormLayout()
        layout.setSpacing(15)
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
        self.setStyleSheet(qdarkstyle.load_stylesheet_pyqt5())

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

    def closeEvent(self, event):
        a = QMessageBox(self)
        a.setFont(self.font)
        a.setText("您确定要退出吗？")
        a.setWindowModality(QtCore.Qt.WindowModal)

        # a.setIcon(QMessageBox.NoIcon)
        b=QtGui.QPixmap('2.png')

        a.setIconPixmap(b)
        # a.addButton('确定',QMessageBox.AcceptRole)
        # a.addButton('取消',QMessageBox.RejectRole)
        a.setDefaultButton(a.addButton('确定',QMessageBox.AcceptRole))
        a.setEscapeButton(a.addButton('取消',QMessageBox.RejectRole))

        # reply = QMessageBox.question(self, '确认', '您确定要退出吗？',
        #                              QMessageBox.Yes | QMessageBox.No, QMessageBox.No)




        result=a.exec()
        #print(result)
        if  result== 0:
            event.accept()

        elif result== 1:
            event.ignore()


    def btn1_clk(self):
        username=str(self.le1.text())
        password=str(self.le2.text())
        
        if check_contain_chinese(username) or check_contain_chinese(password):
            a = QMessageBox(self)
            a.setFont(self.font)
            a.setText("用户名和密码不可包含中文！")
            a.setWindowModality(QtCore.Qt.WindowModal)

            a.setIcon(QMessageBox.NoIcon)
            a.setDefaultButton(QMessageBox.Yes)
            
            if a.exec() == 1024:
                return 0
            
        try:
            cur,conn=DataBaseRelated.ini()
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


        response=DataBaseRelated.signin(username,password,cur)
        if response==0:
            if DataBaseRelated.search_userstatus(username,cur)==0:
                self.hide()
                self.window2=w2.Window(username)
                self.window2.show()
                # t=threading.Thread(target=new,args=username)
                # t.start()
            else:
                a=QMessageBox(self)
                a.setFont(self.font)
                a.setText("您已经在线了，请勿重复登录")
                a.setWindowModality(QtCore.Qt.WindowModal)

                a.setIcon(QMessageBox.NoIcon)
                a.setDefaultButton(QMessageBox.Yes)

                if a.exec() == 1024:
                    self.le1.clear()
                    self.le2.clear()

        elif response==1:
            a = QMessageBox(self)
            a.setText("密码错误，请重新登录")
            a.setFont(self.font)
            a.setWindowModality(QtCore.Qt.WindowModal)

            a.setIcon(QMessageBox.NoIcon)
            a.setDefaultButton(QMessageBox.Yes)



            if a.exec() == 1024:
                #self.le1.clear()
                self.le2.clear()
            # buttonReply = QMessageBox.question(self, 'temproom', "密码错误，请重新登录", QMessageBox.Yes)
            # if buttonReply==QMessageBox.Yes:
            #
            #     self.le2.clear()
            #     self.show()

        elif response==2:
            a = QMessageBox(self)
            a.setText("不存在此用户，请注册")
            a.setFont(self.font)
            a.setWindowModality(QtCore.Qt.WindowModal)

            a.setIcon(QMessageBox.NoIcon)
            a.setDefaultButton(QMessageBox.Yes)

            # buttonReply = a.(self, 'temproom', "您已经在线了，请勿重复登录", QMessageBox.Yes)

            if a.exec() == 1024:
                self.le1.clear()
                self.le2.clear()

        conn.close()

    def btn2_clk(self):
        self.window2=w3.LoginWindow()
        self.window2.show()


if __name__=='__main__':
    app = QApplication(sys.argv)
    app.setWindowIcon(QtGui.QIcon('1.png'))
    a_window = Window()
    sys.exit(app.exec_())
