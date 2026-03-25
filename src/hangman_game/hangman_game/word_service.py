import rclpy
from rclpy.node import Node
from hangman_interfaces.srv import CheckLetter
import random


class WordService(Node):

    def __init__(self):
        super().__init__('word_service')

        self.srv = self.create_service(
            CheckLetter,
            'check_letter',
            self.check_letter_callback
        )

        self.word = random.choice(['apple', 'banana', 'robot'])
        self.current_state = ['_' for _ in self.word]

        self.guessed_letters = set()
        self.max_attempts = 6
        self.wrong_attempts = 0
        self.game_over = False

        self.get_logger().info("Word Service Started")
        self.get_logger().info(f"Word selected: {self.word}")

    def check_letter_callback(self, request, response):
        letter = request.letter.lower()

         # 🔥 게임 종료 체크
        if self.game_over:
            response.is_correct = False
            response.message = "Game already finished"
            response.updated_word_state = ''.join(self.current_state)
            return response

        # 🔥 중복 입력 체크
        if letter in self.guessed_letters:
            response.is_correct = False
            response.message = "Already guessed"
            response.updated_word_state = ''.join(self.current_state)
            return response
        
        self.guessed_letters.add(letter)

        # 🔥 정답 체크
        if letter in self.word:
            for i, l in enumerate(self.word):
                if l == letter:
                    self.current_state[i] = letter

            response.is_correct = True
            response.message = "Correct!"
        else:
            self.wrong_attempts += 1
            response.is_correct = False
            response.message = f"Wrong! ({self.wrong_attempts}/{self.max_attempts})"

        # 🔥 승리 조건
        if '_' not in self.current_state:
            self.game_over = True
            response.message = "You Win!"

        # 🔥 패배 조건
        elif self.wrong_attempts >= self.max_attempts:
            self.game_over = True
            response.message = f"Game Over! Word was '{self.word}'"

        response.updated_word_state = ''.join(self.current_state)

        self.get_logger().info(
            f"State: {response.updated_word_state} | Wrong: {self.wrong_attempts}"
        )

        return response


def main(args=None):
    rclpy.init(args=args)

    node = WordService()
    rclpy.spin(node)

    node.destroy_node()
    rclpy.shutdown()


if __name__ == '__main__':
    main()
    