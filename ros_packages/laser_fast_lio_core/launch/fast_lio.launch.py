import os

from launch import LaunchDescription

from launch.actions import DeclareLaunchArgument, IncludeLaunchDescription
from launch.launch_description_sources import PythonLaunchDescriptionSource
from launch.substitutions import LaunchConfiguration, PathJoinSubstitution, PythonExpression

from launch_ros.actions import Node
from launch_ros.substitutions import FindPackageShare

from ament_index_python.packages import get_package_share_directory

def generate_launch_description():
    package_path = get_package_share_directory('laser_fast_lio_core')
    default_config_file_path = os.path.join(package_path, 'params', 'mid360_internal.yaml')

    # Declare arguments
    declared_arguments = []

    declared_arguments.append(
        DeclareLaunchArgument(
            'namespace',
            default_value=os.getenv('UAV_NAME', "uav1"),
            description='Top-level namespace.'))

    declared_arguments.append(
        DeclareLaunchArgument(
            'use_sim_time',
            default_value=PythonExpression(['"', os.getenv('REAL_UAV', "true"), '" == "false"']),
            description='Whether use the simulation time.'))

    declared_arguments.append(
        DeclareLaunchArgument(
            'topic_pcl',
            default_value='',
            description='Pcl Topic.'))

    declared_arguments.append(
        DeclareLaunchArgument(
            'topic_imu',
            default_value='',
            description='IMU Topic.'))

    declared_arguments.append(
        DeclareLaunchArgument(
            'fast_lio_config_file_path',
            default_value=default_config_file_path,
            description='Config file path for fast lio.'))

    # Initialize arguments
    namespace = LaunchConfiguration('namespace')
    use_sim_time = LaunchConfiguration('use_sim_time')
    fast_lio_config_file_path = LaunchConfiguration('fast_lio_config_file_path')
    topic_imu = LaunchConfiguration('topic_imu')
    topic_pcl = LaunchConfiguration('topic_pcl')

    # Launch Fast Lio
    fast_lio_launch = IncludeLaunchDescription(
        PythonLaunchDescriptionSource([
            PathJoinSubstitution([
                FindPackageShare('fast_lio'),
                'launch',
                'mapping.launch.py'
            ])
        ]),
        launch_arguments={
            'use_sim_time': use_sim_time,
            'config_file_path': fast_lio_config_file_path,
            'topic_imu': topic_imu,
            'topic_pcl': topic_pcl,
        }.items()
    )

    return LaunchDescription(declared_arguments + [fast_lio_launch])
