"""Utilities for working with templates."""

import os
from typing import Any

from jinja2 import Environment, FileSystemLoader, Template
from .files import get_component_path


def render_template(
    component_name: str,
    template_name: str = "template.jinja2",
    context: dict[str, Any] | None = None,
) -> str:
    """
    Render a Jinja2 template given its path.

    Args:
        template_path (str): Path to the template file.
        context (dict, optional): Dictionary containing variables to be passed to the template.

    Returns:
        str: Rendered template as a string.
    """
    template_dir: str = os.path.dirname(get_component_path(component_name, "templates"))
    template_file: str = os.path.basename(template_name)

    env = Environment(loader=FileSystemLoader(template_dir))
    template: Template = env.get_template(template_file)

    return template.render(context or {})


__all__: list[str] = ["render_template"]
