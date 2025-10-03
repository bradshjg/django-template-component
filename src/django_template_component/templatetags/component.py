from django import template

from django_template_component.registry import component_registry

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
    extra_context = template.base.token_kwargs(remaining, parser)
    return ComponentNode(component_name[1:-1], extra_context)


class ComponentNode(template.Node):
    def __init__(self, component_name: str, kwargs: dict):
        self.component_name = component_name
        self.kwargs = kwargs

    def render(self, context):
        component_cls = component_registry.get(self.component_name)
        kwargs = {key: value.resolve(context) for key, value in self.kwargs.items()}
        return component_cls(**kwargs).render()
