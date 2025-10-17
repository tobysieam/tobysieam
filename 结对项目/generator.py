import random
from fractions import Fraction
from typing import Tuple, List


class Expr:
    """表达式树：叶子为 Fraction（自然数或真分数），内部结点为运算符和两个子表达式"""
    def __init__(self, op=None, left=None, right=None, value: Fraction=None):
        self.op = op  # '+', '-', '*', '/'
        self.left = left
        self.right = right
        self.value = value

    def is_leaf(self):
        return self.op is None

    def eval(self) -> Fraction:
        if self.is_leaf():
            return self.value
        a = self.left.eval()
        b = self.right.eval()
        if self.op == '+':
            return a + b
        if self.op == '-':
            return a - b
        if self.op == '*':
            return a * b
        if self.op == '/':
            return a / b
        raise ValueError('未知运算符')

    def to_string(self) -> str:
        if self.is_leaf():
            return fraction_to_str(self.value)
        left = self.left.to_string()
        right = self.right.to_string()
        return f'({left} {self.op} {right})'

    def canonical(self) -> str:
        """返回用于去重的规范化字符串：对于 + 和 * 允许交换左右子树（但不做平展）。"""
        if self.is_leaf():
            return fraction_to_str(self.value)
        L = self.left.canonical()
        R = self.right.canonical()
        s1 = f'({L}{self.op}{R})'
        s2 = f'({R}{self.op}{L})'
        if self.op in ['+', '*']:
            return min(s1, s2)
        return s1


def fraction_to_str(fr: Fraction) -> str:
    # natural number
    if fr.denominator == 1:
        return str(fr.numerator)
    # improper fraction -> mixed number
    if abs(fr.numerator) > fr.denominator:
        whole = fr.numerator // fr.denominator
        rem = abs(fr.numerator % fr.denominator)
        return f"{whole}'{rem}/{fr.denominator}"
    return f"{fr.numerator}/{fr.denominator}"


class Generator:
    def __init__(self, max_value: int = 10):
        if max_value < 1:
            raise ValueError('max_value must be >=1')
        self.max_value = max_value

    def random_fraction(self) -> Fraction:
        # generate natural number or proper fraction within range
        # choose to generate integer or fraction
        if random.random() < 0.5:
            return Fraction(random.randrange(0, self.max_value))
        # proper fraction: numerator < denominator, denominator in [2, max_value-1]
        den_max = max(2, self.max_value - 1)
        den = random.randint(2, den_max)
        num = random.randint(1, den - 1)
        return Fraction(num, den)

    def generate_one(self) -> Expr:
        # generate expression with up to 3 operators (i.e., up to 4 operands)
        ops_count = random.randint(1, 3)
        # generate left-to-right binary tree with random parentheses
        expr = Expr(value=self.random_fraction())
        for _ in range(ops_count):
            # choose op but restrict choices to ones that can satisfy constraints
            possible_ops = ['+', '-', '*', '/']
            # prefer random choice but will be validated below
            op = random.choice(possible_ops)

            # Build right operand with targeted approach for '-' and '/'
            if op == '-':
                # choose right such that expr.eval() >= right.eval()
                left_val = expr.eval()
                # sample until right <= left
                while True:
                    right = Expr(value=self.random_fraction())
                    try:
                        if right.eval() <= left_val:
                            break
                    except Exception:
                        pass
                expr = Expr(op='-', left=expr, right=right)
                # ensure overall non-negative
                if expr.eval() < 0:
                    # fallback: change op to +
                    expr = Expr(op='+', left=expr.left, right=right)
                continue

            if op == '/':
                left_val = expr.eval()
                # if left_val <=0, avoid division (pick addition instead)
                if not (left_val > 0):
                    # fallback to multiplication
                    right = Expr(value=self.random_fraction())
                    expr = Expr(op='*', left=expr, right=right)
                    continue
                # pick right such that right.eval() > left_val
                attempts = 0
                while True:
                    attempts += 1
                    right = Expr(value=self.random_fraction())
                    try:
                        rv = right.eval()
                    except Exception:
                        rv = 0
                    if rv != 0 and rv > left_val:
                        # check proper fraction result
                        res = left_val / rv
                        if res > 0 and abs(res.numerator) < res.denominator:
                            break
                    # continue sampling until satisfy
                    if attempts > 500:
                        # as a safe fallback, switch operator to + to avoid stuck loop
                        op = '+'
                        break
                expr = Expr(op=op, left=expr, right=right)
                continue

            # default for + and *: sample random right until no zero-division issues
            right = Expr(value=self.random_fraction())
            expr = Expr(op=op, left=expr, right=right)
        return expr

    def generate(self, n: int) -> Tuple[List[str], List[str]]:
        exercises = []
        answers = []
        seen = set()
        attempts = 0
        while len(exercises) < n and attempts < n * 50:
            attempts += 1
            e = self.generate_one()
            s = e.to_string()
            # remove outer parentheses
            if s.startswith('(') and s.endswith(')'):
                s_inner = s[1:-1]
            else:
                s_inner = s
            key = e.canonical()
            if key in seen:
                continue
            seen.add(key)
            exercises.append(s_inner + ' =')
            ans = fraction_to_str(e.eval())
            answers.append(ans)
        return exercises, answers
