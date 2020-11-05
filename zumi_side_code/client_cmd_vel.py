#! /usr/bin/python
# -*- coding: utf-8 -*-
import time

from socket import *
from select import *
import sys
from time import ctime
import json
from zumi.zumi import Zumi

HOST = '192.168.0.5'
PORT = 10000
BUFSIZE = 1024
ADDR = (HOST,PORT)

clientSocket = socket(AF_INET, SOCK_STREAM)#  ^d^|  ^d ^w^p   ^q ^f^m ^u^x     ^|^d ^u^|  ^f^l  ^s ^}^d  ^c^} ^d $
clientSocket.connect(ADDR)#  ^d^|  ^d ^w^p   ^q ^f^m ^}^d  ^k^| ^o^d ^u^| ^k .

zumi = Zumi()

while True :
    data = clientSocket.recv(BUFSIZE)
    print(data.decode())
    tmp_str2 = data.decode().split(",")
    if len(tmp_str2) != 2:
        print("this is no data")
        continue 
    l_speed = int(tmp_str2[0])
    r_speed = int(tmp_str2[1])
    print('l_speed {0} r_speed {1}'.format(l_speed,r_speed))

    #-126 and 127 range 
    zumi.control_motors(l_speed, r_speed)

print('connect is success')

