"""
CLI to collect docs from a folder for use with LLMs.
"""

import os
from typing import List, Union

from llamda_cli.lld_utils import render_template, console, FileTree

NestedStrings = Union[str, List[Union[str, "NestedStrings"]]]

IGNORED_FILES: list[str] = [
    "_",
    ".",
    "CONTRIBUTING.md",
    "CODE_OF_CONDUCT.md",
    "SECURITY.md",
    "HISTORY.md",
    "LICENSE.md",
    "release",
    "tests",
    "venv",
    "__pycache__",
]


def is_ignored(file: str) -> bool:
    """
    Check if a file is ignored.
    """
    return file.startswith(".") or file in IGNORED_FILES


def get_md_files(path: str, base_path: str = "") -> FileTree:
    """
    Collects all .md files from a folder and subfolder into a nested dictionary,
    with the name as key and the content as value (if file) or a nested dictionary
    (if folder).
    """
    result: FileTree = {}

    list_dir: list[str] = os.listdir(path)

    for item in list_dir:
        if (
            item.startswith(".")
            or item in IGNORED_FILES
            or item.startswith("_")
            or item.startswith("release/")
        ):
            continue
        item_path: str = os.path.join(path, item)
        if os.path.isdir(item_path):
            # prompt the user to skip the folder
            if not console.ask(
                f":file_folder: {item_path.replace(base_path, '')}?", default=True
            ):
                continue
            result[item] = get_md_files(item_path, base_path=base_path)
        elif item.endswith(".md") and item not in IGNORED_FILES:
            if not console.ask(
                f"\t :page_facing_up: {item}?",
                default=True,
            ):
                continue
            with open(item_path, "r", encoding="utf-8") as file:
                result[item] = file.read()

    return result


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
