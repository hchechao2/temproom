# -*- coding=utf-8 -*-


"""
file: main.py
"""
from PyQt5.QtWidgets import (QApplication, QComboBox, QDialog,
        QDialogButtonBox, QFormLayout, QGridLayout, QGroupBox, QHBoxLayout,
        QLabel, QLineEdit, QMenu, QMenuBar, QPushButton,QVBoxLayout, QDesktopWidget)
 
import sys,socket,ip
import send,record,play,threading
import DataBaseRelated

class Dialog(QDialog):
    number=0
    userlist=[]
    user=[]
    username=''
    def __init__(self,username,roomnumber):
        super(Dialog, self).__init__()
        
        self.l1 = QLabel('当前用户：')
        self.l2 = QLabel('房间号：')
        self.l3 = QLabel(str(username))
        self.l4 = QLabel(str(roomnumber))
        self.b1 = QPushButton('上线')
        self.b2 = QPushButton('下线')
        self.b1.clicked.connect(self.connect)

        # self.b2.clicked.connect(self.b2_click(username,roomnumber))
        self.username=username
        # 调整显示内容
        cur, conn = DataBaseRelated.ini()
        self.number = DataBaseRelated.curretroomusernumber(roomnumber,cur)
        for i in range(self.number):
            result=DataBaseRelated.curretroomusers(roomnumber,cur)
            self.userlist.append(result[i][2])
            self.use = QLabel(str(self.userlist[i]))
            self.user.append(self.use)
        conn.close()







        self.formGroupBox = QGroupBox("本房间内用户")
        layout = QVBoxLayout()
        for i in range(self.number):
            layout.addWidget(self.user[i])
        layout.addStretch()
        self.formGroupBox.setLayout(layout)




        #
        # self.createFormGroupBox()

        v_box = QVBoxLayout()
        

        layout = QGridLayout()  
        # layout.addWidget(self.l1,0,0) 
        # layout.addWidget(self.l3,0,1) 
        # layout.addWidget(self.l2,1,0) 
        # layout.addWidget(self.l4,1,1)


        h_box1 = QHBoxLayout()
        h_box2 = QHBoxLayout()

        h_box1.addWidget(self.l1)
        h_box1.addWidget(self.l3)
        v_box.addLayout(h_box1)

        h_box2.addWidget(self.l2)
        h_box2.addWidget(self.l4)
        v_box.addLayout(h_box2)

        layout.addLayout(v_box,0,0,1,1)
        # self.formGroupBox = QGroupBox("房间内用户")
        layout.addWidget(self.formGroupBox,2,0,5,2)
        layout.addWidget(self.b1,7,1,1,1)
        layout.addWidget(self.b2, 8, 1, 1, 1)
        # layout.addWidget(self.user,2,0,0,2)

        self.setLayout(layout)
        self.setWindowTitle('Temproom')
        self.resize(250,600)
        self.center()

        # self.b1.clicked.connect(self.btn1_clk)
        # self.b2.clicked.connect(self.btn2_clk)

        self.hide()

    def connect(self):
        so = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        so.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        so.bind((ip.getip(), 6666))
        so.listen(1000)
        conn, addr = so.accept()
        t = threading.Thread(target=self.flow,args=conn)
        t.start()

    def center(self):
        qr = self.frameGeometry()
        cp = QDesktopWidget().availableGeometry().center()
        qr.moveCenter(cp)
        self.move(qr.topLeft())

    def b2_click(self,username, roomnumber):
        cur, conn = DataBaseRelated.ini()
        DataBaseRelated.useroffline(username, roomnumber, cur, conn)
        DataBaseRelated.roomoffline(roomnumber, cur, conn)
        conn.close()
    # def btn1_clk(self):
    #         pass
    #
    # def btn2_clk(self):
    #         pass


    #
    # def createFormGroupBox(self,):

    def flow(self,conn):
        # s = send.client_connect()
        # while 1:
        #     record.record(self.username)
        #     send.send(s, self.username)
        #     for i in self.userlist:
        #         if self.username != i:
        #             send.recv(s)
        #             t = threading.Thread(target=play.play,args=i)
        #             t.start()

        while 1:
            record.record(self.username)
            send.send(conn, self.username)
            opp = send.recv(conn)
            play(opp)


if __name__ == '__main__':
    app = QApplication(sys.argv)

    main = Dialog()


    sys.exit(main.exec_())