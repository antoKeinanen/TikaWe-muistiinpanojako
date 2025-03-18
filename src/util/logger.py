from typing import ClassVar, Literal


class Logger:
    _level_colors: ClassVar[dict] = {
        "log": "\x1b[38;20m",
        "warning": "\x1b[33;20m",
        "error": "\x1b[31;20m",
    }

    _level_prefixes: ClassVar[dict] = {
        "log": " [I] ",
        "warning": " [W] ",
        "error": " [X] ",
    }

    _reset = "\x1b[0m"

    @staticmethod
    def _format(values: tuple, level: Literal["log", "warning", "error"]) -> str:
        level = str(level)
        return str(
            Logger._level_colors[level]
            + Logger._level_prefixes[level]
            + " ".join([str(v) for v in values])
            + Logger._reset
        )

    @staticmethod
    def _output(values: tuple, level: Literal["log", "warning", "error"]) -> None:
        value = Logger._format(values, level)
        print(value, flush=True)  # noqa: T201

    @staticmethod
    def log(*values: tuple) -> None:
        Logger._output(values, "log")

    @staticmethod
    def warning(*values: tuple) -> None:
        Logger._output(values, "warning")

    @staticmethod
    def error(*values: tuple) -> None:
        Logger._output(values, "error")
