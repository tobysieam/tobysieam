import pytest
from checker import calc_similarity

def test_identical():
    assert abs(calc_similarity("abc", "abc") - 1.0) < 1e-6

def test_completely_different():
    assert abs(calc_similarity("abc", "xyz") - 0.0) < 1e-6

def test_partial_overlap():
    assert abs(calc_similarity("abcdef", "abdf") - 4/6) < 1e-6

def test_empty_orig():
    assert abs(calc_similarity("", "abc") - 0.0) < 1e-6

def test_empty_plag():
    assert abs(calc_similarity("abc", "") - 0.0) < 1e-6

def test_chinese():
    orig = "今天是星期天，天气晴，今天晚上我要去看电影。"
    plag = "今天是周天，天气晴朗，我晚上要去看电影。"
    sim = calc_similarity(orig, plag)
    assert 0.5 < sim < 1.0

def test_case_sensitive():
    assert abs(calc_similarity("ABC", "abc") - 0.0) < 1e-6

def test_substring():
    assert abs(calc_similarity("abcdef", "abc") - 3/6) < 1e-6

def test_long_text():
    orig = "a" * 1000
    plag = "a" * 800 + "b" * 200
    sim = calc_similarity(orig, plag)
    assert 0.7 < sim < 1.0

def test_special_chars():
    assert abs(calc_similarity("a,b.c!d?e", "abcde") - 5/9) < 1e-6
