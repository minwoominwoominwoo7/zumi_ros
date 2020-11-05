import glob
import os

from setuptools import find_packages
from setuptools import setup

package_name = 'zumi_ros'

setup(
    name=package_name,
    version='2.0.1',
    packages=find_packages(),
    data_files=[
        ('share/ament_index/resource_index/packages', ['resource/' + package_name]),
        ('share/' + package_name, ['package.xml']),
        # To be added
        # ('share/' + package_name + '/launch', glob.glob(os.path.join('launch', 'turtlebot3_interactive_marker.launch.py'))),
        # ('share/' + package_name + '/launch', glob.glob(os.path.join('launch', 'turtlebot3_obstacle_detection.launch.py'))),
        # ('share/' + package_name + '/rviz', glob.glob(os.path.join('rviz', 'turtlebot3_interactive_marker.rviz'))),
    ],
    install_requires=['setuptools','launch'],
    zip_safe=True,
    author=['test'],
    author_email=['test@test.com'],
    maintainer='test',
    maintainer_email='test@test.com',
    keywords=['ROS', 'ROS2', 'zumi', 'rclpy'],
    classifiers=[
        'Intended Audience :: Developers',
        'License :: OSI Approved :: Apache Software License',
        'Programming Language :: Python',
        'Topic :: Software Development',
    ],
    description=(
        'Zumi Ros node'
    ),
    license='Apache License, Version 2.0',
    entry_points={
        'console_scripts': [
            # To be added
            # 'turtlebot3_interactive_marker = turtlebot3_example.turtlebot3_interactive_marker.main:main', 
            'zumi_camera = zumi_ros.zumi_camera.main:main',
            'zumi_cmd_vel = zumi_ros.zumi_cmd_vel.main:main',
        ],
    },
)
