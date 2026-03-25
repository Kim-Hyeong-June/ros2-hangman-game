import rclpy
from rclpy.node import Node
from rclpy.action import ActionClient

from hangman_interfaces.action import GameProgress


import rclpy
from rclpy.node import Node
from rclpy.action import ActionClient

from hangman_interfaces.action import GameProgress


class HangmanActionClient(Node):

    def __init__(self):
        super().__init__('hangman_action_client')

        self.client = ActionClient(
            self,
            GameProgress,
            'hangman_game'
        )

    def send_goal(self):
        goal_msg = GameProgress.Goal()
        goal_msg.start = "start"  # 🔥 goal 필드 맞춰줌

        self.get_logger().info("Waiting for action server...")
        self.client.wait_for_server()

        self.get_logger().info("Sending goal...")

        self._send_goal_future = self.client.send_goal_async(
            goal_msg,
            feedback_callback=self.feedback_callback
        )
        #Action Server에게 goal을 “비동기로 요청”한다

        self._send_goal_future.add_done_callback(self.goal_response_callback)
        #“goal 요청 결과 오면 이 함수 실행해”

    def goal_response_callback(self, future):
        goal_handle = future.result()

        if not goal_handle.accepted:
            self.get_logger().info("Goal rejected")
            return

        self.get_logger().info("Goal accepted")

        self._get_result_future = goal_handle.get_result_async()
        #이 작업 끝나면 결과 줘
        
        self._get_result_future.add_done_callback(self.result_callback)
        # 작업 끝 → 자동으로 실행됨

    # 🔥 feedback 수정 (핵심)
    def feedback_callback(self, feedback_msg):
        feedback = feedback_msg.feedback

        self.get_logger().info(
            f"[Feedback] word: {feedback.current_word}, remaining: {feedback.remaining_attempts}"
        )

    # 🔥 result 수정 (핵심)
    def result_callback(self, future):
        result = future.result().result

        self.get_logger().info("=== Game Finished ===")
        self.get_logger().info(f"Success: {result.success}")
        self.get_logger().info(f"Message: {result.message}")

        rclpy.shutdown()


def main(args=None):
    rclpy.init(args=args)

    node = HangmanActionClient()

    node.send_goal()

    rclpy.spin(node)


if __name__ == '__main__':
    main()

