"""Column analysis for CSV data."""

from collections.abc import Iterable, Sequence

MISSING_VALUES = frozenset({"", "na", "n/a", "null", "nan"})


def _is_missing(value: str) -> bool:
    return value.strip().lower() in MISSING_VALUES


def _parse_number(value: str) -> float | None:
    try:
        return float(value)
    except ValueError:
        try:
            return float(int(value))
        except ValueError:
            return None


def analyze(
    headers: Sequence[str],
    rows: Iterable[Sequence[str]],
    columns: Sequence[str] | None = None,
) -> list[dict]:
    header_list = list(headers)

    if columns is None:
        selected = list(header_list)
    else:
        selected = list(columns)
        known = set(header_list)
        for name in selected:
            if name not in known:
                raise ValueError(f"Unbekannte Spalte: {name}")

    index_map: dict[str, int] = {}
    for i, name in enumerate(header_list):
        index_map.setdefault(name, i)

    states = [
        {
            "name": name,
            "idx": index_map[name],
            "numeric": True,
            "count": 0,
            "total": 0.0,
            "min": None,
            "max": None,
            "distinct": set(),
            "missing": 0,
        }
        for name in selected
    ]

    for row in rows:
        for state in states:
            idx = state["idx"]
            value = row[idx] if idx < len(row) else ""
            if _is_missing(value):
                state["missing"] += 1
                continue
            state["distinct"].add(value)
            if state["numeric"]:
                number = _parse_number(value)
                if number is None:
                    state["numeric"] = False
                else:
                    state["count"] += 1
                    state["total"] += number
                    if state["min"] is None or number < state["min"]:
                        state["min"] = number
                    if state["max"] is None or number > state["max"]:
                        state["max"] = number

    result = []
    for state in states:
        if state["numeric"]:
            count = state["count"]
            mean = state["total"] / count if count else 0.0
            result.append(
                {
                    "name": state["name"],
                    "type": "numeric",
                    "count": count,
                    "min": state["min"] if state["min"] is not None else 0.0,
                    "max": state["max"] if state["max"] is not None else 0.0,
                    "mean": mean,
                    "missing": state["missing"],
                }
            )
        else:
            result.append(
                {
                    "name": state["name"],
                    "type": "text",
                    "distinct": len(state["distinct"]),
                    "missing": state["missing"],
                }
            )
    return result
