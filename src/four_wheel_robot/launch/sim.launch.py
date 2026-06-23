"""

sim.launch.py



Головний launch.



Запускає:



gazebo.launch.py


+


control.launch.py


+


rsp.launch.py





Це головна точка входу.




Запуск:



ros2 launch four_wheel_robot sim.launch.py






Повна архітектура:



Keyboard

↓

teleop

↓

cmd_vel

↓

diff_drive_controller

↓

ros2_control

↓

wheel joints

↓

Gazebo

↓

joint_states

↓

robot_state_publisher

↓

TF

↓

RViz


"""

