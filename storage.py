"""state.json 파일 저장/불러오기를 담당하는 StateStorage 클래스."""

import json
import os
from pathlib import Path

from quiz import Quiz


class StateFileError(Exception):
    """state.json 내용이 손상되었거나 형식이 올바르지 않을 때 발생하는 예외."""


def _is_int(value) -> bool:
    """bool(True/False)을 제외한 진짜 정수인지 확인한다. (bool은 int의 하위 타입)"""
    return isinstance(value, int) and not isinstance(value, bool)


class StateStorage:
    """퀴즈 목록과 최고 점수를 JSON 파일(UTF-8)로 저장하고 불러온다.

    저장 형식(스키마):
    {
        "quizzes": [{"question": str, "choices": [str x4], "answer": 1~4}, ...],
        "best_score": 0~100 또는 null,
        "best_correct": 정답 수 또는 null,   (선택 항목)
        "best_total": 푼 문제 수 또는 null   (선택 항목)
    }
    필수 키는 quizzes 하나이며, {"quizzes": [...], "best_score": 3} 같은
    최소 형식도 그대로 읽을 수 있다.
    """

    def __init__(self, path: str | Path):
        self.path = Path(path)

    def load(self) -> dict:
        """파일을 읽어 {"quizzes": [Quiz, ...], "best_score": ..., ...} 형태로 돌려준다.

        - 파일이 없으면 FileNotFoundError
        - 내용이 손상/형식 오류이면 StateFileError
        - 그 밖의 읽기 오류(권한 등)는 OSError
        """
        # utf-8-sig: 메모장 등에서 BOM이 붙은 UTF-8로 저장해도 읽을 수 있게 한다.
        with open(self.path, "r", encoding="utf-8-sig") as file:
            try:
                data = json.load(file)
            except (json.JSONDecodeError, UnicodeDecodeError) as error:
                raise StateFileError(f"JSON 형식이 올바르지 않습니다: {error}") from error
        return self._parse(data)

    def save(
        self,
        quizzes: list[Quiz],
        best_score: int | None,
        best_correct: int | None,
        best_total: int | None,
    ) -> None:
        """현재 상태를 파일에 저장한다. 실패하면 OSError가 발생한다.

        저장 도중 프로그램이 멈춰도 기존 파일이 깨지지 않도록
        임시 파일에 먼저 쓴 뒤 원래 파일과 교체한다.
        """
        data = {
            "quizzes": [quiz.to_dict() for quiz in quizzes],
            "best_score": best_score,
            "best_correct": best_correct,
            "best_total": best_total,
        }
        temp_path = self.path.with_name(self.path.name + ".tmp")
        with open(temp_path, "w", encoding="utf-8") as file:
            json.dump(data, file, ensure_ascii=False, indent=4)
            file.write("\n")
        os.replace(temp_path, self.path)

    def backup_corrupted(self) -> Path | None:
        """손상된 파일을 state.json.bak 으로 옮겨 둔다. 실패하면 None."""
        backup_path = self.path.with_name(self.path.name + ".bak")
        try:
            os.replace(self.path, backup_path)
        except OSError:
            return None
        return backup_path

    @staticmethod
    def _parse(data) -> dict:
        """JSON에서 읽은 값을 검사하고 Quiz 객체 목록으로 변환한다."""
        if not isinstance(data, dict):
            raise StateFileError("최상위 데이터가 객체({ })가 아닙니다.")

        raw_quizzes = data.get("quizzes")
        if not isinstance(raw_quizzes, list):
            raise StateFileError("'quizzes' 항목이 없거나 목록이 아닙니다.")
        try:
            quizzes = [Quiz.from_dict(item) for item in raw_quizzes]
        except ValueError as error:
            raise StateFileError(f"퀴즈 데이터 오류: {error}") from error

        best_score = data.get("best_score")
        best_correct = data.get("best_correct")
        best_total = data.get("best_total")
        if best_score is None:
            # 아직 한 번도 풀지 않은 상태
            best_correct = best_total = None
        else:
            if not _is_int(best_score) or not 0 <= best_score <= 100:
                raise StateFileError("best_score는 0~100 사이의 정수여야 합니다.")
            if best_correct is None or best_total is None:
                # 최소 형식: 점수만 있고 상세 기록(정답 수/문제 수)은 없는 경우
                best_correct = best_total = None
            elif not (_is_int(best_correct) and _is_int(best_total)
                      and 0 <= best_correct <= best_total and best_total > 0):
                raise StateFileError("best_correct/best_total 값이 올바르지 않습니다.")

        return {
            "quizzes": quizzes,
            "best_score": best_score,
            "best_correct": best_correct,
            "best_total": best_total,
        }
