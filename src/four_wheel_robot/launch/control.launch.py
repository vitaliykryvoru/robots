"""

control.launch.py



Призначення:

Запустити:


controller_manager


joint_state_broadcaster


diff_drive_controller




Потік:


cmd_vel

↓

diff_drive_controller

↓

ros2_control

↓

wheel joints

↓

Gazebo




Саме цей launch

робить робота

керованим.



Без нього:


teleop працює

але робот не рухається.


"""

