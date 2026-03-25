import rclpy
import time

from rclpy.node import Node
from rclpy.action import ActionServer
from rclpy.executors import MultiThreadedExecutor

from std_msgs.msg import String
from hangman_interfaces.action import GameProgress
from hangman_interfaces.srv import CheckLetter


class HangmanActionServer(Node):

    def __init__(self):
        super().__init__('hangman_action_server')

        # Action Server
        self.action_server = ActionServer(
            self,
            GameProgress,
            'hangman_game',
            self.execute_callback
        )

        # Service Client
        self.client = self.create_client(CheckLetter, 'check_letter')

        # Subscriber (letter input)
        self.subscription = self.create_subscription(
            String,
            'input_letter',
            self.letter_callback,
            10
        )

        self.latest_letter = None
        self.wrong_count = 0
        self.max_attempts = 6

        self.get_logger().info("Hangman Action Server Started")

    def letter_callback(self, msg):
        self.latest_letter = msg.data
        self.get_logger().info(f"Received letter: {self.latest_letter}")

    def execute_callback(self, goal_handle):
        self.get_logger().info("Game started!")

        feedback_msg = GameProgress.Feedback()

        game_over = False
        won = False

        while rclpy.ok():
            # 입력 대기
            if self.latest_letter is None:
                time.sleep(0.1)
                continue

            letter = self.latest_letter
            self.latest_letter = None

            # Service 요청
            req = CheckLetter.Request()
            req.letter = letter

            while not self.client.wait_for_service(timeout_sec=1.0):
                self.get_logger().info("Waiting for service...")

            future = self.client.call_async(req)

            while not future.done():
                time.sleep(0.01)

            # ROS 방식으로 기다림
            #rclpy.spin_until_future_complete(self, future)

            response = future.result()

            # 🔥 추가 (중요)
            if response is None:
                self.get_logger().warn("Service response is None")
                continue

            # 결과 출력
            self.get_logger().info(f"{response.message}")
            self.get_logger().info(f"Word: {response.updated_word_state}")

            if not response.is_correct:
                self.wrong_count += 1

            # 🔥 feedback 전송 (핵심)
            feedback_msg.current_word = response.updated_word_state
            feedback_msg.remaining_attempts = self.max_attempts - self.wrong_count

            goal_handle.publish_feedback(feedback_msg)

             # 🔥 종료 조건 (핵심)
            if '_' not in response.updated_word_state:
                won = True
                game_over = True

            if self.wrong_count >= self.max_attempts:
                game_over = True

            if game_over:
                break
            
        # Action 종료 처리
        goal_handle.succeed()

        result = GameProgress.Result()
        result.success = won

        if won:
            result.message = "You win"
        
        else:
            result.message = "Game Over"
        
        self.get_logger().info("Game finished")

        return result

def main(args=None):
    rclpy.init(args=args)

    node = HangmanActionServer()

    executor = MultiThreadedExecutor()
    executor.add_node(node)

    executor.spin()

    node.destroy_node()
    rclpy.shutdown()

if __name__ == '__main__':
    main()
    