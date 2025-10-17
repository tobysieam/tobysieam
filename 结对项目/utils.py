from fractions import Fraction
import re
from typing import List, Tuple


def parse_fraction(s: str) -> Fraction:
    s = s.strip()
    # mixed number like 2'3/8
    # accept both ASCII apostrophe and Unicode ’
    if "'" in s or "’" in s:
        sep = "'" if "'" in s else "’"
        whole, frac = s.split(sep)
        a, b = frac.split('/')
        return Fraction(int(whole)) + Fraction(int(a), int(b))
    if '/' in s:
        a, b = s.split('/')
        return Fraction(int(a), int(b))
    return Fraction(int(s))


def parse_exercises_file(path: str) -> List[str]:
    with open(path, 'r', encoding='utf-8') as f:
        lines = [line.strip() for line in f if line.strip()]
    # expect each line like: expression =
    return [line.rstrip('= ').strip() for line in lines]


def parse_answers_file(path: str) -> List[str]:
    with open(path, 'r', encoding='utf-8') as f:
        lines = [line.strip() for line in f if line.strip()]
    return lines


def eval_expr(expr: str) -> Fraction:
    # convert operators to python and evaluate safely using Fraction
    # tokenization: numbers, fractions like a/b, mixed like 2'3/8
    expr = expr.replace('×', '*').replace('÷', '/')
    # replace mixed numbers
    expr = re.sub(r"(\d+)'(\d+)/(\d+)", lambda m: f"({int(m.group(1))} + Fraction({m.group(2)},{m.group(3)}))", expr)
    # replace simple fractions
    expr = re.sub(r"(\d+)/(\d+)", lambda m: f"Fraction({m.group(1)},{m.group(2)})", expr)
    # ensure integers are plain
    expr = re.sub(r"(?<!Fraction\()\b(\d+)\b", lambda m: f"Fraction({m.group(1)},1)", expr)
    # safe eval
    from fractions import Fraction
    return eval(expr, {'Fraction': Fraction})


def normalize_answer_str(s: str) -> str:
    # convert Fraction to required string formats
    fr = parse_fraction(s) if ("/" in s or "'" in s) or re.fullmatch(r"\d+", s) else Fraction(int(s))
    if fr.denominator == 1:
        return str(fr.numerator)
    if abs(fr.numerator) > fr.denominator:
        whole = fr.numerator // fr.denominator
        rem = abs(fr.numerator % fr.denominator)
        return f"{whole}'{rem}/{fr.denominator}"
    return f"{fr.numerator}/{fr.denominator}"


def grade(exercises: List[str], user_answers: List[str]) -> Tuple[List[int], List[int]]:
    correct = []
    wrong = []
    for i, expr in enumerate(exercises, start=1):
        try:
            real = eval_expr(expr)
            real_s = normalize_answer_str(str(real.numerator) + '/' + str(real.denominator) if real.denominator!=1 else str(real.numerator))
        except Exception:
            real_s = 'ERR'
        user = user_answers[i-1] if i-1 < len(user_answers) else ''
        try:
            user_fr = parse_fraction(user)
            user_s = normalize_answer_str(str(user_fr.numerator) + '/' + str(user_fr.denominator) if user_fr.denominator!=1 else str(user_fr.numerator))
        except Exception:
            user_s = 'ERR'
        if real_s == user_s:
            correct.append(i)
        else:
            wrong.append(i)
    return correct, wrong
