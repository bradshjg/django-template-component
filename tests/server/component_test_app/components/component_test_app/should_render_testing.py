from django_template_component import TemplateComponent, register_component


@register_component("component_test_app/should_render_testing")
class ShouldRenderComponent(TemplateComponent):
    template_name = "component_test_app/should_render_testing.html"

    def __init__(self, *, should_render: bool):
        self._should_render = should_render

    def get_context(self):
        return {}

    def should_render(self):
        return self._should_render
