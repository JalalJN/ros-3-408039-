"""Display the model; start exactly one joint-state publisher."""
import os
from ament_index_python.packages import get_package_share_directory
from launch import LaunchDescription
from launch.actions import DeclareLaunchArgument
from launch.conditions import IfCondition, UnlessCondition
from launch.substitutions import LaunchConfiguration
from launch_ros.actions import Node
from launch_ros.parameter_descriptions import ParameterValue
from launch.actions import OpaqueFunction
import xacro


def start_nodes(context):
    model = LaunchConfiguration('urdf_model').perform(context)
    description = xacro.process_file(model).toxml()
    return [Node(package='robot_state_publisher', executable='robot_state_publisher',
                 output='screen', parameters=[{'robot_description': ParameterValue(description, value_type=str)}])]


def generate_launch_description():
    share = get_package_share_directory('my_robot_model')
    gui = LaunchConfiguration('gui')
    return LaunchDescription([
        DeclareLaunchArgument('urdf_model', default_value=os.path.join(share, 'urdf', 'diff_robot_model.urdf.xacro')),
        DeclareLaunchArgument('gui', default_value='true', choices=['true', 'false']),
        DeclareLaunchArgument('rviz', default_value='true', choices=['true', 'false']),
        OpaqueFunction(function=start_nodes),
        Node(package='joint_state_publisher_gui', executable='joint_state_publisher_gui',
             condition=IfCondition(gui), output='screen'),
        Node(package='joint_state_publisher', executable='joint_state_publisher',
             condition=UnlessCondition(gui), output='screen'),
        Node(package='rviz2', executable='rviz2', condition=IfCondition(LaunchConfiguration('rviz')),
             arguments=['-d', os.path.join(share, 'config', 'rviz.rviz')], output='screen'),
    ])
