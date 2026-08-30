# csvstat

csvstat ist ein kleines Python-Kommandozeilenwerkzeug, das eine CSV-Datei einliest
und pro Spalte einfache Statistiken ausgibt: für numerische Spalten
count/min/max/Mittelwert und die Anzahl fehlender Werte, für Textspalten die Anzahl
eindeutiger Werte. Es unterstützt konfigurierbare Trennzeichen, die Auswahl einzelner
Spalten sowie eine JSON-Ausgabe und liefert bei ungültigen Eingaben verständliche
Fehlermeldungen ohne Traceback.

## Tech-Stack

- Python (>= 3.10)
- argparse (Kommandozeile)
- csv, json, statistics (Standardbibliothek)
- pytest (Tests)
- pyproject.toml (Paketierung mit setuptools)

## Installation

```bash
pip install -e ".[dev]"
```

## Nutzung

```bash
csvstat <pfad> [Optionen]
```

Verfügbare Optionen:

- `path` (Positional): Pfad zur CSV-Datei.
- `--delimiter`: Spaltentrennzeichen (Standard `,`; `TAB` oder `\t` für Tabulator).
- `--columns`: Komma-separierte Liste der auszugebenden Spalten.
- `--json`: Ausgabe als JSON statt Text.

Beispiele:

```bash
csvstat daten.csv
csvstat daten.csv --delimiter ";"
csvstat daten.csv --columns name,wert
csvstat daten.csv --json
```
