import pytest
import sys
import os
# ensure project root is on path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from generator import Generator, Expr
from utils import parse_fraction, eval_expr
from fractions import Fraction


def test_parse_fraction_mixed_and_simple():
    assert parse_fraction('3/5') == Fraction(3,5)
    assert parse_fraction("2'3/8") == Fraction(2) + Fraction(3,8)
    assert parse_fraction('4') == Fraction(4,1)


def test_generator_range_and_ops():
    g = Generator(max_value=10)
    exs, ans = g.generate(50)
    assert len(exs) == 50
    # ensure no operator count >3 (approx by counting ops in string)
    for e in exs:
        # count operators but ignore '/' that are part of fractions (we count tokens)
        tokens = e.replace("/", " ").split()
        opcount = sum(1 for t in tokens for c in t if c in '+-*×÷')
        assert opcount <= 3


def test_no_negative_intermediate():
    g = Generator(max_value=10)
    for _ in range(100):
        expr = g.generate_one()
        # traverse nodes and evaluate each subexpression (via eval on subtree)
        def walk(node):
            if node.is_leaf():
                return [node.eval()]
            vals = [node.eval()]
            vals += walk(node.left)
            vals += walk(node.right)
            return vals
        vals = walk(expr)
        assert all(v >= 0 for v in vals)


def test_division_is_proper_fraction():
    g = Generator(max_value=10)
    for _ in range(200):
        e = g.generate_one()
        # walk nodes to find divisions
        def find_divs(node):
            found = []
            if not node.is_leaf():
                if node.op == '/':
                    found.append((node.left.eval(), node.right.eval(), node.eval()))
                found += find_divs(node.left)
                found += find_divs(node.right)
            return found
        for L, R, res in find_divs(e):
            # result must be a proper fraction (0<res<1) for positive numbers
            assert R != 0
            assert res > 0 and abs(res.numerator) < res.denominator


def test_dedup_examples():
    # Build small trees to test canonical equivalence behavior
    a = Expr(value=Fraction(1,1))
    b = Expr(value=Fraction(2,1))
    c = Expr(value=Fraction(3,1))
    # (1+2)+3
    t1 = Expr(op='+', left=Expr(op='+', left=a, right=b), right=c)
    # 3+(2+1)
    t2 = Expr(op='+', left=c, right=Expr(op='+', left=b, right=a))
    # Their canonical should be equal (per requirement example)
    assert t1.canonical() == t2.canonical()
