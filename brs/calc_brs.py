"""
Расчёт итогового рейтинга по Балльно-рейтинговой системе (БРС)
курса «Алгоритмы и структуры данных».

Зависимости: pandas, numpy
"""

import argparse
import re
import sys
from pathlib import Path

import numpy as np
import pandas as pd


# ============================================================
# КОНСТАНТЫ БРС
# ============================================================
SCORE_ON_TIME = 100
SCORE_LATE = 50
SCORE_ABSENT = 0

HARD_DEADLINE_CAP = 50
LATE_PENALTY = 50
MIN_LAB_THRESHOLD = 50
PASSING_SCORE = 70
BONUS_PROJECT_SCORE = 10

WEIGHT_ATTENDANCE = 0.15
WEIGHT_QUIZ = 0.10
WEIGHT_REPORT = 0.15
WEIGHT_LABS = 0.60


# ============================================================
# АВТОМАТИЧЕСКОЕ ОПРЕДЕЛЕНИЕ СТРУКТУРЫ CSV
# ============================================================
def find_numbered_columns(columns: list[str],
                          prefix: str,
                          exclude_prefixes: list[str] | None = None) -> list[int]:
    """
    Находит все номера N в именах колонок вида '<prefix>_N_<suffix>'.
    Опционально исключает колонки, начинающиеся с одного из exclude_prefixes.
    """
    pattern = re.compile(rf"^{re.escape(prefix)}_(\d+)_")
    numbers = set()
    for col in columns:
        if exclude_prefixes and any(col.startswith(f"{ep}_") for ep in exclude_prefixes):
            continue
        m = pattern.match(col)
        if m:
            numbers.add(int(m.group(1)))
    return sorted(numbers)


def detect_structure(df: pd.DataFrame) -> dict:
    """Определяет количество лекций, лаб. занятий и ЛР в файле."""
    cols = list(df.columns)
    return {
        "lectures": find_numbered_columns(cols, "lecture"),
        "lab_sessions": find_numbered_columns(cols, "lab_session"),
        "labs": find_numbered_columns(
            cols, "lab",
            exclude_prefixes=["lab_session"]
        ),
    }


# ============================================================
# ФУНКЦИИ РАСЧЁТА
# ============================================================
def normalize_attendance(value) -> float:
    """Преобразует значение посещаемости в балл."""
    if pd.isna(value) or str(value).strip() == "":
        return 0.0
    s = str(value).strip().lower()
    if s in ("on_time", "вовремя", "100"):
        return float(SCORE_ON_TIME)
    if s in ("late", "опоздание", "50"):
        return float(SCORE_LATE)
    if s in ("absent", "отсутствие", "0"):
        return float(SCORE_ABSENT)
    try:
        return float(s)
    except ValueError:
        return 0.0


def calc_attendance(row: pd.Series, structure: dict) -> float:
    """Средний балл за посещаемость по всем занятиям."""
    scores = []
    for n in structure["lectures"]:
        col = f"lecture_{n}_attendance"
        if col in row.index:
            scores.append(normalize_attendance(row[col]))
    for n in structure["lab_sessions"]:
        col = f"lab_session_{n}_attendance"
        if col in row.index:
            scores.append(normalize_attendance(row[col]))
    if not scores:
        return 0.0
    return float(np.mean(scores))


def calc_quiz(row: pd.Series, structure: dict) -> float:
    """Балл за опросы по правилу сглаживания."""
    scores = []
    for n in structure["lectures"]:
        col = f"lecture_{n}_quiz"
        if col in row.index and pd.notna(row[col]) and str(row[col]).strip() != "":
            try:
                scores.append(float(row[col]))
            except ValueError:
                continue
    if not scores:
        return 0.0
    if len(scores) == 1:
        return scores[0]
    if len(scores) == 2:
        return max(scores)
    scores_sorted = sorted(scores)
    trimmed = scores_sorted[1:-1]
    return float(np.mean(trimmed))


def calc_report(row: pd.Series, structure: dict) -> float:
    """Средний балл за доклады."""
    scores = []
    for n in structure["lectures"]:
        col = f"lecture_{n}_report"
        if col in row.index and pd.notna(row[col]) and str(row[col]).strip() != "":
            try:
                scores.append(float(row[col]))
            except ValueError:
                continue
    return float(np.mean(scores)) if scores else 0.0


def calc_labs(row: pd.Series, structure: dict) -> tuple[float, bool, int]:
    """Возвращает (S_лаб, all_submitted, late_count)."""
    final_scores = []
    all_submitted = True
    late_count = 0

    for n in structure["labs"]:
        score_col = f"lab_{n}_score"
        deadline_col = f"lab_{n}_deadline"

        if score_col not in row.index or deadline_col not in row.index:
            continue

        status = str(row[deadline_col]).strip().lower() if pd.notna(row[deadline_col]) else ""

        if status in ("not_submitted", "не сдано", "не сдана"):
            final_scores.append(0.0)
            all_submitted = False
            late_count += 1
            continue

        raw_score = float(row[score_col]) if pd.notna(row[score_col]) else 0.0

        if status in ("on_time", "вовремя", ""):
            final_scores.append(min(raw_score, 100.0))
        elif status in ("soft_deadline", "жёсткий", "жесткий"):
            final_scores.append(min(raw_score / 2.0, HARD_DEADLINE_CAP))
        elif status in ("late", "после", "просрочено"):
            final_scores.append(0.0)
        else:
            final_scores.append(min(raw_score, 100.0))

    s_lab = float(np.mean(final_scores)) if final_scores else 0.0
    return s_lab, all_submitted, late_count


def parse_project_value(value) -> bool:
    """
    Парсит значение колонки project.
    Поддерживает: 1, True, "yes", "да", "1" и т.д.
    """
    if pd.isna(value):
        return False

    s = str(value).strip().lower()

    # Числовые значения
    if s in ("1", "true", "yes", "да", "y"):
        return True

    # Попытка преобразовать в число
    try:
        return int(float(s)) == 1
    except (ValueError, TypeError):
        return False


def evaluate_student(row: pd.Series, structure: dict) -> pd.Series:
    """Полный расчёт рейтинга и блокирующих условий."""
    s_pos = calc_attendance(row, structure)
    s_opr = calc_quiz(row, structure)
    s_dok = calc_report(row, structure)
    s_lab, all_submitted, late_count = calc_labs(row, structure)

    # Обработка проекта
    has_project = False
    project_raw_value = None

    # Ищем колонку project (с возможными пробелами)
    project_col = None
    for col in row.index:
        if col.strip().lower() == "project":
            project_col = col
            break

    if project_col:
        project_raw_value = row[project_col]
        has_project = parse_project_value(project_raw_value)

    rating = (s_pos * WEIGHT_ATTENDANCE
              + s_opr * WEIGHT_QUIZ
              + s_dok * WEIGHT_REPORT
              + s_lab * WEIGHT_LABS)

    penalty = late_count * LATE_PENALTY
    rating_after_penalty = max(rating - penalty, 0.0)

    bonus = BONUS_PROJECT_SCORE if has_project else 0
    rating_with_bonus = min(rating_after_penalty + bonus, 100.0)

    block_reasons = []
    if not all_submitted:
        block_reasons.append("не сданы все ЛР")
    if s_lab < MIN_LAB_THRESHOLD:
        block_reasons.append(f"S_лаб={s_lab:.2f} < {MIN_LAB_THRESHOLD}")

    is_blocked = len(block_reasons) > 0

    # Если заблокирован, бонус не учитывается
    final_rating = 0.0 if is_blocked else rating_with_bonus
    is_passed = (not is_blocked) and (final_rating >= PASSING_SCORE)

    return pd.Series({
        "S_пос": round(s_pos, 2),
        "S_опр": round(s_opr, 2),
        "S_док": round(s_dok, 2),
        "S_лаб": round(s_lab, 2),
        "ЛР_сдано": len(structure["labs"]) - late_count,
        "ЛР_всего": len(structure["labs"]),
        "Рейтинг_до_штрафа": round(rating, 2),
        "Штраф_ЛР": penalty,
        "Проект_raw": str(project_raw_value) if project_raw_value is not None else "N/A",
        "Проект": "ДА" if has_project else "НЕТ",
        "Бонус_проект": bonus,
        "Рейтинг_итог": round(final_rating, 2),
        "Блок": "ДА" if is_blocked else "НЕТ",
        "Причина_блока": "; ".join(block_reasons) if block_reasons else "-",
        "Зачёт": "ДА" if is_passed else "НЕТ",
    })


# ============================================================
# ВЫБОР ФАЙЛА
# ============================================================
def select_csv_file() -> Path:
    """Интерактивный выбор CSV-файла из текущей директории."""
    csv_files = sorted(Path(".").glob("*.csv"))
    if not csv_files:
        raise FileNotFoundError(
            "В текущей директории не найдено ни одного CSV-файла."
        )
    print("\nДоступные файлы групп:")
    for i, f in enumerate(csv_files, start=1):
        print(f"  {i}. {f.name}")
    while True:
        choice = input(f"\nВыберите номер файла (1–{len(csv_files)}): ").strip()
        if choice.isdigit() and 1 <= int(choice) <= len(csv_files):
            return csv_files[int(choice) - 1]
        print("Некорректный ввод. Попробуйте снова.")


# ============================================================
# ТОЧКА ВХОДА
# ============================================================
def main() -> None:
    parser = argparse.ArgumentParser(
        description="Расчёт БРС по курсу «Алгоритмы и структуры данных»."
    )
    parser.add_argument("csv_path", nargs="?", default=None,
                        help="Путь к CSV-файлу группы.")
    parser.add_argument("-o", "--output", default=None,
                        help="Путь к выходному файлу.")
    args = parser.parse_args()

    csv_path = Path(args.csv_path) if args.csv_path else select_csv_file()
    if not csv_path.exists():
        print(f"❌ Файл {csv_path} не найден.")
        sys.exit(1)

    output_path = Path(args.output) if args.output else csv_path.with_name(f"results_{csv_path.name}")

    df = pd.read_csv(csv_path)

    # Проверка наличия колонки project
    has_project_col = any(col.strip().lower() == "project" for col in df.columns)
    if not has_project_col:
        print("⚠️  В файле отсутствует колонка 'project'. Бонусные баллы не будут начислены.")
        print("   Добавьте колонку 'project' со значениями 0 или 1.\n")

    structure = detect_structure(df)

    print(f"\n📂 Файл: {csv_path}")
    print(f"👥 Студентов: {len(df)}")
    print(f"📚 Лекций обнаружено: {len(structure['lectures'])}")
    print(f"🧪 Лабораторных занятий обнаружено: {len(structure['lab_sessions'])}")
    print(f"📝 Лабораторных работ обнаружено: {len(structure['labs'])}")
    print(f"🎯 Колонка 'project': {'✅ найдена' if has_project_col else '❌ отсутствует'}")
    print()

    if not structure["labs"]:
        print("⚠️  В файле не обнаружено ни одной ЛР. Проверьте структуру CSV.")
        sys.exit(1)

    results = df.apply(lambda row: evaluate_student(row, structure), axis=1)
    df_out = pd.concat([df[["student_id"]], results], axis=1)

    df_out.to_csv(output_path, index=False, encoding="utf-8-sig")
    print(f"✅ Результаты сохранены в {output_path}\n")

    display_cols = ["student_id", "S_пос", "S_опр", "S_док", "S_лаб",
                    "ЛР_сдано", "Проект", "Бонус_проект", "Рейтинг_итог", "Блок", "Зачёт"]
    print(df_out[display_cols].to_string(index=False))


if __name__ == "__main__":
    main()
