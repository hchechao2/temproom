# -*- coding=utf-8 -*-


"""
file: temproom_server.py
"""
import threading
import DataBase_server
import recv
import sys

closesignal=0
class MyThread(threading.Thread):

    def __init__(self,func,args=()):
        super(MyThread,self).__init__()
        self.func = func
        self.args = args

    def run(self):
        self.result = self.func(*self.args)

    def get_result(self):
        try:
            return self.result  # 如果子线程不使用join方法，此处可能会报没有self.result的错误
        except:
            return 'null'


def check():
    total=[]
    cur,conn=DataBase_server.ini()
    numberlist=DataBase_server.return_roomnumberlist(cur)
    amountlist=DataBase_server.return_useramountlist(cur)
    conn.close()
    for i in range(len(amountlist)):
        if amountlist[i] >=2:
            cur, conn = DataBase_server.ini()
            users=DataBase_server.curretroomusers(numberlist[i],cur)
            total.append((users,numberlist[i]))
            conn.close()
    return total

def trans1(client):#接受音频文件
    return recv.recv(client)


def trans2(k,client,t):#转发音频文件
    for j in t:
        # if j.get_result()==0:#如果没接收到文件，程序退出
        #     global closesignal
        #     closesignal = 1
        #     sys.exit(-1)

        if j!=t[k]:
            while 1:
                if not j.isAlive():#接受进程结束后转发
                    break
            recv.send(client,j.get_result())



def trans3():
    t1=[]
    t2=[]
    while 1:#检测符合条件的客户端
        total=check()
        print(total)
        if len(total):
            break

    # for i in total:
    i=total[0]#测试第一组
    amount=len(i[0])#组内客户端数量
    print(amount)
    clients=recv.server_connect(amount)#建立socket
    while 1:
        for j in range(amount):
            if closesignal==1:
                sys.exit(-1)
            th=MyThread(func=trans1,args=[clients[j][0]])#创建接受子线程

            if len(t1)<j+1:#如果是第一次转发
                t1.append(th)
            else:#如果不是第一次转发
                t1[j]=th
            t1[j].start()

        for k in range(amount):
            if closesignal == 1:
                sys.exit(-1)
            th2=threading.Thread(target=trans2,args=(k,clients[k][0],t1))#创建转发子线程

            if len(t2)<k+1:#同上
                t2.append(th2)
            else:
                t2[k]=th2
            t2[k].start()
            t2[k].join()

if __name__=='__main__':
    trans3()



#print(clients[0][1])

#username=recv.recv(clients[0][0])
#print('用户为'+username)
#recv.send(clients[0][0],username)
#clients[0][0].close()
