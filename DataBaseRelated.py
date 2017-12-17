# -*- coding: utf-8 -*-
"""
Created on Sat Dec  2 18:41:35 2017

@author: Lenovo
"""

import pymysql
import random


def ini():
    conn=pymysql.connect(host='120.79.72.9',user='root',passwd='123',db='temproom',unix_socket="/var/run/mysqld/mysqld.sock")
    cur = conn.cursor()
    return cur,conn


def search_username(username,cur):
        # username = input('请输入用户名:')
        # if len(username)>30:
        #     print('用户名过长，请重新输入！')
        #     continue
        sql = "select * from Users where username = '" + username + "'"
        cur.execute(sql)
        return cur.rowcount




def signin(username,password,cur):
    if search_username(username,cur)==1:
        # data = pd.DataFrame(list(cur.fetchall()))
        # cursor_des = pd.DataFrame(list(cur.description))
        # data.columns = list(cursor_des[0])
        results = cur.fetchall()
        # print(results[0])
        if password == results[0][1]:
            return 0
        else:
            return 1
    else:
        return 2


def signup(username,password,cur,conn):
    # while(1):
    #     password = input('请输入密码(区分大小写)：')
    #     if len(password)>30:
    #         print('密码过长，请重新输入！')
    #         continue
    #     break
    # sex = input('请勾选性别：')
    #
    # while(1):
    #     nickname = input('请输入昵称：')
    #     if len(password)>30:
    #         print('昵称过长，请重新输入！')
    #         continue
    #     break

    # today = datetime.datetime.now().strftime("%Y-%m-%d")
    sql = """insert into Users
	values('%s','%s',%d)"""
    cur.execute(sql % (username,password,0))
    conn.commit()



#%%判断创建新房间还是进入已有房间
#创建房间
# while(1):
#     roomnumber = str(random.randint(1000, 9999))

def search_room(roomnumber,cur):
    sql = "select * from Rooms where roomnumber = '%d'"
    cur.execute(sql% roomnumber)
    return cur.rowcount

def return_roomnumberlist(cur):
    sql = "select * from Rooms "
    cur.execute(sql)
    results = cur.fetchall()
    numberlist=[]
    for i in range(cur.rowcount):
        numberlist.append(results[i][0])

    return numberlist



def numberofrooms(cur):
    sql = "select * from Rooms "
    cur.execute(sql)
    return cur.rowcount

def numberofusers(cur):
    sql = "select * from Rooms "
    cur.execute(sql)
    results = cur.fetchall()
    total=0
    for i in range(cur.rowcount):
        total+=results[i][2]
    return total

def newroom(roomnumber,keyintoroom,roomowner,cur,conn):
    sql = """insert into Rooms
	values(%d,%d,%d)"""
    cur.execute(sql % (int(roomnumber),keyintoroom,1))
    conn.commit()

    sql = """update Users
	set currentroom = %d
	where username='%s'"""
    cur.execute(sql % (int(roomnumber),roomowner))
    conn.commit()


    # s = "insert into " + table_name;
    # sql = "" + s + "(id,fid,content)values(null,'" + f_id
    # + "','" + new_content + "')"



    sql="create table if not exists room%s" %str(roomnumber)+ """(
    id  int(1)  auto_increment PRIMARY key,
    status  int  not null,
    username  VARCHAR(30))"""
    cur.execute(sql)
    conn.commit()

    sql ="insert into room%s"%str(roomnumber)+"(status,username) values(%d,'%s')"
    cur.execute(sql % (1,roomowner))
    conn.commit()

def curretroomusers(roomnumber,cur):
    sql = "select * from room%s" % str(roomnumber)
    cur.execute(sql)

    results = cur.fetchall()

    return results

def curretroomusernumber(roomnumber,cur):
    sql = "select * from Rooms where roomnumber = '%d'"
    cur.execute(sql% roomnumber)
    results=cur.fetchall()
    return results[0][2]


def getinroom(username,roomnumber,keyintoroom,cur,conn):
    # sql = "select * from rooms where roomnumber =' " + roomnumber+"'"
    # cur.execute(sql)
    if search_room(roomnumber,cur)==1:
        results=cur.fetchall()

        if keyintoroom== results[0][1]:
            sql = """update Rooms
	        set numberofusers = numberofusers+1
	        where roomnumber = %d"""
            cur.execute(sql % (int(roomnumber)))
            conn.commit()

            sql = """update Users
	        set currentroom = %d
	        where username='%s'"""
            cur.execute(sql % (int(roomnumber),username))
            conn.commit()

            sql = "insert into room%s" % str(roomnumber)+"(status,username) values(%d,'%s')"
            cur.execute(sql % (1, username))
            conn.commit()

            return 0
        else:
            return 1
    else:
        return 2

def useroffline(username,roomnumber, cur, conn):
    if search_room(roomnumber,cur)==1:
        results=cur.fetchall()
        if results[0][2]>0:
            sql = """update Rooms
	        set numberofusers = numberofusers-1
	        where roomnumber = %d"""
            cur.execute(sql % (int(roomnumber)))
            conn.commit()
        else:
            sql = """update Rooms
            set numberofusers = 0
            where roomnumber = %d"""
            cur.execute(sql % (int(roomnumber)))
            conn.commit()


        sql = """update Users
        set currentroom = %d
        where username='%s'"""
        cur.execute(sql % (0, username))
        conn.commit()

        sql = "delete from room%s" % str(roomnumber) + " where username='%s' "%username
        # '" + username + "'"
        #print(sql)
        cur.execute(sql)
        conn.commit()



def roomoffline(roomnumber,cur,conn):
    if search_room(roomnumber,cur)==1:
        results=cur.fetchall()
        if results[0][2]==0:
            sql = """delete from Rooms
            where roomnumber=%d"""
            cur.execute(sql%(int(roomnumber)))
            conn.commit()

            sql = "drop table room%s"% str(roomnumber)
            #print(sql)
            cur.execute(sql)
            conn.commit()
        else:
            pass

    else:
        pass
        # sql = "drop table room%s" % str(roomnumber)
        # print(sql)
        # # cur.execute(sql)
        # conn.commit()
        # print('wrong')

if __name__=='__main__':
    cur,conn=ini()
    #signup('anyone4','anyone4',cur,conn)
    #print(signin('hechao','123',cur))
    #newroom(16,2,'hechao',cur,conn)
    #print(search_room(121,cur))
    #getinroom('anyone4',15,2,cur,conn)
    useroffline('anyone',1333,cur,conn)
    #roomoffline(16,cur,conn)
    #search_room(15,cur)
    conn.close()
