"""Tools for collecting docs from a given folder or git repo."""

from .files import collect_files as get_files

__all__: list[str] = ["get_files"]
