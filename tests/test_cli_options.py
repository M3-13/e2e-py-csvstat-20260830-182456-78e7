"""End-to-end tests for csvstat command-line options."""

import csvstat.cli as cli


def _write(tmp_path, name, content):
    path = tmp_path / name
    path.write_text(content, encoding="utf-8")
    return path


def test_default_comma_delimiter(tmp_path, capsys):
    path = _write(tmp_path, "data.csv", "a,b\n1,x\n2,y\n3,z\n")
    assert cli.main([str(path)]) == 0
    out = capsys.readouterr().out
    assert "Spalte: a" in out
    assert "count: 3" in out
    assert "Spalte: b" in out
    assert "distinct: 3" in out


def test_semicolon_delimiter(tmp_path, capsys):
    path = _write(tmp_path, "data.csv", "a;b\n1;x\n2;y\n3;z\n")
    assert cli.main([str(path), "--delimiter", ";"]) == 0
    out = capsys.readouterr().out
    assert "count: 3" in out
    assert "distinct: 3" in out


def test_columns_filter(tmp_path, capsys):
    path = _write(tmp_path, "data.csv", "a,b,c\n1,x,10\n2,y,20\n")
    assert cli.main([str(path), "--columns", "a,c"]) == 0
    out = capsys.readouterr().out
    assert "Spalte: a" in out
    assert "Spalte: c" in out
    assert "Spalte: b" not in out


def test_unknown_column_exits_one(tmp_path, capsys):
    path = _write(tmp_path, "data.csv", "a,b\n1,x\n")
    assert cli.main([str(path), "--columns", "a,zzz"]) == 1
    err = capsys.readouterr().err
    assert "zzz" in err


def test_header_without_data_rows(tmp_path, capsys):
    path = _write(tmp_path, "data.csv", "a,b\n")
    assert cli.main([str(path)]) == 0
    out = capsys.readouterr().out
    assert "count: 0" in out
    assert "missing: 0" in out
