"""
CLI to collect docs from a folder for use with LLMs.
"""

import os
from typing import List, Union
from llamda_cli.lld_docs.get_md_files import get_md_files

from llamda_cli.lld_utils import render_template, console, FileTree

NestedStrings = Union[str, List[Union[str, "NestedStrings"]]]


def get_nested_keys(tree: FileTree) -> NestedStrings:
    """
    Get the keys of a nested dictionary.
    """
    result: list[NestedStrings] = []
    for key, value in tree.items():
        if isinstance(value, dict):
            result.append([key, get_nested_keys(value)] if len(value) > 0 else key)
        else:
            result.append(key if len(value) > 0 else key)
    return result


def collect_docs(path: str) -> str:
    """
    Collects all .md files from a folder and subfolder into a single string,
    with XML demarcation and a table of contents.
    """
    title: str = os.path.basename(os.path.dirname(path))
    console.vprint(f"[bold|yellow]{title}[/bold|yellow] ({path})")

    if not console.yes:
        console.print(
            "\n\n[bold|yellow]Select files and folders to include:[/bold|yellow]"
        )

    file_tree: FileTree = get_md_files(path, base_path=path)
    files: list[dict[str, str]] = []

    def flatten_tree(tree: FileTree, prefix: str = "") -> None:
        for name, content in tree.items():
            if isinstance(content, dict):
                flatten_tree(content, f"{prefix}{name}/")
            else:
                files.append({"name": f"{prefix}{name}", "content": content})

    flatten_tree(file_tree)

    # Render the template
    content: str = render_template(
        component_name="docs",
        context={"title": title, "files": files},
    )
    return content


__all__: list[str] = ["collect_docs"]
