"""Tests for the csvstat command-line interface."""

import csvstat.cli as cli


def test_help_shows_all_options(capsys):
    try:
        cli.main(["--help"])
    except SystemExit as exc:
        assert exc.code == 0
    out = capsys.readouterr().out
    assert "path" in out
    assert "--delimiter" in out
    assert "--columns" in out
    assert "--json" in out


def test_nonexistent_file_errors_without_traceback(tmp_path, capsys):
    path = tmp_path / "does_not_exist.csv"
    assert cli.main([str(path)]) == 1
    err = capsys.readouterr().err
    assert err.strip() != ""
    assert "Traceback" not in err


def test_empty_file_errors(tmp_path, capsys):
    path = tmp_path / "empty.csv"
    path.write_text("", encoding="utf-8")
    assert cli.main([str(path)]) == 1
    err = capsys.readouterr().err
    assert "leer" in err


def test_header_only_file_exits_zero(tmp_path, capsys):
    path = tmp_path / "header.csv"
    path.write_text("a,b,c\n", encoding="utf-8")
    assert cli.main([str(path)]) == 0
