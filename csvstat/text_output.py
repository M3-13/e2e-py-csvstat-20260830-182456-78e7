"""Human-readable text output for csvstat."""


def render_text(result: list[dict]) -> str:
    blocks = []
    for column in result:
        name = column["name"]
        kind = column["type"]
        lines = [f"Spalte: {name} ({kind})"]
        if kind == "numeric":
            lines.append(f"  count: {column['count']}")
            lines.append(f"  min: {column['min']:.4f}")
            lines.append(f"  max: {column['max']:.4f}")
            lines.append(f"  mean: {column['mean']:.4f}")
            lines.append(f"  missing: {column['missing']}")
        else:
            lines.append(f"  distinct: {column['distinct']}")
            lines.append(f"  missing: {column['missing']}")
        blocks.append("\n".join(lines))
    return "\n\n".join(blocks)
