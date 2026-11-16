# Практическая работа №3 — модели роботов в ROS 2 Jazzy

Архив содержит исходный пакет `my_robot_model`, отчёт `REPORT_RU.md` и результаты проверок `VALIDATION.txt`. Основная модель: мобильная платформа, два ведущих колеса, пассивная шаровая опора, двухзвенный манипулятор и корпус датчика STL.

## Сборка и запуск (Ubuntu 24.04, ROS 2 Jazzy)

Предполагается установленный ROS 2 Jazzy. Скопируйте папку `my_robot_model` из архива в `~/ros2_ws/src/`.

```bash
sudo apt update
sudo apt install python3-colcon-common-extensions ros-jazzy-xacro ros-jazzy-robot-state-publisher ros-jazzy-joint-state-publisher ros-jazzy-joint-state-publisher-gui ros-jazzy-rviz2 liburdfdom-tools
source /opt/ros/jazzy/setup.bash
cd ~/ros2_ws
colcon build --symlink-install --packages-select my_robot_model
source install/setup.bash
ros2 launch my_robot_model robot.launch.py
```

Откроются RViz и окно управления четырьмя подвижными суставами. В RViz модель подписана на `/robot_description`, фиксированная система — `base_link`. Сетка связана с `base_footprint` и находится на уровне земли. Отображение TF можно включить в панели Displays.

Начальная модель без руки:

```bash
ros2 launch my_robot_model robot.launch.py urdf_model:="$(ros2 pkg prefix --share my_robot_model)/urdf/my_first_model.urdf"
```

Без GUI состояний суставов: `ros2 launch my_robot_model robot.launch.py gui:=false`.
Без RViz: `ros2 launch my_robot_model robot.launch.py rviz:=false`.

Нативная проверка в установленной ROS-среде:

```bash
check_urdf ~/ros2_ws/src/my_robot_model/urdf/my_first_model.urdf
xacro ~/ros2_ws/src/my_robot_model/urdf/diff_robot_model.urdf.xacro > /tmp/lab3_robot.urdf
check_urdf /tmp/lab3_robot.urdf
```

Проверка автономным скриптом (Python с модулями `xacro`, `urdf_parser_py`, `yaml`):

```bash
python3 my_robot_model/scripts/validate.py
```

## Состав

- `urdf/my_first_model.urdf`: начальная URDF-модель платформы.
- `urdf/diff_robot_model.urdf.xacro`: основной параметризованный робот с рукой.
- `urdf/diff_robot_model.urdf`: эквивалентная развёрнутая модель без макросов.
- `urdf/materials.xacro`, `wheel.xacro`, `arm.xacro`: цвета и макросы.
- `meshes/sensor.stl`: оригинальная сетка корпуса датчика, без внешних ресурсов.
- `launch/robot.launch.py`: запуск издателей и RViz с аргументами.
- `config/rviz.rviz`: готовая конфигурация визуализации.
- `setup.py`, `setup.cfg`, `package.xml`, `resource/`, `my_robot_model/`: пакет ament_python.
- `scripts/run.sh`: сборка и запуск из пакета, размещённого в `<workspace>/src`.
- `scripts/validate.py`: воспроизводимые проверки структуры и геометрии.

## Границы проверки

XACRO действительно развёрнут и разобран URDF-парсером. Выполнены проверки структуры, осей, размеров, ограничений, зазоров, STL и синтаксиса Python/YAML/XML. Здесь отсутствует ROS 2, поэтому `colcon build`, нативный `check_urdf`, запуск ROS-узлов и RViz фактически не выполнялись. Скриншоты RViz не создавались и не подменялись иллюстрациями. Модель предназначена для кинематической визуализации; физическая симуляция, управление приводами и навигация не входят в данную работу.

Формат загрузки конкретного учебного сайта не был предоставлен. Архив является комплектом исходников и отчёта, а не подтверждением приёма системой. Персональные ФИО/номер группы не выдуманы; `Student` и `student@example.com` в метаданных пакета — нейтральные технические значения.
