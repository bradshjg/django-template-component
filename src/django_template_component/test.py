from django_template_component.registry import component_registry


def render_component(component_name: str, **kwargs):
    component_cls = component_registry.get(component_name)
    component = component_cls(**kwargs)
    return component.render()
