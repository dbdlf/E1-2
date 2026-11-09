"""퀴즈 게임 실행 진입점: python main.py"""

import sys
from pathlib import Path

from quiz_game import QuizGame
from storage import StateStorage

# 실행 위치와 상관없이 항상 프로젝트 루트(main.py가 있는 폴더)의 state.json을 사용한다.
STATE_FILE = Path(__file__).resolve().parent / "state.json"


def configure_console() -> None:
    """출력이 파일/파이프로 연결되어도 한글·이모지가 깨지지 않도록 UTF-8로 맞춘다."""
    for stream in (sys.stdout, sys.stdin):
        encoding = (getattr(stream, "encoding", "") or "").lower().replace("-", "")
        if encoding != "utf8" and hasattr(stream, "reconfigure"):
            stream.reconfigure(encoding="utf-8", errors="replace")


def main() -> None:
    configure_console()
    game = QuizGame(StateStorage(STATE_FILE))
    try:
        game.run()
    except KeyboardInterrupt:
        # 데이터를 불러오는 도중처럼 게임 루프 밖에서 Ctrl+C가 눌린 경우.
        # 상태가 아직 준비되지 않았을 수 있으므로 저장하지 않고 종료한다.
        print("\n👋 프로그램을 종료합니다.")


if __name__ == "__main__":
    main()
