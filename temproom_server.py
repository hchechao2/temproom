# -*- coding=utf-8 -*-


"""
file: temproom_server.py
"""
import sys
import threading
from PyQt5.QtWidgets import (QLabel, QCheckBox, QPushButton, QVBoxLayout,QHBoxLayout,
 QApplication, QWidget,QLineEdit,QMessageBox,QDesktopWidget,QFormLayout)
from PyQt5.QtCore import QCoreApplication
from ip import getip
import DataBaseRelated
import recv

class Window(QWidget):

    def __init__(self):
        super().__init__()

        self.init_ui()

    def init_ui(self):
        self.l1 = QLabel('房间数')
        self.l2 = QLabel('总在线人数')
        self.b=QPushButton('刷新')




        self.l3 = QLabel('')
        self.l4 = QLabel('')
        self.refresh()
        self.l5 = QLabel('本机公网ip')
        self.l6 = QLabel(getip())
        # self.b1 = QPushButton('下线')

        # layout=QFormLayout()
        # layout.addRow(self.l1,self.l3)
        # layout.addRow(self.l2,self.l4)
        v_box = QVBoxLayout()
        h_box1 = QHBoxLayout()
        h_box2 = QHBoxLayout()
        h_box3 = QHBoxLayout()

        h_box1.addWidget(self.l1)
        h_box1.addWidget(self.l3)
        h_box1.addStretch()
        v_box.addLayout(h_box1)

        h_box2.addWidget(self.l2)
        h_box2.addWidget(self.l4)
        h_box2.addStretch()
        v_box.addLayout(h_box2)
        
        h_box3.addWidget(self.l5)
        h_box3.addWidget(self.l6)
        h_box3.addStretch()
        v_box.addLayout(h_box3)

        v_box.addWidget(self.b)
        self.setLayout(v_box)
        self.setWindowTitle('Temproom Server')

        self.b.clicked.connect(self.refresh)

        self.resize(250,150)
        self.center()
        self.show()


    def refresh(self):
        cur, conn = DataBaseRelated.ini()
        status1 = DataBaseRelated.numberofrooms(cur)
        status2 = DataBaseRelated.numberofusers(cur)
        self.l3.setText(str(status1))
        self.l4.setText(str(status2))
        numberlist = DataBaseRelated.return_roomnumberlist(cur)
        conn.close()
        for i in numberlist:
            number, c = recv.ready(i)
            if number >= 3:
                t = threading.Thread(target=recv.work, args=c)
                t.start()



    def center(self):

        qr = self.frameGeometry()
        cp = QDesktopWidget().availableGeometry().center()
        qr.moveCenter(cp)
        self.move(qr.topLeft())

  #   def btn1_clk(self):
        
  #       reply = QMessageBox.question(self, 'Message',
		# "Are you sure to quit?", QMessageBox.Yes | 
		# QMessageBox.No, QMessageBox.No)

  #       if reply == QMessageBox.Yes:
  #           event.accept()
  #       else:
  #           event.ignore()       


if __name__=='__main__':
    app = QApplication(sys.argv)
    a_window = Window()
    sys.exit(app.exec_())