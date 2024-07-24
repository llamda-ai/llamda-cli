"""llamda_cli package."""

from click import Group
from .lld_cli import main

main: Group = main
