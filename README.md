# Four-Wheel Mobile Robot — ROS 2 Jazzy

Навчальний проєкт зі створення власної чотириколісної мобільної платформи за допомогою **ROS 2 Jazzy, URDF та Xacro**.

На поточному етапі проєкт містить:
- основний корпус робота (`base_link`);
- чотири колеса;
- обертові з'єднання (`continuous joints`);
- геометрію Visual та Collision;
- інерційні параметри;
- Xacro-макрос для повторного використання опису колеса;
- запуск моделі через `robot_state_publisher`;
- візуалізацію моделі в RViz2.

> **Поточний стан:** створена базова геометрична модель чотириколісного робота. Керування моторами, одометрія, Gazebo та Nav2 поки не налаштовані.

---

# 1. Вимоги

Для роботи використовується:

| Компонент | Версія |
|---|---|
| Ubuntu | 24.04 |
| ROS 2 | Jazzy |
| Build system | ament_cmake |
| Robot description | URDF / Xacro |
| Visualization | RViz2 |

Переконайся, що ROS 2 Jazzy встановлений.

Перевір:

```bash
echo $ROS_DISTRO
```

Очікуваний результат:

```text
jazzy
```

Якщо змінна порожня, підключи ROS 2:

```bash
source /opt/ros/jazzy/setup.bash
```

---

# 2. Встановлення необхідних пакетів

Встанови залежності:

```bash
sudo apt update

sudo apt install \
  ros-jazzy-xacro \
  ros-jazzy-robot-state-publisher \
  ros-jazzy-joint-state-publisher-gui \
  ros-jazzy-rviz2 \
  python3-colcon-common-extensions \
  python3-rosdep \
  libxml2-utils
```

Ці пакети використовуються для:

| Пакет | Призначення |
|---|---|
| xacro | Перетворення Xacro у URDF |
| robot_state_publisher | Публікація TF для моделі робота |
| joint_state_publisher_gui | Графічне керування станами joint |
| rviz2 | Візуалізація робота |
| colcon | Збірка ROS 2 пакетів |
| rosdep | Встановлення залежностей |
| libxml2-utils | Перевірка XML-файлів |

---

# 3. Створення робочої області ROS 2

Створюємо робочу область:

```bash
mkdir -p ~/robot_ws/src
```

Переходимо до неї:

```bash
cd ~/robot_ws
```

Підключаємо ROS 2:

```bash
source /opt/ros/jazzy/setup.bash
```

---

# 4. Створення ROS 2 пакета

Переходимо в каталог `src`:

```bash
cd ~/robot_ws/src
```

Створюємо пакет:

```bash
ros2 pkg create my_robot_description \
  --build-type ament_cmake
```

Переходимо до пакета:

```bash
cd my_robot_description
```

Створюємо необхідні каталоги:

```bash
mkdir urdf launch meshes rviz
```

Структура проєкту:

```text
robot_ws/
└── src/
    └── my_robot_description/
        ├── urdf/
        │   └── my_robot.urdf.xacro
        ├── launch/
        │   └── display.launch.py
        ├── meshes/
        ├── rviz/
        ├── CMakeLists.txt
        ├── package.xml
        └── README.md
```

---

# 5. Налаштування package.xml

Відкриваємо файл:

```bash
nano package.xml
```

Повністю замінюємо його вміст:

```xml
<?xml version="1.0"?>
<?xml-model href="http://download.ros.org/schema/package_format3.xsd" schematypens="http://www.w3.org/2001/XMLSchema"?>

<package format="3">
  <name>my_robot_description</name>
  <version>0.0.0</version>
  <description>Four-wheel mobile robot description package</description>

  <maintainer email="your_email@example.com">your_name</maintainer>
  <license>Apache-2.0</license>

  <buildtool_depend>ament_cmake</buildtool_depend>

  <!-- Runtime dependencies -->
  <exec_depend>xacro</exec_depend>
  <exec_depend>robot_state_publisher</exec_depend>
  <exec_depend>joint_state_publisher_gui</exec_depend>
  <exec_depend>rviz2</exec_depend>

  <!-- Testing dependencies -->
  <test_depend>ament_lint_auto</test_depend>
  <test_depend>ament_lint_common</test_depend>

  <export>
    <build_type>ament_cmake</build_type>
  </export>
</package>
```

Заміни `your_email@example.com` та `your_name` на свої дані.

### Важливо

Ми використовуємо `<exec_depend>`, оскільки ці пакети потрібні під час виконання та запуску моделі.

Не потрібно додавати `joint_state_publisher_gui` через `find_package()` у `CMakeLists.txt`: ми запускаємо його як ROS 2 вузол через Python launch-файл.

Перевір XML:

```bash
xmllint --noout package.xml
```

Якщо команда нічого не вивела — XML синтаксично правильний.

---

# 6. Налаштування CMakeLists.txt

Відкриваємо:

```bash
nano CMakeLists.txt
```

Повністю замінюємо вміст:

```cmake
cmake_minimum_required(VERSION 3.8)
project(my_robot_description)

find_package(ament_cmake REQUIRED)

install(
  DIRECTORY
    urdf
    launch
    meshes
    rviz
  DESTINATION share/${PROJECT_NAME}
)

ament_package()
```

### Пояснення

`find_package(ament_cmake REQUIRED)` підключає систему збірки ROS 2.

`install()` копіює каталоги моделі та launch-файли до встановленого пакета.

`ament_package()` завершує конфігурацію пакета.

Для нашого пакета опису робота цього достатньо. Ми не компілюємо власні C++ вузли.

---

# 7. Створення URDF/Xacro моделі

Відкриваємо файл:

```bash
nano urdf/my_robot.urdf.xacro
```

Вставляємо повний код:

```xml
<?xml version="1.0"?>

<robot name="my_robot"
       xmlns:xacro="http://www.ros.org/wiki/xacro">

  <!-- ================================= -->
  <!-- 1. ROBOT PARAMETERS               -->
  <!-- ================================= -->

  <xacro:property name="chassis_length" value="0.40"/>
  <xacro:property name="chassis_width" value="0.30"/>
  <xacro:property name="chassis_height" value="0.08"/>

  <xacro:property name="wheel_radius" value="0.05"/>
  <xacro:property name="wheel_width" value="0.03"/>

  <xacro:property name="wheel_x" value="0.13"/>
  <xacro:property name="wheel_y" value="0.17"/>


  <!-- ================================= -->
  <!-- 2. MAIN CHASSIS                   -->
  <!-- ================================= -->

  <link name="base_link">

    <visual>
      <origin xyz="0 0 0" rpy="0 0 0"/>

      <geometry>
        <box size="${chassis_length}
                   ${chassis_width}
                   ${chassis_height}"/>
      </geometry>

      <material name="blue">
        <color rgba="0.1 0.3 0.8 1"/>
      </material>
    </visual>

    <collision>
      <origin xyz="0 0 0" rpy="0 0 0"/>

      <geometry>
        <box size="${chassis_length}
                   ${chassis_width}
                   ${chassis_height}"/>
      </geometry>
    </collision>

    <inertial>
      <origin xyz="0 0 0" rpy="0 0 0"/>

      <mass value="5.0"/>

      <inertia
        ixx="0.05" ixy="0" ixz="0"
        iyy="0.08" iyz="0"
        izz="0.10"/>
    </inertial>

  </link>


  <!-- ================================= -->
  <!-- 3. WHEEL MACRO                    -->
  <!-- ================================= -->

  <xacro:macro name="wheel" params="name x y">

    <link name="${name}_wheel_link">

      <visual>
        <origin
          xyz="0 0 0"
          rpy="1.5708 0 0"/>

        <geometry>
          <cylinder
            radius="${wheel_radius}"
            length="${wheel_width}"/>
        </geometry>

        <material name="black">
          <color rgba="0.05 0.05 0.05 1"/>
        </material>
      </visual>

      <collision>
        <origin
          xyz="0 0 0"
          rpy="1.5708 0 0"/>

        <geometry>
          <cylinder
            radius="${wheel_radius}"
            length="${wheel_width}"/>
        </geometry>
      </collision>

      <inertial>
        <origin xyz="0 0 0" rpy="0 0 0"/>

        <mass value="0.5"/>

        <inertia
          ixx="0.001" ixy="0" ixz="0"
          iyy="0.001" iyz="0"
          izz="0.001"/>
      </inertial>

    </link>


    <!-- Wheel joint -->

    <joint name="${name}_wheel_joint"
           type="continuous">

      <parent link="base_link"/>
      <child link="${name}_wheel_link"/>

      <origin
        xyz="${x} ${y} ${-chassis_height/2 - wheel_radius}"
        rpy="0 0 0"/>

      <axis xyz="0 1 0"/>

    </joint>

  </xacro:macro>


  <!-- ================================= -->
  <!-- 4. CREATE FOUR WHEELS             -->
  <!-- ================================= -->

  <!-- Front left wheel -->

  <xacro:wheel
    name="front_left"
    x="${wheel_x}"
    y="${wheel_y}"/>


  <!-- Front right wheel -->

  <xacro:wheel
    name="front_right"
    x="${wheel_x}"
    y="${-wheel_y}"/>


  <!-- Rear left wheel -->

  <xacro:wheel
    name="rear_left"
    x="${-wheel_x}"
    y="${wheel_y}"/>


  <!-- Rear right wheel -->

  <xacro:wheel
    name="rear_right"
    x="${-wheel_x}"
    y="${-wheel_y}"/>

</robot>
```

---

# 8. Геометрія робота

Поточні параметри моделі:

| Параметр | Значення |
|---|---:|
| Довжина корпусу | 0.40 м |
| Ширина корпусу | 0.30 м |
| Висота корпусу | 0.08 м |
| Радіус колеса | 0.05 м |
| Ширина колеса | 0.03 м |
| X коліс | ±0.13 м |
| Y коліс | ±0.17 м |
| Маса корпусу | 5.0 кг |
| Маса одного колеса | 0.5 кг |

Система координат ROS:

- X — вперед;
- Y — вліво;
- Z — вгору.

Розташування коліс:

| Колесо | X | Y |
|---|---:|---:|
| Front Left | +0.13 | +0.17 |
| Front Right | +0.13 | -0.17 |
| Rear Left | -0.13 | +0.17 |
| Rear Right | -0.13 | -0.17 |

Координата Z для центрів коліс визначається формулою:

```xml
${-chassis_height/2 - wheel_radius}
```

Центр корпусу `base_link` знаходиться в його геометричному центрі.

### Важливо про поточну конструкцію

Усі чотири колеса мають `continuous joint`. На цьому етапі це лише геометрична модель з обертовими з'єднаннями.

Модель поки не розрізняє ведучі та пасивні колеса і не має контролера руху.

Інерційні параметри є приблизними навчальними значеннями. Для фізично коректної симуляції їх потрібно буде розрахувати окремо.

---

# 9. Створення launch-файлу

Створюємо:

```bash
nano launch/display.launch.py
```

Вставляємо:

```python
import os

from launch import LaunchDescription
from launch_ros.actions import Node
from launch.substitutions import Command
from launch_ros.parameter_descriptions import ParameterValue
from ament_index_python.packages import get_package_share_directory


def generate_launch_description():

    pkg_path = get_package_share_directory(
        'my_robot_description'
    )

    xacro_file = os.path.join(
        pkg_path,
        'urdf',
        'my_robot.urdf.xacro'
    )

    robot_description = ParameterValue(
        Command(['xacro ', xacro_file]),
        value_type=str
    )

    return LaunchDescription([

        # Publishes robot description and TF

        Node(
            package='robot_state_publisher',
            executable='robot_state_publisher',
            parameters=[{
                'robot_description': robot_description
            }]
        ),

        # GUI for joint states

        Node(
            package='joint_state_publisher_gui',
            executable='joint_state_publisher_gui'
        ),

        # RViz2 visualization

        Node(
            package='rviz2',
            executable='rviz2'
        )

    ])
```

### Призначення вузлів

| Вузол | Призначення |
|---|---|
| robot_state_publisher | Публікує TF та опис робота |
| joint_state_publisher_gui | Дозволяє змінювати кути joint |
| rviz2 | Відображає модель |

---

# 10. Перевірка Xacro

Повертаємося до робочої області:

```bash
cd ~/robot_ws
```

Підключаємо ROS 2:

```bash
source /opt/ros/jazzy/setup.bash
```

Перетворюємо Xacro у звичайний URDF:

```bash
ros2 run xacro xacro \
  src/my_robot_description/urdf/my_robot.urdf.xacro \
  -o /tmp/my_robot.urdf
```

Якщо помилок немає, перевіряємо URDF:

```bash
check_urdf /tmp/my_robot.urdf
```

Якщо `check_urdf` не знайдено:

```bash
sudo apt install liburdfdom-tools
```

Перевірка XML:

```bash
xmllint --noout /tmp/my_robot.urdf
```

---

# 11. Встановлення залежностей через rosdep

Виконай:

```bash
cd ~/robot_ws

source /opt/ros/jazzy/setup.bash

rosdep install \
  --from-paths src \
  --ignore-src \
  -r -y
```

`rosdep` перевіряє залежності пакетів і встановлює відсутні системні пакети.

Повідомлення `DeprecationWarning` від Python `pkg_resources` саме по собі не означає помилку встановлення.

---

# 12. Збірка проєкту

Перед збіркою переконайся, що `CMakeLists.txt` містить тільки:

```cmake
cmake_minimum_required(VERSION 3.8)
project(my_robot_description)

find_package(ament_cmake REQUIRED)

install(
  DIRECTORY
    urdf
    launch
    meshes
    rviz
  DESTINATION share/${PROJECT_NAME}
)

ament_package()
```

Не додавай:

```cmake
find_package(joint_state_publisher_gui REQUIRED)
```

Це було причиною першої помилки збірки.

Тепер виконай:

```bash
cd ~/robot_ws

source /opt/ros/jazzy/setup.bash

colcon build --symlink-install
```

Після успішної збірки:

```bash
source install/setup.bash
```

Очікуваний результат:

```text
Starting >>> my_robot_description
Finished <<< my_robot_description

Summary: 1 package finished
```

Якщо потрібно повністю очистити результати попередньої збірки:

```bash
cd ~/robot_ws

rm -rf build install log

source /opt/ros/jazzy/setup.bash

colcon build --symlink-install
```

---

# 13. Запуск робота у RViz2

Виконуємо:

```bash
cd ~/robot_ws

source /opt/ros/jazzy/setup.bash
source install/setup.bash

ros2 launch my_robot_description display.launch.py
```

Має відкритися RViz2 та графічний інтерфейс `joint_state_publisher_gui`.

## Налаштування RViz2

У лівій панелі RViz2:

1. Знайди поле `Fixed Frame`.
2. Встанови значення `base_link`.
3. Натисни `Add`.
4. Додай `RobotModel`.
5. Переконайся, що модель відображається.

Якщо модель не відображається, перевір:

- чи працює `robot_state_publisher`;
- чи існує параметр `robot_description`;
- чи публікуються `/joint_states` та `/tf`;
- чи немає помилок Xacro.

---

# 14. Перевірка ROS 2 вузлів і топіків

Поки модель запущена, відкрий інший термінал:

```bash
source /opt/ros/jazzy/setup.bash
source ~/robot_ws/install/setup.bash
```

Перевір вузли:

```bash
ros2 node list
```

Очікуються вузли:

```text
/joint_state_publisher
/joint_state_publisher_gui
/robot_state_publisher
```

Назви можуть трохи відрізнятися залежно від версії та конфігурації вузлів.

Перевір топіки:

```bash
ros2 topic list
```

Перевір стани з'єднань:

```bash
ros2 topic echo /joint_states
```

Перевір TF:

```bash
ros2 topic echo /tf
```

---

# 15. Поточна структура проєкту

```text
robot_ws/
└── src/
    └── my_robot_description/
        ├── urdf/
        │   └── my_robot.urdf.xacro
        │
        ├── launch/
        │   └── display.launch.py
        │
        ├── meshes/
        │
        ├── rviz/
        │
        ├── CMakeLists.txt
        ├── package.xml
        └── README.md
```

---

# 16. Типові помилки

## Помилка 1: CMake не знаходить joint_state_publisher_gui

Повідомлення:

```text
Could not find a package configuration file provided by
"joint_state_publisher_gui"
```

Причина: `joint_state_publisher_gui` помилково доданий через `find_package()`.

Рішення: видалити цей рядок із `CMakeLists.txt`.

Правильний CMake:

```cmake
find_package(ament_cmake REQUIRED)
```

## Помилка 2: Invalid XML у package.xml

Повідомлення:

```text
The manifest contains invalid XML:
not well-formed (invalid token)
```

Причина: зайві символи, помилки форматування або некоректне кодування XML.

Рішення:

```bash
xmllint --noout package.xml
```

Перший рядок повинен бути:

```xml
<?xml version="1.0"?>
```

Не повинно бути зворотних слешів перед XML-тегами.

## Помилка 3: Xacro не знаходить файл

Перевір шлях:

```bash
ls ~/robot_ws/src/my_robot_description/urdf/
```

Має бути:

```text
my_robot.urdf.xacro
```

## Помилка 4: Пакет не знаходиться після збірки

Виконай:

```bash
source /opt/ros/jazzy/setup.bash
source ~/robot_ws/install/setup.bash
```

---

# 17. Наступні етапи розвитку проєкту

Після завершення поточного етапу планується поступове розширення робота.

| Етап | Завдання |
|---|---|
| 1 | Базова геометрія URDF — виконано |
| 2 | Правильне дерево TF |
| 3 | Додавання `base_footprint` |
| 4 | Додавання LiDAR |
| 5 | Додавання IMU |
| 6 | Додавання камер |
| 7 | Налаштування `ros2_control` |
| 8 | Налаштування контролера коліс |
| 9 | Одометрія |
| 10 | Gazebo simulation |
| 11 | SLAM |
| 12 | Nav2 |

У перспективі архітектуру можна розвивати за прикладом ROSMASTER X3 від Automatic Addison, використовуючи окремі пакети для опису робота, керування, симуляції, локалізації та навігації.

---

# 18. Основні команди для щоденної роботи

Підключити ROS 2:

```bash
source /opt/ros/jazzy/setup.bash
```

Перейти в робочу область:

```bash
cd ~/robot_ws
```

Зібрати проєкт:

```bash
colcon build --symlink-install
```

Підключити зібраний workspace:

```bash
source install/setup.bash
```

Перевірити Xacro:

```bash
ros2 run xacro xacro \
  src/my_robot_description/urdf/my_robot.urdf.xacro \
  -o /tmp/my_robot.urdf
```

Перевірити URDF:

```bash
check_urdf /tmp/my_robot.urdf
```

Запустити RViz2:

```bash
ros2 launch my_robot_description display.launch.py
```

---

**Кінець поточного етапу:** створено ROS 2 пакет `my_robot_description`, описано чотириколісну базу за допомогою Xacro та підготовлено запуск моделі у RViz2.
