from __future__ import annotations

import re

from django import template

from django_template_component.registry import ComponentNotRegisteredError, component_registry

register = template.Library()


@register.tag(name="component")
def do_component(parser, token):
    try:
        tag_name, component_name, *remaining = token.split_contents()
    except ValueError as e:
        msg = "component tag requires a quoted template name and key=value arguments"
        raise template.TemplateSyntaxError(msg) from e
    if not (component_name[0] == component_name[-1] and component_name[0] in ('"', "'")):
        msg = f"{tag_name!r} tag's template name should be in quotes"
        raise template.TemplateSyntaxError(msg)
    extra_context = token_kwargs(remaining, parser)
    return ComponentNode(component_name[1:-1], extra_context)


kwarg_re = re.compile(r"(\w+)=(.+)")
invalid_kwargs_msg = "'component' tag requires 'key=value' arguments (values can be variables or literals)"


def token_kwargs(bits: list[str], parser) -> dict[str, str]:
    if not bits:
        return {}
    kwargs = {}
    while bits:
        match = kwarg_re.match(bits[0])
        if not match:
            raise template.TemplateSyntaxError(invalid_kwargs_msg)
        key, value = match.groups()
        kwargs[key] = parser.compile_filter(value)
        del bits[:1]
    return kwargs


class ComponentNode(template.Node):
    def __init__(self, component_name: str, kwargs: dict):
        self.component_name = component_name
        self.kwargs = kwargs

    def render(self, context):
        try:
            component_cls = component_registry.get(self.component_name)
        except ComponentNotRegisteredError as e:
            msg = "error resolving component"
            raise template.TemplateSyntaxError(msg) from e
        kwargs = {key: value.resolve(context) for key, value in self.kwargs.items()}
        try:
            component = component_cls(**kwargs)
        except TypeError as e:
            msg = "error instantiating component"
            raise template.TemplateSyntaxError(msg) from e
        return component.render()
