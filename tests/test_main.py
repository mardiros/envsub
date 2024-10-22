import io

from envsub.__main__ import main


def test_main(monkeypatch):
    monkeypatch.setenv('NAME', 'World')
    stdout = io.StringIO()
    monkeypatch.setattr('sys.stdin', io.StringIO('Hello, ${NAME}!'))
    monkeypatch.setattr('sys.stdout', stdout)
    main()
    assert stdout.getvalue() == 'Hello, World!'
