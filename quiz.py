"""개별 퀴즈 한 문제를 표현하는 Quiz 클래스."""


class Quiz:
    """문제(question), 선택지 4개(choices), 정답 번호(answer, 1~4)를 가진 퀴즈."""

    CHOICE_COUNT = 4

    def __init__(self, question: str, choices: list[str], answer: int):
        # 잘못된 데이터로 객체가 만들어지지 않도록 생성 시점에 검사한다.
        if not isinstance(question, str) or not question.strip():
            raise ValueError("문제는 비어 있지 않은 문자열이어야 합니다.")
        if not isinstance(choices, list) or len(choices) != self.CHOICE_COUNT:
            raise ValueError(f"선택지는 {self.CHOICE_COUNT}개여야 합니다.")
        if not all(isinstance(choice, str) and choice.strip() for choice in choices):
            raise ValueError("선택지는 비어 있지 않은 문자열이어야 합니다.")
        # bool은 int의 하위 타입이므로 True/False가 정답으로 들어오지 않게 따로 막는다.
        if isinstance(answer, bool) or not isinstance(answer, int):
            raise ValueError("정답은 정수 번호여야 합니다.")
        if not 1 <= answer <= self.CHOICE_COUNT:
            raise ValueError(f"정답은 1~{self.CHOICE_COUNT} 사이의 번호여야 합니다.")

        self.question = question.strip()
        self.choices = [choice.strip() for choice in choices]
        self.answer = answer

    def display(self, number: int | None = None) -> None:
        """문제와 선택지를 화면에 출력한다."""
        print(f"[문제 {number}]" if number is not None else "[문제]")
        print(self.question)
        print()
        for index, choice in enumerate(self.choices, start=1):
            print(f"{index}. {choice}")
        print()

    def is_correct(self, user_answer: int) -> bool:
        """사용자가 고른 번호가 정답인지 확인한다."""
        return user_answer == self.answer

    def correct_choice(self) -> str:
        """정답 번호에 해당하는 선택지 내용을 돌려준다."""
        return self.choices[self.answer - 1]

    def to_dict(self) -> dict:
        """JSON으로 저장할 수 있도록 딕셔너리로 변환한다."""
        return {
            "question": self.question,
            "choices": list(self.choices),
            "answer": self.answer,
        }

    @classmethod
    def from_dict(cls, data: dict) -> "Quiz":
        """딕셔너리(JSON에서 읽은 값)로부터 Quiz 객체를 만든다.

        형식이 잘못되었으면 ValueError를 발생시킨다.
        """
        if not isinstance(data, dict):
            raise ValueError("퀴즈 데이터는 객체(딕셔너리)여야 합니다.")
        try:
            return cls(data["question"], data["choices"], data["answer"])
        except KeyError as error:
            raise ValueError(f"퀴즈에 필수 항목 {error}이(가) 없습니다.") from error
