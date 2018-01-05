# -*- coding=utf-8 -*-


"""
file: send.py
socket client
"""

import socket
import os
import sys
import struct



def client_connect():
    try:
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        s.connect(('120.79.72.9', 6666))
    except socket.error as msg:
        print (msg)
        sys.exit(1)
    print('连接服务器成功')
    return s
    #
    # print (bytes.decode(s.recv(1024)))

def send(s,username):
    # while 1:
    filepath = username+'.wav'
    if os.path.isfile(filepath):
        # 定义定义文件信息。
        fileinfo_size = os.path.getsize(filepath)
        length=len(username)
        info=struct.pack('ii10s',fileinfo_size,length,bytes(username,'utf-8'))


        s.send(info)

        print('sending to server')

        fp = open(filepath, 'rb')
        while 1:
            data = fp.read(1024)
            if not data:
                print ('send over...')
                break
            s.send(data)


def recv(s,num):

    info = s.recv(18)
    filesize,length=struct.unpack('ii',info[0:8])
    username = (struct.unpack('{length}s'.format(length=length), info[8:8 + length])[0]).decode()
    # sp=info.find(' ')
    # username = info[sp+1:len(info)]

    if filesize:
        #print('filesize is {0}'.format(buf))
        recvd_size = 0  # 定义已接收文件的大小
        # fp = open(username+'.wav', 'wb')
        fp = open(username+'_'+str(num)+'.wav', 'wb')
        print('start receiving from server')

        while not recvd_size == filesize:
            if filesize - recvd_size > 1024:
                data = s.recv(1024)
                recvd_size += len(data)
            else:
                data = s.recv(filesize - recvd_size)
                recvd_size = filesize
            fp.write(data)
        print('done，接受到'+username)
        fp.close()

