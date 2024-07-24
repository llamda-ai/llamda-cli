"""CLI for llamdadoc."""

import click
from llamda_cli.lld_utils import console
from llamda_cli.lld_docs import collect_docs
from llamda_cli.lld_utils import write_file


@click.group()
def main() -> None:
    """llamda's cli tools."""


@main.command()
@click.argument("path", type=click.Path(exists=True))
@click.option("-o", "--outfile", type=click.Path(), required=False)
@click.option("-v", "--verbose", is_flag=True, required=False, default=False)
@click.option("-y", "--yes", is_flag=True, required=False, default=False)
def docs(
    path: str,
    outfile: str | None = None,
    verbose: bool = False,
    yes: bool = False,
) -> None:
    """Collect docs from a path and write them to an outfile."""
    console.set_verbose(verbose)
    console.set_yes(yes)
    if outfile is None:
        outfile = path.split(".")[0] + ".xml"
    content: str = collect_docs(path=path)
    if len(content) == 0:
        raise ValueError("No content to write to file.")
    console.vprint()
    console.print(f"Writing to {outfile}")
    write_file(path=str(outfile), content=content)


if __name__ == "__main__":
    main()
