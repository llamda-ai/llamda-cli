"""decorators for common options and other arguments"""

import functools
from functools import wraps
import os
from typing import Any, Callable, List

import rich_click as click

from ..utils.console import console


def common_options(func: Callable[..., Any]) -> Callable[..., Any]:
    """adds the common args and options to a command: path, verbose, yes"""

    @click.argument("path", type=click.Path(exists=True), required=True, default=".")
    @click.option(
        "-v",
        "--verbose",
        is_flag=True,
        required=False,
        default=False,
        help="Verbose output.",
    )
    @click.option(
        "-y",
        "--yes",
        is_flag=True,
        required=False,
        default=False,
        help="Automatically confirm all prompts.",
    )
    @functools.wraps(func)
    def wrapper(
        *args: Any, verbose: bool = False, yes: bool = False, **kwargs: Any
    ) -> Any:

        console.set_verbose(verbose)
        console.set_yes(yes)
        return func(*args, **kwargs)

    return wrapper


def with_extensions(default_extensions: List[str]) -> Callable[..., Any]:
    """Decorator to add an extensions option to a command."""

    def decorator(func: Callable[..., Any]) -> Callable[..., Any]:
        @click.option(
            "--extension",
            "-e",
            type=click.STRING,
            multiple=True,
            help="The extension(s) of the files to search for.",
            default=default_extensions,
        )
        @wraps(func)
        def wrapper(*args: Any, **kwargs: Any) -> Callable[..., Any]:
            extension: tuple[str, ...] = kwargs.get("extension", ())
            if not extension:
                extension = tuple(default_extensions)

            kwargs["extension"] = extension
            return func(*args, **kwargs)

        return wrapper

    return decorator


def with_outfile(default_extension: str = ".xml") -> Callable[..., Any]:
    """Decorator to add an outfile option to a command."""

    def decorator(func: Callable[..., Any]) -> Callable[..., Any]:
        @click.option(
            "-o",
            "--outfile",
            type=click.Path(),
            required=False,
            default=None,
            help=r"""The output file path. Defaults to:
            /{current_dir}/{source_dirname}{default_extension}""",
        )
        @wraps(func)
        def wrapper(*args: Any, outfile: str | None = None, **kwargs: Any) -> Any:
            result = func(*args, **kwargs)

            if outfile is None:
                current_dir = os.getcwd()
                source_dirname = os.path.basename(current_dir)
                outfile = os.path.join(
                    current_dir, f"{source_dirname}{default_extension}"
                )

            # Write the result to the outfile
            with open(outfile, "w", encoding="utf-8") as f:
                f.write(str(result))

            console.c.log(f"Wrote {outfile}")
            return result

        return wrapper

    return decorator
