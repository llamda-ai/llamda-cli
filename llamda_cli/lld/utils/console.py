"""CLI utils."""

from typing import Any
from rich.console import Console
from rich.prompt import Confirm


class VConsole:
    """A console with verbose mode."""

    def __init__(self, verbose: bool = False, yes: bool = False) -> None:
        self.c = Console()
        self.verbose = verbose
        self.yes = yes

    def ask(self, *args: Any, **kwargs: Any) -> bool:
        """Confirm the user's choice."""
        if self.yes:
            return True
        return Confirm.ask(*args, **kwargs)

    def print(self, *args: Any, **kwargs: Any) -> None:
        """Always print, regardless of verbose setting."""
        self.c.print(*args, **kwargs)

    def vprint(self, *args: Any, **kwargs: Any) -> None:
        """Print only if verbose is True."""
        if self.verbose:
            self.c.print(*args, **kwargs)

    def vlog(self, *args: Any, **kwargs: Any) -> None:
        """Print only if verbose is True."""
        if self.verbose:
            self.c.log(*args, **kwargs)

    def set_verbose(self, verbose: bool) -> None:
        """Set the verbose mode."""
        self.verbose: bool = verbose

    def set_yes(self, yes: bool) -> None:
        """Set the autoconfirm mode."""
        self.yes: bool = yes

    def yes_or_ask(self, question: str, yes: bool = True) -> bool:
        """
        If yes is True, returns True.
        If yes is False, asks the user if they want to include the file or folder.
        """
        if yes:
            return True
        return self.ask(question, default=True)


# Create a global instance of VerboseConsole
console = VConsole()
__all__: list[str] = ["console"]
