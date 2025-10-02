from django import template

register = template.Library()


@register.tag(name="component")
def do_component(parser, token):
    import pdb; pdb.set_trace()
