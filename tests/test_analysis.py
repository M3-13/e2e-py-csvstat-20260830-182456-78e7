"""Tests for csvstat.analysis."""

import pytest

from csvstat import analysis


def test_numeric_column_stats():
    result = analysis.analyze(["a"], [["1"], ["2"], ["3"], ["4"]])
    col = result[0]
    assert col["name"] == "a"
    assert col["type"] == "numeric"
    assert col["count"] == 4
    assert col["min"] == 1.0
    assert col["max"] == 4.0
    assert col["mean"] == 2.5
    assert col["missing"] == 0


def test_text_column_distinct():
    result = analysis.analyze(["a"], [["x"], ["y"], ["x"], ["z"]])
    col = result[0]
    assert col["type"] == "text"
    assert col["distinct"] == 3
    assert col["missing"] == 0


def test_mixed_column_is_text_with_all_distinct():
    result = analysis.analyze(["a"], [["1"], ["2"], ["abc"]])
    col = result[0]
    assert col["type"] == "text"
    assert col["distinct"] == 3


def test_negative_and_decimal_numbers_are_numeric():
    result = analysis.analyze(["a"], [["-5"], ["3.14"], ["0"]])
    col = result[0]
    assert col["type"] == "numeric"
    assert col["count"] == 3
    assert col["min"] == -5.0
    assert col["max"] == 3.14
    assert col["mean"] == pytest.approx((-5.0 + 3.14 + 0.0) / 3)


def test_missing_values_are_ignored():
    rows = [["1"], [""], ["NA"], ["N/A"], ["null"], ["nan"], ["2"]]
    result = analysis.analyze(["a"], rows)
    col = result[0]
    assert col["type"] == "numeric"
    assert col["count"] == 2
    assert col["missing"] == 5


def test_missing_values_are_case_insensitive():
    rows = [["Na"], ["NULL"], ["Null"], ["nAn"]]
    result = analysis.analyze(["a"], rows)
    col = result[0]
    assert col["missing"] == 4
    assert col["count"] == 0
    assert col["min"] == 0.0
    assert col["max"] == 0.0
    assert col["mean"] == 0.0


def test_header_without_data_rows():
    result = analysis.analyze(["a", "b"], [])
    assert len(result) == 2
    for col in result:
        assert col["type"] == "numeric"
        assert col["count"] == 0
        assert col["missing"] == 0


def test_columns_filter_preserves_requested_order():
    rows = [["1", "x", "3"], ["2", "y", "4"]]
    result = analysis.analyze(["a", "b", "c"], rows, columns=["c", "a"])
    assert [c["name"] for c in result] == ["c", "a"]
    assert result[0]["type"] == "numeric"
    assert result[1]["type"] == "numeric"


def test_default_column_order_matches_header():
    rows = [["1", "x"], ["2", "y"]]
    result = analysis.analyze(["a", "b"], rows)
    assert [c["name"] for c in result] == ["a", "b"]


def test_unknown_column_raises_value_error():
    rows = [["1", "2"]]
    with pytest.raises(ValueError) as excinfo:
        analysis.analyze(["a", "b"], rows, columns=["a", "zzz"])
    assert "Unbekannte Spalte: zzz" in str(excinfo.value)


def test_missing_column_stats_for_text():
    rows = [["x"], [""], ["NA"], ["y"]]
    result = analysis.analyze(["a"], rows)
    col = result[0]
    assert col["type"] == "text"
    assert col["distinct"] == 2
    assert col["missing"] == 2
