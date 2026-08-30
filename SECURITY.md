VERDICT: CHANGES_REQUESTED

## Sicherheitsbericht

### Zusammenfassung
Das Produkt ist ein kleines, lokal ausgeführtes CLI-Tool ohne Netzwerk- oder Web-Angriffsfläche. Die Kernanforderung AC-08 ist erfüllt: Es kommen ausschließlich `int()` und `float()` zur numerischen Typ-Erkennung zum Einsatz; `eval`, `exec`, `pickle` oder vergleichbare Codeausführung ist nicht vorhanden. Es wurden keine hartkodierten Secrets oder kritischen Schwachstellen gefunden.

Die folgenden Punkte sind als Härtungsmaßnahmen zu verstehen. Sie sind kein Blocker, sollten aber vor einem Release umgesetzt werden.

### Festgestellte Befunde

#### 1. Medium – Terminal-Escape-Injection über CSV-Spaltennamen
- **Betroffene Stelle**: `csvstat/text_output.py`, Funktion `render_text`; Spaltennamen werden ungeprüft aus der CSV-Datei übernommen und in `stdout` geschrieben.
- **Beschreibung**: Ein Angreifer kann eine CSV-Datei mit bösartigen ANSI-/Terminal-Escape-Sequenzen im Header (z. B. `\x1b[2J`, `\x1b]0;evil\x07`) bereitstellen. Wenn ein Benutzer diese Datei mit `csvstat` analysiert und die Textausgabe in einem Terminal betrachtet, kann der Terminalzustand manipuliert werden. Die JSON-Ausgabe ist davon nicht betroffen, da `json.dumps` Steuerzeichen standardmäßig escaped.
- **Fix**: Vor der Textausgabe alle Steuerzeichen (Codepoints `0x00–0x1F` und `0x7F`) in Spaltennamen filtern oder sichtbar escapen, z. B.:
  ```python
  import re
  def _sanitize(value: str) -> str:
      return re.sub(r"[\x00-\x1f\x7f]", "", value)
  ```
  Dies muss mit der Produktfunktion vereinbar sein: Spaltennamen aus legitimen CSV-Dateien ohne Steuerzeichen bleiben unverändert erhalten.

#### 2. Low – Ungültiger `--delimiter` verursacht unbehandelten Traceback
- **Betroffene Stelle**: `csvstat/cli.py`, nach der Umwandlung von `TAB`/`\\t`.
- **Beschreibung**: Wird ein mehrstelliger Delimiter (z. B. `::`) übergeben, wirft `csv.reader(..., delimiter=delimiter)` einen `TypeError` („delimiter must be a 1-character string“). Dieser wird nicht abgefangen; es erscheint ein Python-Traceback. Das verletzt den Geist der sauberen Fehlerbehandlung aus AC-05/AC-06 (verständliche Fehlermeldung auf `stderr`, Exit-Code 1, kein Traceback).
- **Fix**: Delimiter vor der Verwendung validieren:
  ```python
  if len(delimiter) != 1:
      print("Fehler: Das Trennzeichen muss genau ein Zeichen sein.", file=sys.stderr)
      return 1
  ```
  Alternativ den `TypeError` gezielt abfangen und als verständliche Fehlermeldung ausgeben.

#### 3. Low – Nicht standardkonformes JSON bei `inf`-Werten
- **Betroffene Stelle**: `csvstat/analysis.py`, Funktion `_parse_number`; `csvstat/json_output.py`, `json.dumps`.
- **Beschreibung**: `float("inf")` bzw. `float("-inf")` wird als gültige Zahl erkannt. Enthält eine Spalte den Wert `inf`, erzeugt die JSON-Ausgabe `Infinity` bzw. `-Infinity`. Python akzeptiert das beim Parsen, aber es ist kein strikt valides JSON nach RFC 8259 und kann bei maschineller Weiterverarbeitung zu Fehlern führen.
- **Fix**: In `_parse_number` nur endliche Zahlen akzeptieren:
  ```python
  import math

  def _parse_number(value: str) -> float | None:
      try:
          number = float(value)
      except ValueError:
          try:
              number = float(int(value))
          except ValueError:
              return None
      return number if math.isfinite(number) else None
  ```
  Dadurch werden `inf`-Werte als Text behandelt, die JSON-Ausgabe bleibt valide und die Produktfunktion (Statistiken für echte numerische Spalten) bleibt korrekt.

### Geprüfte Bereiche ohne Befund

- **Secrets**: Keine hartkodierten Schlüssel, Passwörter, Tokens oder URLs im sichtbaren Code. `.gitignore` schließt übliche Umgebungs-/Secret-Dateien aus.
- **Injection/Inputs**: Keine SQL-, Command-, Path- oder Deserialisierungs-Injection. Die Datei wird nur lesend geöffnet; es gibt keine Shell-Ausführung. CSV-Inhalte werden nicht als Code interpretiert.
- **AuthN/AuthZ**: Entfällt – lokales CLI ohne Authentifizierung.
- **Dependencies**: Nur Python-Standardbibliothek plus pytest als optionale Dev-Abhängigkeit. Keine bekannten ausgenutzten CVEs sichtbar. Die Scanner `bandit` und `semgrep` wurden übersprungen (`[skipped]`); deren Ausbleiben ist eine dokumentierte Lücke, aber kein Befund.
- **Konfiguration/Transport**: Keine Netzwerkkommunikation, keine unsicheren Standardeinstellungen oder offenen Debug-/CORS-Optionen.

### Empfehlung
Die drei Befunde sind Härtungsmaßnahmen ohne akutes Exploit-Risiko. Nach Umsetzung der Fixes kann der Freigabeprozess erneut bewertet werden.