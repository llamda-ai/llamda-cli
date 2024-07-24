"""
Collects all .md files from a folder and subfolder into a nested dictionary,
with the name as key and the content as value (if file) or a nested dictionary
(if folder).
"""

import os

from llamda_cli.lld_utils import FileTree, console

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


def yes_or_ask(question: str, yes: bool = True) -> bool:
    """
    If yes is True, returns True.
    If yes is False, asks the user if they want to include the file or folder.
    """
    if yes:
        return True
    return console.ask(question, default=True)


def get_md_files(path: str, base_path: str = "", yes: bool = False) -> FileTree:
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
            if not yes_or_ask(
                f":file_folder: {item_path.replace(base_path, '')}?", yes=yes
            ):
                continue
            if not yes:
                yes = console.ask("Include all files in this folder?", default=True)
            result[item] = get_md_files(item_path, base_path=base_path, yes=yes)
        elif item.endswith(".md") and item not in IGNORED_FILES:
            if not yes_or_ask(
                f"\t :page_facing_up: {item}?",
                yes=yes,
            ):
                continue
            with open(item_path, "r", encoding="utf-8") as file:
                result[item] = file.read()

    return result
