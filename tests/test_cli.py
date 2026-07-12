from crucible.cli import main


def test_main_runs(capsys):
    main()
    captured = capsys.readouterr()
    assert "crucible" in captured.out
