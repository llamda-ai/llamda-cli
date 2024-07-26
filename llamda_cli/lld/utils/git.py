"""Git utils"""

import os
from pathlib import Path
from typing import Any, Callable, Optional, TypedDict

from git import Diff, IndexFile, NoSuchPathError, Repo

from .console import console
from .files import is_binary, path_as_path


def null_if_no_repo(func: Callable[..., Any]) -> Callable[..., Any | None]:
    """Decorator which, applied to methods, returns null
    and logs if the instance has no self.repo"""
    # pylint: disable=import-outside-toplevel

    @path_as_path
    def wrapper(self: "Git", *args: Any, **kwargs: Any) -> Any | None:
        if self.no_repo:
            console.vlog(
                f"Calling {func.__name__} No repo found for {self.__class__.__name__}"
            )
            return None
        return func(self, *args, **kwargs)

    return wrapper


class GitDiff(TypedDict):
    """Git diff"""

    full_file: str
    diff_sections: list[dict[str, list[str]]]


class Git:
    """Git utils"""

    @path_as_path
    def __init__(self, path: Path) -> None:
        """Initialize the git utils"""
        try:
            self.no_repo = False
            self.repo = Repo(path)
        except NoSuchPathError:
            self.no_repo = True
            self.repo: Repo

    @classmethod
    def init(cls, path: Path) -> Optional["Git"]:
        """Initialize the git utils"""
        try:
            return cls(path)
        except NoSuchPathError:
            return None

    @property
    @null_if_no_repo
    def index(self) -> IndexFile:
        """Get the index"""
        return self.repo.index

    @null_if_no_repo
    def is_ignored(self, path: Path) -> bool:
        """Check if the path is ignored"""
        return len(self.repo.ignored(path)) > 0

    @null_if_no_repo
    def get_diff(self) -> dict[str, GitDiff]:
        """Get the diff for each modified file"""
        diff_data: dict[str, GitDiff] = {}
        diff_index: list[Diff] = self.repo.index.diff(None)
        for diff in diff_index:
            if diff.a_path is None:
                continue
            file_path: str = diff.a_path

            # skip ignored and binary files
            if (
                self.is_ignored(Path(file_path))
                or diff.a_blob is None
                or is_binary(Path(file_path))
            ):
                continue

            # Get the full file content
            full_file: str = diff.a_blob.data_stream.read().decode("utf-8")

            # Get the diff
            diff_text: str = self.repo.git.diff(file_path)

            # Parse the diff to get before/after sections
            sections: list[dict[str, list[str]]] = self._parse_diff(diff_text)

            diff_data[file_path] = {"full_file": full_file, "diff_sections": sections}

        return diff_data

    def _parse_diff(self, diff_text: str) -> list[dict[str, list[str]]]:
        """Parse the diff text to get before/after sections"""
        sections: list[dict[str, list[str]]] = []
        current_section: dict[str, list[str]] = {"before": [], "after": []}
        lines: list[str] = diff_text.split("\n")

        for line in lines:
            if line.startswith("@@"):
                if current_section["before"] or current_section["after"]:
                    sections.append(current_section)
                    current_section = {"before": [], "after": []}
            elif line.startswith("-"):
                current_section["before"].append(line[1:])
            elif line.startswith("+"):
                current_section["after"].append(line[1:])

        if current_section["before"] or current_section["after"]:
            sections.append(current_section)

        # Merge sections if they are close together
        merged_sections: list[dict[str, list[str]]] = []
        for i, section in enumerate(sections):
            if i > 0 and self._should_merge_diff_sections(merged_sections[-1], section):
                merged_sections[-1]["before"].extend(section["before"])
                merged_sections[-1]["after"].extend(section["after"])
            else:
                merged_sections.append(section)

        return merged_sections

    def _should_merge_diff_sections(
        self, section1: dict[str, list[str]], section2: dict[str, list[str]]
    ) -> bool:
        """Check if two sections should be merged"""
        total_lines: int = (
            len(section1["before"])
            + len(section1["after"])
            + len(section2["before"])
            + len(section2["after"])
        )
        gap = len(section2["before"]) - len(section1["after"])
        return gap < 0.2 * total_lines


class GitSingleton:
    """Git singleton"""

    _instance = None

    @classmethod
    def get_instance(cls) -> Git:
        """Get the git instance"""
        if cls._instance is None:
            cls._instance = Git(os.getcwd())
        return cls._instance

    @classmethod
    def reset_instance(cls):
        """Reset the git instance"""
        cls._instance = Git(os.getcwd())


# Create a convenience function to get the Git instance
def giddit() -> Git:
    """Get the git instance"""
    return GitSingleton.get_instance()


__all__: list[str] = ["giddit"]
