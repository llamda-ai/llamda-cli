"""Utilities for working with files."""

from typing import Dict, Union, Callable, Any
import os
from pathlib import Path

from .console import console


IGNORED_PREFIXES: tuple[str, ...] = (
    ".",
    "_",
    "release/",
    "venv/",
    "dist/",
    "build/",
    "__pycache__",
)

FileTree = Dict[str, Union[str, "FileTree"]]


def write_file(path: str, content: str) -> None:
    """Write content to a file."""
    with open(path, "w", encoding="utf-8") as f:
        f.write(content)


def normalise_path(path: str) -> Path:
    """Normalise a path."""
    return Path(path)


def is_binary(path: Path) -> bool:
    """Check if a file is binary."""

    try:
        with open(path, "r", encoding="utf-8") as f:
            f.readline()
    except UnicodeDecodeError:
        return True
    return False


def path_as_path(func: Callable[..., Any]) -> Callable[..., Any]:
    """Convert path arguments to Path objects."""

    def wrapper(self: Any, *args: Any, **kwargs: Any) -> Any:
        if not kwargs.get("path"):
            return func(self, *args, **kwargs)

        if "path" in kwargs and isinstance(kwargs["path"], (str, Path)):
            kwargs["path"] = Path(kwargs["path"])

        return func(self, *args, **kwargs)

    return wrapper


def get_package_root() -> str:
    """Get the path to the package root."""
    current_dir: str = os.path.dirname(os.path.abspath(__file__))
    return os.path.dirname(current_dir)


def get_component_path(component_name: str, path: str) -> str:
    """Get the path to a component's file."""
    base_dir: str = get_package_root()

    component_dirs: dict[str, str] = {
        "files": "files",
        "docs": "files",
    }

    component_dir: str = component_dirs.get(component_name, component_name)

    full_path: str = os.path.join(base_dir, component_dir, path)

    return os.path.abspath(full_path)


def is_ignored(file: str) -> bool:
    """
    Check if a file is ignored.
    """
    from .git import giddit

    return giddit().is_ignored(file) or any(
        file.startswith(prefix) for prefix in IGNORED_PREFIXES
    )


def get_files_of_type(
    path: str,
    base_path: str = "",
    yes: bool = False,
    extension: str | tuple[str, ...] = "md",
) -> FileTree:
    """
    Collects all files of a given type from a folder and subfolder into a nested dictionary,
    with the name as key and the content as value (if file) or a nested dictionary
    (if folder).
    """
    extensions: tuple[str, ...] = (
        extension if isinstance(extension, tuple) else (extension,)
    )
    result: FileTree = {}

    list_dir: list[str] = os.listdir(path)

    for item in list_dir:
        if is_ignored(item):
            continue
        item_path: str = os.path.join(path, item)
        if os.path.isdir(item_path):

            # prompt the user to skip the folder
            if not console.yes_or_ask(
                f":file_folder: {item_path.replace(base_path, '')}?", yes=yes
            ):
                continue
            if not yes:
                yes = console.ask("Include all files in this folder?", default=True)
            result[item] = get_files_of_type(
                item_path, base_path=base_path, yes=yes, extension=extensions
            )
        elif any(item.endswith(ext) for ext in extensions) and not is_ignored(item):
            if not console.yes_or_ask(
                f"\t :page_facing_up: {item}?",
                yes=yes,
            ):
                continue
            with open(item_path, "r", encoding="utf-8") as file:
                result[item] = file.read()

    return result


__all__: list[str] = ["get_files_of_type", "FileTree"]
