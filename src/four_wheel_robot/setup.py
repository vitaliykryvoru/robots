from setuptools import find_packages, setup

package_name = 'four_wheel_robot'

setup(
    name=package_name,
    version='0.0.0',
    packages=find_packages(exclude=['test']),
    data_files=[

        ('share/ament_index/resource_index/packages',

        ['resource/four_wheel_robot']),


        ('share/four_wheel_robot',

        ['package.xml']),


        ('share/four_wheel_robot/launch',

        ['launch/rsp.launch.py']),


        ('share/four_wheel_robot/urdf',
        [
            'urdf/robot.urdf.xacro',
            'urdf/inertial_macros.xacro'
        ])

    ],
    
    install_requires=['setuptools'],
    zip_safe=True,
    maintainer='vitalii',
    maintainer_email='vitaliykryvoru@gmail.com',
    description='TODO: Package description',
    license='TODO: License declaration',
    extras_require={
        'test': [
            'pytest',
        ],
    },
    entry_points={
        'console_scripts': [
        ],
    },
)
