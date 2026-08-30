"""Command-line interface for csvstat."""

import argparse
import csv
import sys

from csvstat import analysis, json_output, text_output


def _build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        prog="csvstat",
        description="Liest eine CSV-Datei und gibt einfache Statistiken pro Spalte aus.",
    )
    parser.add_argument("path", help="Pfad zur CSV-Datei")
    parser.add_argument(
        "--delimiter",
        default=",",
        help="Spaltentrennzeichen (Standard: ','; 'TAB' oder '\\t' für Tabulator)",
    )
    parser.add_argument(
        "--columns",
        help="Komma-separierte Liste der auszugebenden Spalten",
    )
    parser.add_argument(
        "--json",
        action="store_true",
        help="Ausgabe als JSON",
    )
    return parser


def main(argv=None) -> int:
    parser = _build_parser()
    args = parser.parse_args(argv)

    delimiter = args.delimiter
    if delimiter in ("TAB", "\\t"):
        delimiter = "\t"

    try:
        with open(args.path, newline="", encoding="utf-8", errors="replace") as f:
            reader = csv.reader(f, delimiter=delimiter)
            try:
                headers = next(reader)
            except StopIteration:
                print("Fehler: Die Datei ist leer.", file=sys.stderr)
                return 1

            columns = [c.strip() for c in args.columns.split(",")] if args.columns else None

            try:
                result = analysis.analyze(headers, reader, columns)
            except ValueError as exc:
                print(f"Fehler: {exc}", file=sys.stderr)
                return 1
    except FileNotFoundError:
        print(f"Fehler: Datei nicht gefunden: {args.path}", file=sys.stderr)
        return 1
    except PermissionError:
        print(f"Fehler: Keine Leseberechtigung für: {args.path}", file=sys.stderr)
        return 1
    except OSError as exc:
        print(f"Fehler: Datei konnte nicht geöffnet werden: {exc}", file=sys.stderr)
        return 1

    if args.json:
        print(json_output.render_json(result))
    else:
        print(text_output.render_text(result))
    return 0


if __name__ == "__main__":
    sys.exit(main())
