import invoke


@invoke.task(optional=["check"])
def lint(c: invoke.Context, *, check: bool = False):
    command = "ruff check"
    if check:
        command = "ruff check --fix"

    c.run(command)


@invoke.task(optional=["check"])
def format(c: invoke.Context, *, check: bool = False):  # noqa: A001
    command = "ruff format"
    if check:
        command = "ruff format --check"

    c.run(command)


@invoke.task(optional=["debug"])
def start(c: invoke.Context, *, debug: bool = False):
    command = "flask --app src/main run"
    if debug:
        command = "flask --app src/main --debug run"

    c.run(command)


@invoke.task
def setup(c: invoke.Context):
    command = "python setup.py"
    c.run(command)


@invoke.task
def setup_hooks(c: invoke.Context):
    command = "pre-commit install"
    c.run(command)


@invoke.task
def pre_commit(c: invoke.Context):
    command = "pre-commit run --all-files"
    c.run(command)
