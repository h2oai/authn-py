import nox_poetry as nox


@nox.session(python=["3.7", "3.8", "3.9", "3.10"])
def tests(session):
    session.install("pytest", "pytest-asyncio", "respx", "time-machine")
    session.install(".")
    session.run("pytest", *session.posargs)


@nox.session()
def lint(session):
    session.install(".")
    session.install("black", "mypy")
    session.install(
        "flake8",
        "flake8-bugbear",
        "flake8-builtins",
        "flake8-deprecated",
        "flake8-eradicate",
    )
    session.run("black", "--check", ".")
    session.run("mypy", "src")
    session.run("flake8", "src", "tests")
