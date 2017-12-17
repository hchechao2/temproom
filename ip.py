#!/usr/bin/python  
#coding=utf-8  
import socket  
import urllib.request
  
def getip():  
    url="http://ifconfig.me/ip"
    req = urllib.request.Request(url, headers={'User-Agent' : "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_12_6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/62.0.3202.94 Safari/537.36"}) 
    con = urllib.request.urlopen(req)
    return(bytes.decode(con.read()).strip('\n') )
  
  
if __name__ == '__main__':  
    print(getip())