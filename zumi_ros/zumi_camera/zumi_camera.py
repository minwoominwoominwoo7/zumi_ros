#!/usr/bin/env python3
#
# Copyright 2019 ROBOTIS CO., LTD.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
#
# Authors: Ryan Shim, Gilbert

import numpy

from geometry_msgs.msg import Twist
from rclpy.node import Node
from rclpy.qos import QoSProfile
from rclpy.qos import qos_profile_sensor_data 
from sensor_msgs.msg import LaserScan , Image , CameraInfo , CompressedImage

import socket
import cv2
import numpy as np
from cv_bridge import CvBridge

class ZumiCamera(Node):

    def __init__(self):
        super().__init__('zumi_camera_publish')

        """************************************************************
        ** Initialise ROS publishers and subscribers
        ************************************************************"""
        qos = QoSProfile(depth=10)
        self.img_pub = self.create_publisher(Image, '/raw_data', qos)

        self.get_logger().info("Zumin on ")

        HOST=''
        PORT=8485
        
        #TCP 사용
        s=socket.socket(socket.AF_INET,socket.SOCK_STREAM)
        print('Socket created')
        
        #서버의 아이피와 포트번호 지정
        s.bind((HOST,PORT))
        print('Socket bind complete')
        # 클라이언트의 접속을 기다린다. (클라이언트 연결을 10개까지 받는다)
        s.listen(10)
        print('Socket now listening')
        
        #연결, conn에는 소켓 객체, addr은 소켓에 바인드 된 주소
        conn,addr=s.accept()
        self.cvBridge = CvBridge()        

        while True:
            length = self.recvall(conn, 16)
            stringData = self.recvall(conn, int(length))
            data = np.fromstring(stringData, dtype = 'uint8')
            
            image_np = cv2.imdecode(data, cv2.IMREAD_COLOR)
            image_np_180 = cv2.rotate(image_np, cv2.ROTATE_180)
            #cv2.imshow('ImageWindow',image_np_180)
            cv2.waitKey(1)

            #### Create CompressedIamge ####
            msg = CompressedImage()
            #msg.header.stamp = rospy.Time.now()
            msg.format = "jpeg"
            msg.data = np.array(cv2.imencode('.jpg', image_np)[1]).tostring()
            # Publish new image  
            self.img_pub.publish(self.cvBridge.cv2_to_imgmsg(image_np_180, "bgr8"))

    def recvall(self, sock, count):
        # 바이트 문자열
        buf = b''
        while count:
            newbuf = sock.recv(count)
            if not newbuf: return None
            buf += newbuf
            count -= len(newbuf)
        return buf        


