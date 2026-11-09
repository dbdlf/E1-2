"""게임 전체 흐름을 관리하는 QuizGame 클래스."""

from default_quizzes import create_default_quizzes
from input_utils import read_int

LINE = "=" * 40


class QuizGame:
    """메뉴를 보여 주고, 사용자가 고른 기능을 실행한다."""

    def __init__(self):
        self.quizzes = create_default_quizzes()
        self.running = False

    def run(self):
        self.print_title()
        self.running = True
        while self.running:
            self.show_menu()
            choice = read_int("선택: ", 1, 5)
            if choice == 1:
                print("\n🚧 퀴즈 풀기 기능은 준비 중입니다.")
            elif choice == 2:
                print("\n🚧 퀴즈 추가 기능은 준비 중입니다.")
            elif choice == 3:
                print("\n🚧 퀴즈 목록 기능은 준비 중입니다.")
            elif choice == 4:
                print("\n🚧 점수 확인 기능은 준비 중입니다.")
            else:
                self.exit_game()

    def print_title(self):
        print(LINE)
        print("        🎯 나만의 퀴즈 게임 🎯")

    def show_menu(self):
        print(LINE)
        print("1. 퀴즈 풀기")
        print("2. 퀴즈 추가")
        print("3. 퀴즈 목록")
        print("4. 점수 확인")
        print("5. 종료")
        print(LINE)

    def exit_game(self):
        print("👋 게임을 종료합니다. 다음에 또 만나요!")
        self.running = False
