"""CLI for llamdadoc."""

import rich_click as click

from ..utils.git import GitSingleton
from ..files import get_files
from .option_decorators import with_outfile
from .option_decorators import common_options
from .option_decorators import with_extensions


@click.group
def lld() -> None:
    """llamda's cli tools."""
    # Reset the Git instance when the CLI is invoked
    GitSingleton.reset_instance()


@lld.command
@common_options
@with_extensions(default_extensions=[".py"])
@with_outfile()
def files(path: str, extension: str) -> str:
    """Collect files from a path."""
    content: str = get_files(path=path, extension=extension)
    return content


@lld.command(deprecated=True)
@common_options
@with_outfile()
def docs(
    path: str,
) -> str:
    """Collect docs from a path and write them to an xml file ready for Anthropic's Claude."""

    content: str = get_files(path=path, extension=".md")
    return content


__all__: list[str] = ["lld"]
