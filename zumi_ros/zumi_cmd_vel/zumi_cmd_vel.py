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
import json

from geometry_msgs.msg import Twist
from rclpy.node import Node
from rclpy.qos import QoSProfile
from rclpy.qos import qos_profile_sensor_data 
from sensor_msgs.msg import LaserScan , Image , CameraInfo , CompressedImage
from rclpy.context import Context
import rclpy
from socket import *
import time

from geometry_msgs.msg import Twist

class ZumiCmdVel(Node):

    def __init__(self):
        super().__init__('zumi_cmd_vel_publish')
        qos = QoSProfile(depth=10)

        # Initialise subscribers
        self.cmd_vel_sub = self.create_subscription(
            Twist,
            'cmd_vel',
            self.cmd_vel_callback,
            qos)        

        """************************************************************
        ** Initialise timers
        ************************************************************"""
        self.update_timer = self.create_timer(
            0.010,  # unit: s
            self.update_callback)

        self.get_logger().info("Zumin on ")


        # Set the socket parameters
        HOST=''
        PORT = 10000
        buf = 1024
        ADDR = (HOST, PORT)

        # Create socket and bind to address
        self.serverSocket = socket(AF_INET, SOCK_STREAM)
        self.serverSocket.bind(ADDR)
        print('bind')

        # 연결 수신 대기 상태
        self.serverSocket.listen(100)
        print('listen')

        # 연결 수락
        self.clientSocekt, addr_info = self.serverSocket.accept()
        print('accept')
        print('--client information--')
        print(self.clientSocekt,)

        rclpy.get_default_context().on_shutdown(self.fnShutDown)
        print('close')        

    """*******************************************************************************
    ** Callback functions and relevant functions
    *******************************************************************************"""
    def controlMotor(self, wheel_radius, wheel_separation , lin_vel, ang_vel ):
        wheel_vel_left  = lin_vel - (ang_vel * wheel_separation / 2);
        wheel_vel_right  = lin_vel + (ang_vel * wheel_separation / 2);
        print('l_speed {0} r_speed {1}'.format(wheel_vel_left,wheel_vel_right))
        wheel_vel_left_tmp = int(wheel_vel_left*400)  
        wheel_vel_right_tmp = int(wheel_vel_right*400) 
        return wheel_vel_left_tmp,wheel_vel_right_tmp

    def cmd_vel_callback(self, msg):
        print('cmd_vel_callback')
        WHEEL_RADIUS =  0.015 #1.5 cm
        WHEEL_SEPARATION =  0.062 #6.2 cm
        l_speed, r_speed = self.controlMotor(WHEEL_RADIUS, WHEEL_SEPARATION, msg.linear.x, msg.angular.z )
        data=str(l_speed)+','+str(r_speed)
        self.clientSocekt.send(data.encode())       

    def update_callback(self):
        pass

    def fnShutDown(self):
        self.get_logger().info("shutdown !!!!!!!!!!!!!!!!!!!!!!!!!!!!!! ")
        self.clientSocekt.close()
        self.serverSocket.close()

