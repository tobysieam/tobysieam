import sys
import os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from generator import Generator
from utils import eval_expr, parse_fraction, normalize_answer_str
from fractions import Fraction


def test_parse_and_normalize():
    assert normalize_answer_str('4') == '4'
    assert normalize_answer_str('7/24') == '7/24'
    assert normalize_answer_str("9/4") == "2'1/4"


def test_eval_nested_and_zero():
    assert eval_expr('0 / 5/6') == Fraction(0)
    assert eval_expr('(1/2 / 3/4) - 2/7') == Fraction(8,21)


def test_generator_large_sample():
    g = Generator(max_value=20)
    ex, ans = g.generate(200)
    assert len(ex) == 200
    # ensure answers parseable
    for a in ans[:20]:
        parse_fraction(a)
