from launch import LaunchDescription
from launch_ros.actions import Node


def generate_launch_description():
    return LaunchDescription([

        Node(
            package='hangman_game',
            executable='word_service',
            name='word_service',
            output='screen'
        ),

        Node(
            package='hangman_game',
            executable='progress_action_server',
            name='action_server',
            output='screen'
        ),

        # Node(
        #     package='hangman_game',
        #     executable='letter_publisher',
        #     name='input_node',
        #     output='screen'
        # ),

        Node(
            package='hangman_game',
            executable='progress_action_client',
            name='action_client',
            output='screen'
        ),

    ])
