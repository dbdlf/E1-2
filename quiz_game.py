"""게임 전체 흐름을 관리하는 QuizGame 클래스."""

from default_quizzes import create_default_quizzes
from input_utils import read_int
from quiz import Quiz

LINE = "=" * 40
THIN_LINE = "-" * 40


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
                self.play_quiz()
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

    def play_quiz(self):
        """저장된 퀴즈를 순서대로 출제하고 정답/오답을 알려 준다."""
        print(f"\n📝 퀴즈를 시작합니다! (총 {len(self.quizzes)}문제)")
        for number, quiz in enumerate(self.quizzes, start=1):
            print()
            print(THIN_LINE)
            quiz.display(number)
            answer = read_int("정답 입력: ", 1, Quiz.CHOICE_COUNT)
            if quiz.is_correct(answer):
                print("✅ 정답입니다!")
            else:
                print(f"❌ 오답입니다. 정답은 {quiz.answer}번 '{quiz.correct_choice()}'입니다.")

    def exit_game(self):
        print("👋 게임을 종료합니다. 다음에 또 만나요!")
        self.running = False
