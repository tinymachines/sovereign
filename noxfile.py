"""Nox configuration for project-sovereign development tasks."""

import nox

# Python versions to test against
PYTHON_VERSIONS = ["3.13"]

# Paths
SRC_PATHS = ["src", "tests", "noxfile.py"]


@nox.session(python=PYTHON_VERSIONS)
def tests(session):
    """Run the test suite with pytest."""
    session.install("-e", ".[dev]")
    session.run("pytest", *session.posargs)


@nox.session(python=PYTHON_VERSIONS)
def coverage(session):
    """Run tests with coverage reporting."""
    session.install("-e", ".[dev]")
    session.run("pytest", "--cov", "--cov-report=html", "--cov-report=term-missing")


@nox.session(python=PYTHON_VERSIONS)
def lint(session):
    """Run linting with ruff."""
    session.install("ruff")
    session.run("ruff", "check", *SRC_PATHS)


@nox.session(python=PYTHON_VERSIONS)
def format(session):
    """Format code with ruff."""
    session.install("ruff")
    session.run("ruff", "format", *SRC_PATHS)


@nox.session(python=PYTHON_VERSIONS)
def format_check(session):
    """Check code formatting with ruff."""
    session.install("ruff")
    session.run("ruff", "format", "--check", *SRC_PATHS)


@nox.session(python=PYTHON_VERSIONS)
def typecheck(session):
    """Run type checking with pyright."""
    session.install("-e", ".[dev]")
    session.run("pyright", "src")


@nox.session(python=PYTHON_VERSIONS)
def docs(session):
    """Build documentation with mkdocs."""
    session.install("-e", ".[dev]")
    session.run("mkdocs", "build", "--strict")


@nox.session(python=PYTHON_VERSIONS)
def docs_serve(session):
    """Serve documentation locally."""
    session.install("-e", ".[dev]")
    session.run("mkdocs", "serve")


@nox.session(python=PYTHON_VERSIONS)
def benchmarks(session):
    """Run performance benchmarks."""
    session.install("-e", ".[dev]")
    session.run("pytest", "--benchmark-only", "tests/benchmarks/")


@nox.session(python=PYTHON_VERSIONS)
def property_tests(session):
    """Run property-based tests with Hypothesis."""
    session.install("-e", ".[dev]")
    session.run("pytest", "tests/property/", "-v", "--tb=short")


@nox.session(python=PYTHON_VERSIONS)
def clean(session):
    """Clean up build artifacts and cache files."""
    session.run("rm", "-rf", "build/", external=True)
    session.run("rm", "-rf", "dist/", external=True)
    session.run("rm", "-rf", "src/*.egg-info/", external=True)
    session.run("rm", "-rf", ".pytest_cache/", external=True)
    session.run("rm", "-rf", ".coverage", external=True)
    session.run("rm", "-rf", "htmlcov/", external=True)
    session.run("rm", "-rf", ".mypy_cache/", external=True)
    session.run("rm", "-rf", ".pytype/", external=True)
    session.run("find", ".", "-name", "__pycache__", "-type", "d", "-exec", "rm", "-rf", "{}", "+", external=True)


@nox.session
def changelog(session):
    """Build changelog from fragments."""
    session.install("towncrier")
    session.run("towncrier", "build", "--yes")


@nox.session
def changelog_draft(session):
    """Preview changelog without building."""
    session.install("towncrier")
    session.run("towncrier", "build", "--draft")