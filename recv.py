# -*- coding=utf-8 -*-


"""
file: recv.py
socket service
"""


import socket
import time
import sys
import os
from ip import getip
import DataBaseRelated,threading


def server_ini(client_number):
    s = []
    for i in range(client_number):
        so = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        so.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        s.append(so)
    return s


def server_connect(client_number, s):
    conn = []
    addr = []
    for i in range(client_number):
        try:
            s[i].bind((getip(), 6666 + i))
            s[i].listen(100)
        except socket.error as msg:
            print(msg)
            sys.exit(1)

        conn[i], addr[i] = s[i].accept()
        return conn
    #     self._result = result
    #
    # def get_result(self):
    #     return self._result

# def server_connect(client_number,s):
#     conn = []
#     addr = []
#     for i in range(client_number):
#         try:
#             s[i].bind((getip(), 6666+i))
#             s[i].listen(10)
#         except socket.error as msg:
#             print (msg)
#             sys.exit(1)
#
#         conn[i], addr[i] = s[i].accept()
#     return conn
        # t = threading.Thread(target=deal_data, args=conn[i])
        # t.start()

def send(conn,username):
    filepath = username+'.wav'
    if os.path.isfile(filepath):
        # 定义定义文件信息。
        fileinfo_size = os.path.getsize(filepath)

        # 定义文件头信息，包含文件名和文件大小
        # fhead = struct.pack('128sl', os.path.basename(filepath),os.stat(filepath).st_size)
        conn.send(str.encode(str(fileinfo_size)))
        conn.send(str.encode(username))
        fp = open(filepath, 'rb')
        while 1:
            data = fp.read(1024)
            if not data:
                print('{0} file send over...'.format(filepath))
                break
            conn.send(data)
    # conn.close()





def recv(conn):
    #print ('Accept new connection from {0}'.format(addr))
    #conn.settimeout(500)
    # conn.send(str.encode('Hi, Welcome to the server!'))

#   while 1:
    #fileinfo_size = struct.calcsize('128sl')
    buf = bytes.decode(conn.recv(1024))
    username = bytes.decode(conn.recv(1024))
    filesize=int(buf)
    if buf:
        print ('filesize is {0}'.format(buf))
        recvd_size = 0  # 定义已接收文件的大小
        fp = open(username+'.wav', 'wb')
        print ('start receiving...')

        while not recvd_size == filesize:
            if filesize - recvd_size > 1024:
                data = conn.recv(1024)
                recvd_size += len(data)
            else:
                data = conn.recv(filesize - recvd_size)
                recvd_size = filesize
            fp.write(data)
        fp.close()
        print ('end receive...,begin to transmit')
    return username


def ready(roomnumber):
    cur, conn = DataBaseRelated.ini()
    number = DataBaseRelated.curretroomusernumber(roomnumber, cur)
    if number >=2:
        s = server_ini(number)
        c = server_connect(number,s)
        return number ,c
    else:
        return 0,0
    # t = threading.Thread(target=c.server_connect, args=(number, s))
    # t.start()
    # while t.isAlive():
    #     pass
    # conn=c.get_result()
    # for i in conn:
    #     t = threading.Thread(target=recv.recv, args=i)
    #     t.start()
def work(c):
    # for i in c:
    #     t = threading.Thread(target=recv, args=i)
    #     t.start()
    user=[]
    while  1:
        for i in c:
            user.append=recv(i)
            for j in c:
                if j!=i:
                    send(c,user[i])


# if __name__ == '__main__':
#     #socket_service()
