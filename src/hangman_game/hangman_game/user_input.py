import rclpy
from rclpy.node import Node
from std_msgs.msg import String


class UserInputNode(Node):

    def __init__(self):
        super().__init__('user_input_node')

        self.publisher_ = self.create_publisher(
            String,
            'input_letter',
            10
        )

        self.get_logger().info("User Input Node Started")

    def run(self):
        while rclpy.ok():
            letter = input("Enter a letter: ")

            # 입력 검증
            if len(letter) != 1 or not letter.isalpha():
                self.get_logger().warn("Enter a single alphabet letter")
                continue

            msg = String()
            msg.data = letter.lower()

            self.publisher_.publish(msg)

            self.get_logger().info(f"Sent: {msg.data}")


def main(args=None):
    rclpy.init(args=args)

    node = UserInputNode()

    try:
        node.run()
    except KeyboardInterrupt:
        pass

    node.destroy_node()
    rclpy.shutdown()


if __name__ == '__main__':
    main()
    