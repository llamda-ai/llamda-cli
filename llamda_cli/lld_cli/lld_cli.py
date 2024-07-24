"""CLI for llamdadoc."""

import rich_click as click
from llamda_cli.lld_utils import console
from llamda_cli.lld_docs import collect_docs
from llamda_cli.lld_utils import write_file


@click.group()
def main() -> None:
    """llamda's cli tools."""


@main.command()
@click.argument("path", type=click.Path(exists=True))
@click.option(
    "-o",
    "--outfile",
    type=click.Path(),
    required=False,
    help=r"""The output file path. Defaults to:
    /{current_dir}/{source_dirname}.xml""",
)
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
def docs(
    path: str,
    outfile: str | None = None,
    verbose: bool = False,
    yes: bool = False,
) -> None:
    """Collect docs from a path and write them to an xml file ready for Anthropic's Claude."""
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
