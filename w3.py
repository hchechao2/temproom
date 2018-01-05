import sys,threading
from PyQt5.QtWidgets import (QLabel, QCheckBox, QPushButton, QVBoxLayout,QHBoxLayout, QApplication,
    QWidget,QLineEdit,QMessageBox,QDesktopWidget,QFormLayout)
import qdarkstyle
from PyQt5 import QtCore,QtGui
import DataBaseRelated

def check_contain_chinese(check_str):
    for ch in check_str:
        if u'\u4e00' <= ch <= u'\u9fff':
            return True
    return False

class LoginWindow(QWidget):
    font = QtGui.QFont("Times", 12, QtGui.QFont.Bold)
    def __init__(self):
        super().__init__()
        self.setWindowIcon(QtGui.QIcon('1.png'))
        self.init_ui()

    def init_ui(self):
        self.l1 = QLabel('用户名')
        self.l2 = QLabel('密码')
        self.l3 = QLabel('说明：不可包含中文，且应大于4位')
        self.le1 = QLineEdit()
        self.le2 = QLineEdit()
        self.le2.setEchoMode(QLineEdit.Password)
        self.b = QPushButton('注册')

        self.setFont(self.font)
        self.l1.setFont(self.font)
        self.l2.setFont(self.font)
        self.l3.setFont(self.font)
        self.b.setFont(self.font)

        layout=QFormLayout()
        layout.setSpacing(15)
        layout.addRow(self.l1,self.le1)
        layout.addRow(self.l2,self.le2)
        layout.addRow(self.l3)

        v_box = QVBoxLayout()
        h_box = QHBoxLayout()

        h_box.addWidget(self.b)

        v_box.addLayout(layout)
        v_box.addLayout(h_box)

        self.setLayout(v_box)
        self.setWindowTitle('用户注册')
        self.setStyleSheet(qdarkstyle.load_stylesheet_pyqt5())

        self.b.clicked.connect(self.btn2_clk)

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
        username = str(self.le1.text())
        password = str(self.le2.text())
        
        if check_contain_chinese(username) or check_contain_chinese(password):
            a = QMessageBox(self)
            a.setFont(self.font)
            a.setText("用户名和密码不可包含中文！")
            a.setWindowModality(QtCore.Qt.WindowModal)

            a.setIcon(QMessageBox.NoIcon)
            a.setDefaultButton(QMessageBox.Yes)
            
            if a.exec() == 1024:
                return 0
            
        if len(username)<4 or len(password)<4:
            a = QMessageBox(self)
            a.setFont(self.font)
            a.setText("用户名和密码须大于四位")
            a.setWindowModality(QtCore.Qt.WindowModal)

            a.setIcon(QMessageBox.NoIcon)
            a.setDefaultButton(QMessageBox.Yes)

            if a.exec() == 1024:
                self.le1.clear()
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

                if a.exec() == 1024:
                    return 0

            if not DataBaseRelated.search_username(username,cur):
                DataBaseRelated.signup(username,password,cur,conn)
                a = QMessageBox(self)
                a.setText("注册成功~")
                a.setFont(self.font)
                a.setWindowModality(QtCore.Qt.WindowModal)

                a.setIcon(QMessageBox.NoIcon)
                a.setDefaultButton(QMessageBox.Yes)

                if a.exec() == 1024:
                    self.le1.clear()
                    self.le2.clear()
                    self.hide()

            else:
                a = QMessageBox(self)
                a.setText("这个用户名被别人用了，换一个吧")
                a.setFont(self.font)
                a.setWindowModality(QtCore.Qt.WindowModal)

                a.setIcon(QMessageBox.NoIcon)
                a.setDefaultButton(QMessageBox.Yes)

                if a.exec() == 1024:
                    self.le1.clear()
                    self.le2.clear()

            conn.close()


if __name__=='__main__':
    app = QApplication(sys.argv)
    app.setWindowIcon(QtGui.QIcon('1.png'))
    a_window = LoginWindow()
    sys.exit(app.exec_())
