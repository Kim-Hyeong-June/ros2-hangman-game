import rclpy
from rclpy.node import Node
from std_msgs.msg import String
import threading


class LetterPublisher(Node):

    def __init__(self):
        super().__init__('letter_publisher')

        # Topic 이름 (다른 노드랑 맞춰야 함)
        self.publisher_ = self.create_publisher(String, 'input_letter', 10)

        self.get_logger().info("Letter Publisher Started")

    def run(self):
        while rclpy.ok():
            letter = input("Enter a letter: ")

            # 입력 검증 (중요🔥)
            if len(letter) != 1 or not letter.isalpha():
                self.get_logger().warn("Please enter a single alphabet letter")
                continue

            msg = String()
            msg.data = letter.lower()

            self.publisher_.publish(msg)

            self.get_logger().info(f"Published: {msg.data}")

def main(args=None):
    rclpy.init(args=args)

    node = LetterPublisher()

    # 입력 루프를 별도 스레드로 실행
    thread = threading.Thread(target=node.run)
    thread.daemon = True
    thread.start()

    # ROS 통신 처리 (핵심🔥)
    rclpy.spin(node)

    node.destroy_node()
    rclpy.shutdown()

