import pytest
from satquery.evaluation.metrics import (
    normalize_answer,
    exact_match,
    token_f1,
)


def test_normalize_answer():
    assert normalize_answer("  Hello, World!  ") == "hello world"
    assert normalize_answer("U.S.A. / urban-area... ") == "usa urbanarea"
    assert normalize_answer("") == ""


def test_exact_match():
    assert exact_match("Urban Area", "urban area") == 1.0
    assert exact_match("urban", "rural") == 0.0


def test_token_f1():
    assert token_f1("dense urban forest", "dense forest") == pytest.approx(0.8)
    assert token_f1("water body", "water body") == 1.0
    assert token_f1("desert", "forest") == 0.0
    assert token_f1("", "") == 1.0
