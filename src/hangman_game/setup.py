from setuptools import find_packages, setup

package_name = 'hangman_game'

setup(
    name=package_name,
    version='0.0.0',
    packages=find_packages(exclude=['test']),
    data_files=[
        ('share/ament_index/resource_index/packages',
            ['resource/' + package_name]),
        ('share/' + package_name, ['package.xml']),

        # 🔥 이거 추가
        ('share/hangman_game/launch', ['launch/hangman.launch.py']),
    ],
    install_requires=['setuptools'],
    zip_safe=True,
    maintainer='kimhyeongjune',
    maintainer_email='york0095@naver.com',
    description='TODO: Package description',
    license='TODO: License declaration',
    extras_require={
        'test': [
            'pytest',
        ],
    },

    entry_points={
        'console_scripts': [
            'word_service = hangman_game.word_service:main',
            'letter_publisher = hangman_game.letter_publisher:main',
            'progress_action_server = hangman_game.progress_action_server:main',
            'progress_action_client = hangman_game.progress_action_client:main',
        ],
    },

)
