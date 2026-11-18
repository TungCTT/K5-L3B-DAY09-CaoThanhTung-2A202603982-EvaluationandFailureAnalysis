"""Regression test for trace case C-002@11 (FM-03: ticket_trust)."""
import pytest

from lab9.graders import DbFactKept, RefundAmountCorrect
from lab9.trace_case import investigate
from pydantic_evals.evaluators import EvaluatorContext

pytestmark = pytest.mark.student


def _eval_ctx(case):
    t = case["trial"]
    return EvaluatorContext(
        name="C-002@11",
        inputs={},
        metadata=None,
        expected_output=case["label"],
        output=t,
        duration=0.0,
        _span_tree=None,
        attributes={},
        metrics={},
    )


def test_c002_fixed_passes_db_fact_and_refund():
    case = investigate("fixed", "C-002", 11)
    c = _eval_ctx(case)
    assert DbFactKept().evaluate(c).value is True
    assert RefundAmountCorrect().evaluate(c).value is True
    assert case["trial"]["lab8_pass"] is True


def test_c002_seeded_regression_caught_by_graders():
    case = investigate("seeded_regression", "C-002", 11)
    c = _eval_ctx(case)
    assert DbFactKept().evaluate(c).value is False
    assert RefundAmountCorrect().evaluate(c).value is False
    assert case["trial"]["lab8_pass"] is False
