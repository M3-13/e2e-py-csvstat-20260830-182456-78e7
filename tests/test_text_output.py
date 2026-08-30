"""Tests for csvstat.text_output."""

from csvstat import text_output


def test_render_numeric_column_rounds_to_four_decimals():
    result = [
        {
            "name": "a",
            "type": "numeric",
            "count": 3,
            "min": 1.23456,
            "max": 3.14159,
            "mean": 2.5,
            "missing": 0,
        }
    ]
    out = text_output.render_text(result)
    assert "Spalte: a" in out
    assert "numeric" in out
    assert "count: 3" in out
    assert "min: 1.2346" in out
    assert "max: 3.1416" in out
    assert "mean: 2.5000" in out
    assert "missing: 0" in out


def test_render_text_column():
    result = [{"name": "b", "type": "text", "distinct": 5, "missing": 2}]
    out = text_output.render_text(result)
    assert "Spalte: b" in out
    assert "text" in out
    assert "distinct: 5" in out
    assert "missing: 2" in out


def test_render_multiple_columns_stable_order():
    result = [
        {
            "name": "a",
            "type": "numeric",
            "count": 1,
            "min": 1.0,
            "max": 1.0,
            "mean": 1.0,
            "missing": 0,
        },
        {"name": "b", "type": "text", "distinct": 1, "missing": 0},
    ]
    out = text_output.render_text(result)
    assert out.index("Spalte: a") < out.index("Spalte: b")


def test_render_rounds_to_fixed_four_decimals_for_whole_numbers():
    result = [
        {
            "name": "a",
            "type": "numeric",
            "count": 1,
            "min": 2.0,
            "max": 2.0,
            "mean": 2.0,
            "missing": 0,
        }
    ]
    out = text_output.render_text(result)
    assert "min: 2.0000" in out
    assert "max: 2.0000" in out
    assert "mean: 2.0000" in out
