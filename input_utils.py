"""콘솔 입력을 안전하게 받기 위한 함수 모음.

모든 입력은 앞뒤 공백을 제거한 뒤 검사하고,
잘못된 값이면 안내 메시지를 출력한 다음 다시 입력받는다.
"""


def read_int(prompt: str, min_value: int, max_value: int) -> int:
    """min_value 이상 max_value 이하의 정수를 입력받을 때까지 반복한다.

    - 빈 입력(그냥 Enter) → 안내 후 재입력
    - 숫자로 변환할 수 없는 값(예: abc) → 안내 후 재입력
    - 허용 범위 밖의 숫자(예: 메뉴 9, 정답 0) → 안내 후 재입력
    """
    range_text = f"{min_value}-{max_value} 사이의 숫자를 입력하세요."
    while True:
        raw = input(prompt).strip()

        if raw == "":
            print(f"⚠️ 입력이 비어 있습니다. {range_text}")
            continue

        try:
            value = int(raw)
        except ValueError:
            print(f"⚠️ 잘못된 입력입니다. {range_text}")
            continue

        if not min_value <= value <= max_value:
            print(f"⚠️ 범위를 벗어난 숫자입니다. {range_text}")
            continue

        return value


def read_text(prompt: str) -> str:
    """비어 있지 않은 문자열을 입력받을 때까지 반복한다."""
    while True:
        text = input(prompt).strip()
        if text:
            return text
        print("⚠️ 빈 값은 입력할 수 없습니다. 다시 입력하세요.")
