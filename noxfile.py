import nox


@nox.session(python=["3.7", "3.8", "3.9", "3.10"])
def tests(session):
    session.install("poetry")
    session.run("poetry", "install")
    session.run("pytest", *session.posargs)


@nox.session()
def lint(session):
    session.install("poetry")
    session.run("poetry", "install", "--no-root")
    session.run("black", "--check", ".")
    session.run("mypy", ".")
    session.run("flake8", "src", "tests")
