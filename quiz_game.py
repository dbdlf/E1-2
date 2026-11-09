"""게임 전체 흐름(메뉴, 풀이, 추가, 목록, 점수, 저장)을 관리하는 QuizGame 클래스."""

from default_quizzes import create_default_quizzes
from input_utils import read_int, read_text
from quiz import Quiz
from storage import StateFileError, StateStorage

LINE = "=" * 40
THIN_LINE = "-" * 40


class QuizGame:
    """퀴즈 목록과 최고 점수를 보관하고, 메뉴 선택에 따라 기능을 실행한다.

    역할 분담
    - Quiz         : 문제 한 개(출력, 정답 확인)
    - StateStorage : state.json 읽기/쓰기
    - QuizGame     : 사용자와의 상호작용과 게임 진행
    """

    def __init__(self, storage: StateStorage):
        self.storage = storage
        self.quizzes: list[Quiz] = []
        self.best_score: int | None = None    # 최고 점수 (100점 만점)
        self.best_correct: int | None = None  # 최고 점수 때 맞힌 문제 수
        self.best_total: int | None = None    # 최고 점수 때 푼 문제 수
        self.running = False
        # 메뉴 번호 → (메뉴 이름, 실행할 메서드)
        self.menu = {
            1: ("퀴즈 풀기", self.play_quiz),
            2: ("퀴즈 추가", self.add_quiz),
            3: ("퀴즈 목록", self.list_quizzes),
            4: ("점수 확인", self.show_score),
            5: ("종료", self.exit_game),
        }

    # ------------------------------------------------------------------
    # 실행 흐름 / 메뉴
    # ------------------------------------------------------------------
    def run(self) -> None:
        """프로그램의 메인 루프. 종료를 고를 때까지 메뉴를 반복한다."""
        self.print_title()
        self.load_state()
        self.running = True
        try:
            while self.running:
                self.show_menu()
                choice = read_int("선택: ", 1, len(self.menu))
                self.handle_menu(choice)
        except (KeyboardInterrupt, EOFError):
            # Ctrl+C 또는 입력 스트림 종료(Ctrl+Z/Ctrl+D) 시에도 저장 후 안전하게 종료한다.
            self.handle_interrupt()

    def print_title(self) -> None:
        print(LINE)
        print("        🎯 나만의 퀴즈 게임 🎯")
        print(LINE)

    def show_menu(self) -> None:
        print(LINE)
        for number, (name, _) in self.menu.items():
            print(f"{number}. {name}")
        print(LINE)

    def handle_menu(self, choice: int) -> None:
        """선택한 번호에 해당하는 메서드를 실행한다."""
        _, action = self.menu[choice]
        action()
        if self.running:
            print()  # 다음 메뉴와 구분하기 위한 빈 줄

    def exit_game(self) -> None:
        if self.save_state():
            print("\n💾 데이터를 저장했습니다.")
        print("👋 게임을 종료합니다. 다음에 또 만나요!")
        self.running = False

    def handle_interrupt(self) -> None:
        print("\n\n⚠️ 입력이 중단되어 프로그램을 종료합니다.")
        if self.save_state():
            print("💾 데이터를 저장했습니다.")
        print("👋 안전하게 종료되었습니다.")
        self.running = False

    # ------------------------------------------------------------------
    # 1. 퀴즈 풀기
    # ------------------------------------------------------------------
    def play_quiz(self) -> None:
        """저장된 퀴즈를 순서대로 출제하고, 다 풀면 결과를 보여 준다."""
        if not self.quizzes:
            print("\n📭 등록된 퀴즈가 없습니다. 먼저 '2. 퀴즈 추가'로 퀴즈를 등록하세요.")
            return

        total = len(self.quizzes)
        print(f"\n📝 퀴즈를 시작합니다! (총 {total}문제)")
        correct = 0
        for number, quiz in enumerate(self.quizzes, start=1):
            if self.ask_question(number, quiz):
                correct += 1
        self.show_result(correct, total)

    def ask_question(self, number: int, quiz: Quiz) -> bool:
        """문제 하나를 출제하고 정답 여부를 돌려준다."""
        print()
        print(THIN_LINE)
        quiz.display(number)
        answer = read_int("정답 입력: ", 1, Quiz.CHOICE_COUNT)
        if quiz.is_correct(answer):
            print("✅ 정답입니다!")
            return True
        print(f"❌ 오답입니다. 정답은 {quiz.answer}번 '{quiz.correct_choice()}'입니다.")
        return False

    def show_result(self, correct: int, total: int) -> None:
        """풀이 결과를 출력하고 최고 점수를 갱신한다."""
        score = self.calculate_score(correct, total)
        print()
        print(LINE)
        print(f"🏆 결과: {total}문제 중 {correct}문제 정답! ({score}점)")
        if self.update_best_score(score, correct, total):
            print("🎉 새로운 최고 점수입니다!")
            self.save_state()
        else:
            print(f"   (현재 최고 점수: {self.best_score}점)")
        print(LINE)

    @staticmethod
    def calculate_score(correct: int, total: int) -> int:
        """정답 수를 100점 만점 점수로 바꾼다."""
        return round(correct / total * 100)

    def update_best_score(self, score: int, correct: int, total: int) -> bool:
        """이번 점수가 최고 점수보다 높으면 갱신하고 True를 돌려준다."""
        if self.best_score is not None and score <= self.best_score:
            return False
        self.best_score = score
        self.best_correct = correct
        self.best_total = total
        return True

    # ------------------------------------------------------------------
    # 2. 퀴즈 추가
    # ------------------------------------------------------------------
    def add_quiz(self) -> None:
        """문제, 선택지 4개, 정답 번호를 입력받아 새 퀴즈를 등록하고 저장한다."""
        print("\n📌 새로운 퀴즈를 추가합니다.\n")
        question = read_text("문제를 입력하세요: ")
        choices = self.read_choices()
        answer = read_int(f"정답 번호 (1-{Quiz.CHOICE_COUNT}): ", 1, Quiz.CHOICE_COUNT)

        self.quizzes.append(Quiz(question, choices, answer))
        if self.save_state():
            print("\n✅ 퀴즈가 추가되었습니다!")
        else:
            print("\n✅ 퀴즈가 추가되었습니다. (파일 저장에 실패하여 이번 실행 중에만 유지됩니다)")

    @staticmethod
    def read_choices() -> list[str]:
        """서로 다른 선택지 4개를 입력받는다."""
        choices: list[str] = []
        while len(choices) < Quiz.CHOICE_COUNT:
            choice = read_text(f"선택지 {len(choices) + 1}: ")
            if choice in choices:
                print("⚠️ 이미 입력한 선택지입니다. 다른 내용을 입력하세요.")
                continue
            choices.append(choice)
        return choices

    # ------------------------------------------------------------------
    # 3. 퀴즈 목록 / 4. 점수 확인
    # ------------------------------------------------------------------
    def list_quizzes(self) -> None:
        """등록된 퀴즈의 문제 목록을 번호와 함께 보여 준다."""
        if not self.quizzes:
            print("\n📭 등록된 퀴즈가 없습니다. '2. 퀴즈 추가'로 퀴즈를 등록하세요.")
            return

        print(f"\n📋 등록된 퀴즈 목록 (총 {len(self.quizzes)}개)\n")
        print(THIN_LINE)
        for number, quiz in enumerate(self.quizzes, start=1):
            print(f"[{number}] {quiz.question}")
        print(THIN_LINE)

    def show_score(self) -> None:
        """저장된 최고 점수를 보여 준다."""
        if self.best_score is None:
            print("\n🏆 아직 퀴즈를 푼 기록이 없습니다. '1. 퀴즈 풀기'로 도전해 보세요!")
            return
        print(f"\n🏆 최고 점수: {self.best_score}점 "
              f"({self.best_total}문제 중 {self.best_correct}문제 정답)")

    # ------------------------------------------------------------------
    # 파일 저장 / 불러오기
    # ------------------------------------------------------------------
    def load_state(self) -> None:
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
            print(f"   기본 퀴즈 {len(self.quizzes)}개로 실행합니다.")
            return

        self.quizzes = state["quizzes"]
        self.best_score = state["best_score"]
        self.best_correct = state["best_correct"]
        self.best_total = state["best_total"]
        best_text = "기록 없음" if self.best_score is None else f"{self.best_score}점"
        print(f"📂 저장된 데이터를 불러왔습니다. (퀴즈 {len(self.quizzes)}개, 최고점수 {best_text})")

    def save_state(self) -> bool:
        """현재 퀴즈 목록과 최고 점수를 저장한다. 성공 여부를 돌려준다."""
        try:
            self.storage.save(self.quizzes, self.best_score, self.best_correct, self.best_total)
        except OSError as error:
            print(f"⚠️ 데이터 저장에 실패했습니다: {error}")
            return False
        return True

    def reset_to_defaults(self) -> None:
        """기본 퀴즈 데이터로 초기화하고 최고 점수 기록을 비운다."""
        self.quizzes = create_default_quizzes()
        self.best_score = None
        self.best_correct = None
        self.best_total = None
