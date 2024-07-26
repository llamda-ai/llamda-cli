"""llamda_cli package."""

from click import Group
from .lld_cli import lld

cli: Group = lld
