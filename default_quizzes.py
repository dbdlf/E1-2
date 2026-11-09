"""기본 퀴즈 데이터 (주제: 파이썬 & 개발 기초 상식).

state.json이 없거나 손상되었을 때 이 데이터로 게임을 시작한다.
"""

from quiz import Quiz


def create_default_quizzes() -> list[Quiz]:
    """기본 퀴즈 8개를 Quiz 인스턴스로 만들어 돌려준다."""
    return [
        Quiz(
            "파이썬에서 리스트의 길이(원소 개수)를 구하는 내장 함수는?",
            ["len()", "size()", "length()", "count()"],
            1,
        ),
        Quiz(
            "파이썬에서 bool(\"\") (빈 문자열)의 결과는?",
            ["True", "False", "None", "오류 발생"],
            2,
        ),
        Quiz(
            "for i in range(3): 에서 i가 차례로 갖는 값은?",
            ["1, 2, 3", "0, 1, 2", "0, 1, 2, 3", "1, 2"],
            2,
        ),
        Quiz(
            "파이썬에서 {\"name\": \"Kim\"} 처럼 키와 값을 짝지어 저장하는 자료형은?",
            ["list", "tuple", "dict", "set"],
            3,
        ),
        Quiz(
            "클래스의 메서드에서 객체 자기 자신을 가리키는 첫 번째 매개변수 이름(관례)은?",
            ["this", "me", "cls", "self"],
            4,
        ),
        Quiz(
            "Git에서 변경한 파일을 스테이징 영역에 올리는 명령어는?",
            ["git commit", "git add", "git push", "git init"],
            2,
        ),
        Quiz(
            "원격 저장소의 변경 사항을 가져와 현재 브랜치에 합치는 Git 명령어는?",
            ["git clone", "git status", "git pull", "git log"],
            3,
        ),
        Quiz(
            "JSON은 무엇의 약자일까?",
            [
                "JavaScript Object Notation",
                "Java Standard Object Naming",
                "JavaScript Online Network",
                "Just Simple Object Note",
            ],
            1,
        ),
    ]
