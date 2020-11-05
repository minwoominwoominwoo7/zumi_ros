# run command   

## camera node on   

remote pc side ( ros2 foxy )   
ros2 run zumi_ros zumi_camera  
rqt   

zumi side   
python3 client_camera.py

## teleop node on  

remote pc side ( ros2 foxy )  
ros2 run zumi_ros zumi_cmd_vel  
ros2 run turtlebot3_teleop teleop_keyboard  

zumi side   
python3 client_cmd_vel.py  

