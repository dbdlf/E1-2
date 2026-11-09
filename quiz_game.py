"""게임 전체 흐름을 관리하는 QuizGame 클래스."""

from default_quizzes import create_default_quizzes
from input_utils import read_int
from quiz import Quiz
from storage import StateFileError, StateStorage

LINE = "=" * 40
THIN_LINE = "-" * 40


class QuizGame:
    """메뉴를 보여 주고, 사용자가 고른 기능을 실행한다."""

    def __init__(self, storage: StateStorage):
        self.storage = storage
        self.quizzes = []
        self.best_score = None
        self.best_correct = None
        self.best_total = None
        self.running = False

    def run(self):
        self.print_title()
        self.load_state()
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
        print(LINE)

    def show_menu(self):
        print(LINE)
        print("1. 퀴즈 풀기")
        print("2. 퀴즈 추가")
        print("3. 퀴즈 목록")
        print("4. 점수 확인")
        print("5. 종료")
        print(LINE)

    def play_quiz(self):
        """저장된 퀴즈를 순서대로 출제하고, 다 풀면 결과를 보여 준다."""
        if not self.quizzes:
            print("\n📭 등록된 퀴즈가 없습니다. 먼저 '2. 퀴즈 추가'로 퀴즈를 등록하세요.")
            return

        total = len(self.quizzes)
        correct = 0
        print(f"\n📝 퀴즈를 시작합니다! (총 {total}문제)")
        for number, quiz in enumerate(self.quizzes, start=1):
            print()
            print(THIN_LINE)
            quiz.display(number)
            answer = read_int("정답 입력: ", 1, Quiz.CHOICE_COUNT)
            if quiz.is_correct(answer):
                correct += 1
                print("✅ 정답입니다!")
            else:
                print(f"❌ 오답입니다. 정답은 {quiz.answer}번 '{quiz.correct_choice()}'입니다.")

        score = self.calculate_score(correct, total)
        print()
        print(LINE)
        print(f"🏆 결과: {total}문제 중 {correct}문제 정답! ({score}점)")
        print(LINE)

    @staticmethod
    def calculate_score(correct, total):
        """정답 수를 100점 만점 점수로 바꾼다."""
        return round(correct / total * 100)

    def exit_game(self):
        if self.save_state():
            print("\n💾 데이터를 저장했습니다.")
        print("👋 게임을 종료합니다. 다음에 또 만나요!")
        self.running = False

    # ---------------- 파일 저장 / 불러오기 ----------------
    def load_state(self):
        """state.json을 불러온다. 없거나 손상되었으면 기본 퀴즈로 시작한다."""
        try:
            state = self.storage.load()
        except FileNotFoundError:
            self.reset_to_defaults()
            print(f"📂 저장된 데이터가 없어 기본 퀴즈 {len(self.quizzes)}개로 시작합니다.")
            self.save_state()
            return
        except StateFileError as error:
            print(f"⚠️ 데이터 파일이 손상되었습니다. ({error})")
            backup_path = self.storage.backup_corrupted()
            if backup_path is not None:
                print(f"   손상된 파일은 '{backup_path.name}'(으)로 백업했습니다.")
            self.reset_to_defaults()
            print(f"🔧 기본 퀴즈 {len(self.quizzes)}개로 복구합니다.")
            self.save_state()
            return
        except OSError as error:
            print(f"⚠️ 데이터 파일을 읽을 수 없습니다. ({error})")
            self.reset_to_defaults()
            print(f"기본 퀴즈 {len(self.quizzes)}개로 실행합니다.")
            return

        self.quizzes = state["quizzes"]
        self.best_score = state["best_score"]
        self.best_correct = state["best_correct"]
        self.best_total = state["best_total"]
        best_text = "기록 없음" if self.best_score is None else f"{self.best_score}점"
        print(f"📂 저장된 데이터를 불러왔습니다. (퀴즈 {len(self.quizzes)}개, 최고점수 {best_text})")

    def save_state(self):
        """현재 퀴즈 목록과 최고 점수를 저장한다. 성공 여부를 돌려준다."""
        try:
            self.storage.save(self.quizzes, self.best_score, self.best_correct, self.best_total)
        except OSError as error:
            print(f"⚠️ 데이터 저장에 실패했습니다: {error}")
            return False
        return True

    def reset_to_defaults(self):
        """기본 퀴즈 데이터로 초기화하고 최고 점수 기록을 비운다."""
        self.quizzes = create_default_quizzes()
        self.best_score = None
        self.best_correct = None
        self.best_total = None
