"""Utilities for working with files."""

from typing import Dict, Union
import os

FileTree = Dict[str, Union[str, "FileTree"]]


def write_file(path: str, content: str) -> None:
    """Write content to a file."""
    with open(path, "w", encoding="utf-8") as f:
        f.write(content)


def get_package_root() -> str:
    """Get the path to the package root."""
    current_dir = os.path.dirname(os.path.abspath(__file__))
    return os.path.dirname(current_dir)


def get_component_path(component_name: str, path: str) -> str:
    """Get the path to a component's file."""
    base_dir = get_package_root()

    component_dirs: dict[str, str] = {
        "docs": "lld_docs",
    }

    component_dir: str = component_dirs.get(component_name, component_name)

    full_path: str = os.path.join(base_dir, component_dir, path)

    return os.path.abspath(full_path)
