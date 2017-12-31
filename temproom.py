# -*- coding=utf-8 -*-


"""
file: main.py
"""
from PyQt5.QtWidgets import (QApplication, QComboBox, QDialog,
        QCheckBox, QGridLayout, QGroupBox, QHBoxLayout,
        QLabel, QMenu, QMenuBar, QPushButton,QVBoxLayout, QDesktopWidget,QMessageBox)
from PyQt5 import QtCore,QtGui
import sys,time
from PyQt5.QtCore import Qt
import send,record,play,threading
import DataBaseRelated
import qdarkstyle
from Visualization import Visualization
from Visualization import Visualization
from mysignal import Signal
from pydub import AudioSegment
import winsound
import wave
import os

class Dialog(QDialog):
    number=0
    roomnumber=0
    userlist=[]
    user=[]
    username=''
    closesignal=0
    font = QtGui.QFont("Arial", 12, QtGui.QFont.Bold)
    flag_voicechange=0;
    flag_denoise=0;
    def __init__(self,username,roomnumber):
        super(Dialog, self).__init__()
        self.setWindowIcon(QtGui.QIcon('1.png'))
        self.l1 = QLabel('当前用户：')
        self.l2 = QLabel('房间号：')
        self.l3 = QLabel(str(username))
        self.l4 = QLabel(str(roomnumber))
        self.b1 = QPushButton('连接服务器')
        self.b2 = QPushButton('下线')
        self.cb1 = QCheckBox("清脆")
        self.cb2 = QCheckBox("低沉")
        self.cb3 = QCheckBox("降噪")
        self.t1 = QPushButton("麦克风测试")
        #self.cb1= QCheckBox("HHH")

        self.setFont(self.font)
        self.l1.setFont(self.font)
        self.l2.setFont(self.font)
        self.b1.setFont(self.font)
        self.b2.setFont(self.font)
        self.cb1.setFont(self.font)
        self.cb2.setFont(self.font)
        self.cb3.setFont(self.font)
        self.t1.setFont(self.font)

        self.b1.clicked.connect(self.connect)
        self.b2.clicked.connect(self.close)
        self.t1.clicked.connect(self.test)
        self.cb1.stateChanged.connect(self.changecb1)
        self.cb2.stateChanged.connect(self.changecb2)
        self.cb3.stateChanged.connect(self.changecb3)
        self.username=username
        self.roomnumber=roomnumber
        # 调整显示内容
        cur, conn = DataBaseRelated.ini()
        self.number = DataBaseRelated.curretroomusernumber(roomnumber,cur)
        result = DataBaseRelated.curretroomusers(roomnumber, cur)

        for i in range(10):
            self.user.append(QLabel(''))


        for i in range(self.number):
            self.userlist.append(result[i][2])
            self.user[i].setText(str(self.userlist[i]))
        conn.close()



        self.formGroupBox = QGroupBox("本房间内用户")
        layout = QVBoxLayout()
        for i in range(10):
            layout.addWidget(self.user[i])
        layout.addStretch()
        self.formGroupBox.setLayout(layout)

        v_box = QVBoxLayout()  # 垂直布局

        layout = QGridLayout()  # 总体表格布局

        h_box1 = QHBoxLayout()
        h_box2 = QHBoxLayout()

        h_box1.addWidget(self.l1)
        h_box1.addWidget(self.l3)
        v_box.addLayout(h_box1)

        h_box2.addWidget(self.l2)
        h_box2.addWidget(self.l4)
        v_box.addLayout(h_box2)

        layout.addLayout(v_box,0,0,1,1)
        layout.addWidget(self.formGroupBox,2,0,5,3)
        layout.addWidget(self.b1,7,0,1,1)
        layout.addWidget(self.b2,7,1,1,1)
        layout.addWidget(self.t1,7,2,1,1)
        layout.addWidget(self.cb1,8,0,1,1)
        layout.addWidget(self.cb2,8,1,1,1)
        layout.addWidget(self.cb3,8,2,1,1)


        self.setLayout(layout)
        self.setWindowTitle('Temproom')
        self.setStyleSheet(qdarkstyle.load_stylesheet_pyqt5())
        self.resize(250,600)
        self.center()

        try:
            self.t=threading.Thread(target=self.refresh)
            self.t.start()
        except:

            a = QMessageBox(self)
            a.setFont(self.font)
            a.setText("程序异常，请退出")
            a.setWindowModality(QtCore.Qt.WindowModal)

            a.setIcon(QMessageBox.NoIcon)
            a.setDefaultButton(QMessageBox.Yes)


            if a.exec() == 1024:
                self.close()
   
    def test(self):
        v = Visualization()
        
        
    def changecb1(self):
        if self.cb2.isChecked():
            self.cb2.setCheckState(Qt.Unchecked)
        if self.cb1.isChecked():
            self.flag_voicechange=1
        else:
            self.flag_voicechange=0

    def changecb2(self):
        if self.cb1.isChecked():
            self.cb1.setCheckState(Qt.Unchecked)
        if self.cb2.isChecked():
            self.flag_voicechange=2
        else:
            self.flag_voicechange=0

    def changecb3(self):
        if self.cb3.isChecked():
            self.flag_denoise=1
        else:
            self.flag_denoise=0
        
        
     
    def connect(self):
        try:
            so =send.client_connect()

            t = threading.Thread(target=self.flow, args=[so])
            t.start()

        except:
            a = QMessageBox(self)
            a.setFont(self.font)
            a.setText("程序异常，请退出")
            a.setWindowModality(QtCore.Qt.WindowModal)

            a.setIcon(QMessageBox.NoIcon)
            a.setDefaultButton(QMessageBox.Yes)

            if a.exec() == 1024:
                self.close()



    def closeEvent(self, event):
        a = QMessageBox(self)
        a.setText("您确定要退出吗？")
        a.setFont(self.font)
        a.setWindowModality(QtCore.Qt.WindowModal)
        b = QtGui.QPixmap('2.png')
        a.setIconPixmap(b)
        #a.setIcon(QMessageBox.NoIcon)
        # a.addButton('确定',QMessageBox.AcceptRole)
        # a.addButton('取消',QMessageBox.RejectRole)
        a.setDefaultButton(a.addButton('确定', QMessageBox.AcceptRole))
        a.setEscapeButton(a.addButton('取消', QMessageBox.RejectRole))

        # reply = QMessageBox.question(self, '确认', '您确定要退出吗？',
        #                              QMessageBox.Yes | QMessageBox.No, QMessageBox.No)

        result = a.exec()
        #print(result)
        if result == 0:
            event.accept()
            cur, conn = DataBaseRelated.ini()
            DataBaseRelated.useroffline(self.username, self.roomnumber, cur, conn)
            DataBaseRelated.roomoffline(self.roomnumber, cur, conn)
            conn.close()
            self.closesignal=1
        elif result == 1:
            event.ignore()

        # reply = QMessageBox.question(self, '确认', 'You sure to quit?',
        #                              QMessageBox.Yes | QMessageBox.No, QMessageBox.No)
        #
        # if reply == QMessageBox.Yes:
        #     event.accept()
        #     cur, conn = DataBaseRelated.ini()
        #     DataBaseRelated.useroffline(self.username, self.roomnumber, cur, conn)
        #     DataBaseRelated.roomoffline(self.roomnumber, cur, conn)
        #     conn.close()
        # else:
        #     event.ignore()

    def refresh(self):

        while 1:
            if self.closesignal == 1:
                break
            time.sleep(1)
            #print(self.number)

            cur, conn = DataBaseRelated.ini()
            #print(DataBaseRelated.curretroomusernumber(self.roomnumber, cur))

            if DataBaseRelated.curretroomusernumber(self.roomnumber, cur) != self.number:
                cur2, conn2 = DataBaseRelated.ini()
                self.number = DataBaseRelated.curretroomusernumber(self.roomnumber, cur)
                del self.userlist[:]
                # del self.user[:]

                if self.closesignal == 1:
                    break

                result = DataBaseRelated.curretroomusers(self.roomnumber, cur)
                conn2.close()
                for i in range(10):
                    self.user[i].setText('')


                for i in range(self.number):
                    self.userlist.append(result[i][2])
                    self.user[i].setText(str(self.userlist[i]))

                self.update()

            conn.close()
            if self.closesignal == 1:
                break



    def center(self):
        qr = self.frameGeometry()
        cp = QDesktopWidget().availableGeometry().center()
        qr.moveCenter(cp)
        self.move(qr.topLeft())


    def flow(self,s):
        while 1:
            record.record(self.username)
            receive_video=self.username+'.wav'
            x = Signal(receive_video)
            if flag_denoise==1:#降噪
                noise = Signal1('noise.wav')
                x.noise_removal(noise)
                x.write(self.username+'.wav')
            if flag_voicechange==2:#低沉
                x.changenansheng();
                x.write(self.username+'.wav')
            elif  flag_voicechange==1:#清脆
                x.changetongsheng();
                x.write(self.username+'.wav')
            send.send(s, self.username)
            for i in self.userlist:
                if self.username != i:
                    send.recv(s)
                    t = threading.Thread(target=play.play,args=[i])
                    t.start()
            if self.closesignal==1:
                s.closesocket()
                break



if __name__ == '__main__':
    app = QApplication(sys.argv)

    main = Dialog()


    sys.exit(main.exec_())
