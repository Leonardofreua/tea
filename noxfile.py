import tempfile

import nox


nox.options.sessions = "lint", "safety"
locations = "src", "tests", "noxfile.py"


def install_with_constraints(session, *args, **kwargs):
    """Install packages constrained by Poetry's lock file.

    This function is a wrapper for nox.sessions.Session.install. It
    invokes pip to install packages inside of the session's virtualenv.
    Additionally, pip is passed a constraints file generated from
    Poetry's lock file, to ensure that the packages are pinned to the
    versions specified in poetry.lock. This allows you to manage the
    packages as Poetry development dependencies.

    Parameters
    ----------
    session :
        the session object.
    args :
        command-line arguments for pip
    kwargs :
        additional keyword arguments for Session.install.
    """
    with tempfile.NamedTemporaryFile() as requirements:
        session.run(
            "poetry",
            "export",
            "--dev",
            "--format=requirements.txt",
            f"--output={requirements.name}",
            external=True,
        )
        session.install(f"--constraint={requirements.name}", *args, **kwargs)


@nox.session(python=["3.8", "3.7"])
def black(session):
    """Applying of the black guidelines."""
    args = session.posargs or locations
    install_with_constraints(session, "black")
    session.run("black", *args)


@nox.session(python=["3.8", "3.7"])
def bandit(session):
    """Applying of the bandit guidelines."""
    args = session.posargs or locations
    install_with_constraints(session, "bandit")
    session.run("bandit", *args)


@nox.session(python=["3.8", "3.7"])
def isort(session):
    """Reorder the imports"""
    args = session.posargs or locations
    install_with_constraints(session, "isort")
    session.run("isort", *args)


@nox.session(python=["3.8", "3.7"])
def lint(session):
    """Lint using flake8."""
    args = session.posargs or locations
    install_with_constraints(
        session, "flake8", "flake8-bugbear",
    )
    session.run("flake8", *args)


@nox.session(python="3.8")
def safety(session):
    """Scan dependencies for insecure packages."""
    with tempfile.NamedTemporaryFile() as requirements:
        session.run(
            "poetry",
            "export",
            "--dev",
            "--format=requirements.txt",
            "--without-hashes",
            f"--output={requirements.name}",
            external=True,
        )
        install_with_constraints(session, "safety")
        session.run("safety", "check", f"--file={requirements.name}", "--full-report")


@nox.session(python=["3.8", "3.7"])
def tests(session):
    """Run the test suite."""
    args = session.posargs or ["--cov"]
    session.run("poetry", "install", "--no-dev", external=True)
    install_with_constraints(session, "coverage[toml]", "pytest", "pytest-cov")
    session.run("pytest", *args)
