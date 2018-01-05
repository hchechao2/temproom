# -*- coding=utf-8 -*-


"""
file: recv.py
socket service
"""


import socket
import sys
import os
import struct


# def server_ini(client_number):
#     s = []
#     for i in range(client_number):
#         so = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
#         so.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
#         s.append(so)
#     return s


def server_connect(client_number):

    clients = []
    so = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    so.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    try:
        so.bind(('192.168.1.8', 6666))
        so.listen(1)
        so.settimeout(10)
        print('listening')
    except socket.error as msg:
        print(msg)
        sys.exit(1)



    for i in range(client_number):
        print('连接中....')
        conn,addr=so.accept()
        conn.settimeout(5)
        clients.append((conn,addr))
        print("连接成功 "+str(addr))
    return clients
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

        # # 定义定义文件信息。
        # fileinfo_size = os.path.getsize(filepath)
        #
        # info=str(fileinfo_size)+' '+str(username)
        # # 定义文件头信息，包含文件名和文件大小
        # #fhead = struct.pack('128sl', os.path.basename(filepath),os.stat(filepath).st_size)
        # conn.send(info.encode())
        fileinfo_size = os.path.getsize(filepath)
        length = len(username)

        # info = str(fileinfo_size)+' '+str(username)
        # print(info)
        info = struct.pack('ii10s', fileinfo_size, length, bytes(username, 'utf-8'))
        # 定义文件头信息，包含文件名和文件大小
        # fhead = struct.pack('128sl', os.path.basename(filepath),os.stat(filepath).st_size)
        conn.send(info)


        fp = open(filepath, 'rb')
        print('begin to send to'+username)
        while 1:
            data = fp.read(1024)
            if not data:
                print('{0} file send over...'.format(filepath))
                break
            conn.send(data)
    else:
        print('send时本地没有文件')
    # conn.close()





def recv(conn):
    #print ('Accept new connection from {0}'.format(addr))
    #conn.settimeout(500)
    # conn.send(str.encode('Hi, Welcome to the server!'))

#   while 1:
    #fileinfo_size = struct.calcsize('128sl')
    # info = conn.recv(1024).decode()
    # sp=info.find(' ')
    #
    # username = info[sp+1:len(info)]
    # filesize = int(info[0:sp])
    info = conn.recv(18)
    try:
        filesize, length = struct.unpack('ii', info[0:8])
        username = (struct.unpack('{length}s'.format(length=length), info[8:8 + length])[0]).decode()
    except:
        return 0
    if filesize:
        #print ('filesize is {0}'.format(buf))
        recvd_size = 0  # 定义已接收文件的大小
        print(username)
        fp = open(username+'.wav', 'wb')
        print ('start receiving from..'+username)

        while not recvd_size == filesize:
            if filesize - recvd_size > 1024:
                data = conn.recv(1024)
                recvd_size += len(data)
            elif filesize - recvd_size <0:
                return 0
            else:

                data = conn.recv(filesize - recvd_size)
                recvd_size = filesize
            fp.write(data)


        fp.close()
        print ('end receive...')
    return username



# if __name__ == '__main__':
#     #socket_service()
