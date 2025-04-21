import invoke
import sys
from src.util.logger import Logger


@invoke.task(optional=["check"])
def lint(c: invoke.Context, *, check: bool = False):  # noqa: D103
    command = "ruff check"
    if check:
        command = "ruff check --fix"

    c.run(command)


@invoke.task(optional=["check"])
def format(c: invoke.Context, *, check: bool = False):  # noqa: A001, D103
    command = "ruff format"
    if check:
        command = "ruff format --check"

    c.run(command)


@invoke.task(optional=["debug"])
def start(c: invoke.Context, *, debug: bool = False):  # noqa: D103
    command = "flask --app src/main run"
    if debug:
        command = "flask --app src/main --debug run"

    c.run(command)


@invoke.task
def setup(c: invoke.Context):  # noqa: D103
    command = "python scripts/setup.py"
    c.run(command)


@invoke.task
def setup_hooks(c: invoke.Context):  # noqa: D103
    command = "pre-commit install"
    c.run(command)


@invoke.task
def pre_commit(c: invoke.Context):  # noqa: D103
    command = "pre-commit run --all-files"
    c.run(command)


@invoke.task(setup)
def seed_test(c: invoke.context):  # noqa: D103
    command = "python scripts/seed_test.py"
    c.run(command)


@invoke.task(seed_test)
def test(c: invoke.Context):  # noqa: D103
    result = input("Warning! This will reset the database. Is this ok? [Y/n]: ").lower()

    if len(result) > 0 and not result.startswith("y"):
        Logger.log("Cancelled!")
        sys.exit()

    command = "pytest"
    c.run(command)

    setup(c)
