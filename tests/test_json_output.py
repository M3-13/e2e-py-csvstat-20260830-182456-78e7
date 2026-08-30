"""Tests for csvstat JSON output."""

import json

from csvstat.json_output import render_json


def test_render_json_numeric_and_text_column():
    result = [
        {
            "name": "wert",
            "type": "numeric",
            "count": 3,
            "min": 1.0,
            "max": 3.0,
            "mean": 2.0,
            "missing": 0,
        },
        {
            "name": "label",
            "type": "text",
            "distinct": 2,
            "missing": 1,
        },
    ]
    data = json.loads(render_json(result))

    assert data["wert"]["type"] == "numeric"
    assert data["wert"]["count"] == 3
    assert data["wert"]["min"] == 1.0
    assert data["wert"]["max"] == 3.0
    assert data["wert"]["mean"] == 2.0
    assert data["wert"]["missing"] == 0
    assert data["label"]["type"] == "text"
    assert data["label"]["distinct"] == 2
    assert data["label"]["missing"] == 1
    assert "name" not in data["wert"]
    assert "name" not in data["label"]


def test_render_json_does_not_round_numeric_values():
    result = [
        {
            "name": "a",
            "type": "numeric",
            "count": 3,
            "min": 0.0,
            "max": 1.0,
            "mean": 1.0 / 3.0,
            "missing": 0,
        }
    ]
    data = json.loads(render_json(result))

    assert data["a"]["mean"] == 1.0 / 3.0
    assert data["a"]["mean"] != 0.33


def test_render_json_stable_field_order():
    result = [
        {
            "name": "wert",
            "type": "numeric",
            "count": 1,
            "min": 5.0,
            "max": 5.0,
            "mean": 5.0,
            "missing": 0,
        }
    ]
    first = render_json(result)
    second = render_json(result)

    assert first == second
    assert first.index('"type"') < first.index('"count"')
    assert first.index('"count"') < first.index('"min"')


def test_render_json_empty_result_is_empty_object():
    assert render_json([]) == "{}"
